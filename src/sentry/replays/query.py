from collections import namedtuple
from datetime import datetime
from typing import Any, List, Optional, Union

from snuba_sdk import (
    Column,
    Condition,
    Entity,
    Function,
    Granularity,
    Identifier,
    Lambda,
    Limit,
    Offset,
    Op,
    Query,
    Request,
)
from snuba_sdk.orderby import Direction, OrderBy

from sentry.api.event_search import SearchConfig, SearchFilter
from sentry.utils.snuba import raw_snql_query

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 10
DEFAULT_OFFSET = 0

Paginators = namedtuple("Paginators", ("limit", "offset"))

replay_config = SearchConfig(
    duration_keys={"duration"},
    numeric_keys={"project_id"},
    date_keys={"started_at", "finished_at"},
    allowed_keys={
        "title",
        "platform",
        "release",
        "dist",
        "user.id",
        "user.email",
        "user.name",
        "user.ip_address",
        "sdk_name",
        "sdk_version",
        "duration",
        "count_segments",
    },
)


def query_replays_collection(
    project_ids: List[int],
    start: datetime,
    end: datetime,
    environment: List[str],
    sort: Optional[str],
    limit: Optional[str],
    offset: Optional[str],
    search_filters: List[SearchFilter],
) -> dict:
    """Query aggregated replay collection."""
    conditions = []
    if environment:
        conditions.append(Condition("environment"), Op.IN, environment)

    sort_ordering = make_sort_ordering(sort)
    paginators = make_pagination_values(limit, offset)

    response = query_replays_dataset(
        project_ids=project_ids,
        start=start,
        end=end,
        where=[],
        sorting=sort_ordering,
        pagination=paginators,
        search_filters=search_filters,
    )
    return response["data"]


def query_replay_instance(
    project_id: int,
    replay_id: str,
    start: datetime,
    end: datetime,
):
    """Query aggregated replay instance."""
    response = query_replays_dataset(
        project_ids=[project_id],
        start=start,
        end=end,
        where=[
            Condition(Column("replay_id"), Op.EQ, replay_id),
        ],
        sorting=[],
        pagination=None,
    )
    return response["data"]


def query_replays_dataset(
    project_ids: List[str],
    start: datetime,
    end: datetime,
    where: List[Condition],
    sorting: List[OrderBy],
    pagination: Optional[Paginators],
    search_filters: List[SearchFilter],
):
    query_options = {}

    # Instance requests do not paginate.
    if pagination:
        query_options["limit"] = Limit(pagination.limit)
        query_options["offset"] = Offset(pagination.offset)

    snuba_request = Request(
        dataset="replays",
        app_id="replay-backend-web",
        query=Query(
            match=Entity("replays"),
            select=make_select_statement(),
            where=[
                Condition(Column("project_id"), Op.IN, project_ids),
                Condition(Column("timestamp"), Op.LT, end),
                Condition(Column("timestamp"), Op.GTE, start),
                *where,
            ],
            having=[
                # Must include the first sequence otherwise the replay is too old.
                Condition(Function("min", parameters=[Column("sequence_id")]), Op.EQ, 0),
                # Discard short replays (5 seconds by arbitrary decision).
                Condition(Column("duration"), Op.GTE, 5),
                # User conditions.
                *search_filters_to_snuba_filters(search_filters),
            ],
            orderby=sorting,
            groupby=[Column("replay_id")],
            granularity=Granularity(3600),
            **query_options,
        ),
    )
    return raw_snql_query(snuba_request)


# Select.


def make_select_statement() -> List[Union[Column, Function]]:
    """Return the selection that forms the base of our replays response payload."""
    return [
        Column("replay_id"),
        # First, non-null value of a collected array.
        _grouped_unique_scalar_value(column_name="title"),
        _grouped_unique_scalar_value(column_name="project_id", alias="agg_project_id"),
        _grouped_unique_scalar_value(column_name="platform"),
        _grouped_unique_scalar_value(column_name="environment"),
        _grouped_unique_scalar_value(column_name="release"),
        _grouped_unique_scalar_value(column_name="dist"),
        Function(
            "IPv4NumToString",
            parameters=[
                _grouped_unique_scalar_value(
                    column_name="ip_address_v4",
                    aliased=False,
                )
            ],
            alias="ip_address_v4",
        ),
        Function(
            "IPv6NumToString",
            parameters=[
                _grouped_unique_scalar_value(
                    column_name="ip_address_v6",
                    aliased=False,
                )
            ],
            alias="ip_address_v6",
        ),
        _grouped_unique_scalar_value(column_name="user"),
        _grouped_unique_scalar_value(column_name="user_id"),
        _grouped_unique_scalar_value(column_name="user_email"),
        _grouped_unique_scalar_value(column_name="user_name"),
        _grouped_unique_scalar_value(column_name="sdk_name"),
        _grouped_unique_scalar_value(column_name="sdk_version"),
        _grouped_unique_scalar_value(column_name="tags.key"),
        _grouped_unique_scalar_value(column_name="tags.value"),
        # Flatten array of arrays.
        Function(
            "arrayMap",
            parameters=[
                Lambda(
                    ["trace_id"],
                    Function("toString", parameters=[Identifier("trace_id")]),
                ),
                Function(
                    "groupUniqArrayArray",
                    parameters=[Column("trace_ids")],
                ),
            ],
            alias="trace_ids",
        ),
        # Aggregations.
        Function("min", parameters=[Column("timestamp")], alias="started_at"),
        Function("max", parameters=[Column("timestamp")], alias="finished_at"),
        Function(
            "dateDiff",
            parameters=["second", Column("started_at"), Column("finished_at")],
            alias="duration",
        ),
        Function("groupArray", parameters=[Column("url")], alias="urls"),
        Function("count", parameters=[Column("url")], alias="count_urls"),
        Function("count", parameters=[Column("sequence_id")], alias="count_segments"),
    ]


def _grouped_unique_values(column_name: str, aliased: bool = False) -> Function:
    """Returns an array of unique, non-null values.

    E.g.
        [1, 2, 2, 3, 3, 3, null] => [1, 2, 3]
    """
    return Function(
        "groupUniqArray",
        parameters=[Column(column_name)],
        alias=column_name if aliased else None,
    )


def _grouped_unique_scalar_value(
    column_name: str, alias: Optional[str] = None, aliased: bool = True
) -> Function:
    """Returns the first value of a unique array.

    E.g.
        [1, 2, 2, 3, 3, 3, null] => [1, 2, 3] => 1
    """
    return Function(
        "arrayElement",
        parameters=[_grouped_unique_values(column_name), 1],
        alias=alias or column_name if aliased else None,
    )


# Filter.


OPERATOR_MAP = {
    "=": Op.EQ,
    "!=": Op.NEQ,
    ">": Op.GT,
    ">=": Op.GTE,
    "<": Op.LT,
    "<=": Op.LTE,
}


def search_filters_to_snuba_filters(search_filters: List[SearchFilter]) -> List[Condition]:
    for search_filter in search_filters:
        operator_string = search_filter.operator
        operator = OPERATOR_MAP.get(operator_string, "=")

        column_name = search_filter.key.name
        column_name = column_name.replace(".", "_")  # Translate nested fields to flat.

        yield Condition(Column(column_name), operator, search_filter.value.value)


# Sort.


def make_sort_ordering(sort: Optional[str]) -> List[OrderBy]:
    """Return the complete set of conditions to order our query by."""
    if sort == "started_at":
        orderby = [OrderBy(Column("started_at"), Direction.ASC)]
    elif sort == "finished_at":
        orderby = [OrderBy(Column("finished_at"), Direction.ASC)]
    elif sort == "-finished_at":
        orderby = [OrderBy(Column("finished_at"), Direction.DESC)]
    elif sort == "duration":
        orderby = [OrderBy(Column("duration"), Direction.ASC)]
    elif sort == "-duration":
        orderby = [OrderBy(Column("duration"), Direction.DESC)]
    else:
        # By default return the most recent replays.
        orderby = [OrderBy(Column("started_at"), Direction.DESC)]

    return orderby


# Pagination.


def make_pagination_values(limit: Any, offset: Any) -> Paginators:
    """Return a tuple of limit, offset values."""
    limit = _coerce_to_integer_default(limit, DEFAULT_PAGE_SIZE)
    if limit > MAX_PAGE_SIZE or limit < 0:
        limit = DEFAULT_PAGE_SIZE

    offset = _coerce_to_integer_default(offset, DEFAULT_OFFSET)
    return Paginators(limit, offset)


def _coerce_to_integer_default(value: Optional[str], default: int) -> int:
    """Return an integer or default."""
    if value is None:
        return default

    try:
        return int(value)
    except (ValueError, TypeError):
        return default
