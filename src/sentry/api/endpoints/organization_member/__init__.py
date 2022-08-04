from __future__ import annotations

from typing import Collection, TypedDict

from django.db import transaction
from rest_framework.request import Request

from sentry import roles
from sentry.api.exceptions import SentryAPIException, status
from sentry.auth.superuser import is_active_superuser
from sentry.models import Organization, OrganizationMember, OrganizationMemberTeam, Team, TeamStatus
from sentry.roles.manager import Role, TeamRole


class InvalidTeam(SentryAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "invalid_team"
    message = "The team slug does not match a team in the organization"


class TeamRoleDict(TypedDict):
    teamSlug: str
    role: str


@transaction.atomic
def save_team_assignments(
    request: Request,
    organization_member: OrganizationMember,
    teams_with_roles: list[TeamRoleDict] = None,
):
    team_slugs = [item["teamSlug"] for item in teams_with_roles]
    target_teams = list(
        Team.objects.filter(
            organization=organization_member.organization,
            status=TeamStatus.VISIBLE,
            slug__in=team_slugs,
        )
    )
    if len(target_teams) != len(team_slugs):
        raise InvalidTeam

    # Avoids O(n * n) search later
    team_role_map = {}
    for item in teams_with_roles:
        team_role_map[item["teamSlug"]] = item["role"]

    new_rows = []
    for team in target_teams:
        new_rows.append((team, team_role_map[team.slug]))

    OrganizationMemberTeam.objects.filter(organizationmember=organization_member).delete()
    OrganizationMemberTeam.objects.bulk_create(
        [
            OrganizationMemberTeam(organizationmember=organization_member, team=team, role=role)
            for team, role in new_rows
        ]
    )

    """
    if not teams_with_roles:
        # Certain org-level roles has a superset of permissions compared to team-level roles
        # As such, we can delete their team-level role assignment
        minimum_team_role = roles.get_minimum_team_role(organization_member.role)
        applying_minimum = False

        # Avoids O(n * n) search later
        team_role_map = {}
        for item in teams_with_roles:
            team_role_map[item["teamSlug"]] = item["role"]

        new_rows = {}
        for team in target_teams:
            new_row[team.slug] = (team, team_role_map[team.slug])

        # curr_rows = list(
        #     OrganizationMemberTeam.objects.filter(organizationmember=organization_member).prefetch_related("team")
        # )
        # for row in curr_rows:
        #     row.team.slug

        # OrganizationMemberTeam.objects.create([
        #     OrganizationMemberTeam(organizationmember=organization_member, team=team, role=role)
        #     for team, role in org_member_teams
        # ])

            if not can_set_team_role(request, _):
                team_role.priority < minimum_team_role.priority
                applying_minimum = True
                item["role"] = None
            elif False:
                pass

        # OrganizationMemberTeam.objects.bulk_create([
        #     OrganizationMemberTeam(team=item["teamSlug"], role=item["role"], organizationmember=organization_member)
        #     for item in teams_with_roles
        # ])


        return
    """


@transaction.atomic
def deprecated_save_team_assignments(organization_member: OrganizationMember, teams: list[str]):
    """
    This method is used when a user invite an organization member.
    """
    target_teams = list(
        Team.objects.filter(
            organization=organization_member.organization, status=TeamStatus.VISIBLE, slug__in=teams
        )
    )
    # if len(target_teams) != len(teams):
    #     raise InvalidTeam

    OrganizationMemberTeam.objects.filter(organizationmember=organization_member).delete()
    OrganizationMemberTeam.objects.bulk_create(
        [
            OrganizationMemberTeam(organizationmember=organization_member, team=team)
            for team in target_teams
        ]
    )


def can_set_team_role(request: Request, team: Team, new_role: TeamRole) -> bool:
    if not can_admin_team(request, team):
        return False

    org_role = request.access.get_organization_role()
    if org_role and org_role.can_manage_team_role(new_role):
        return True

    team_role = request.access.get_team_role(team)
    if team_role and team_role.can_manage(new_role):
        return True

    return False


def can_admin_team(request: Request, team: Team) -> bool:
    if request.access.has_scope("org:write"):
        return True
    if not request.access.has_team_membership(team):
        return False
    return request.access.has_team_scope(team, "team:write")


def get_allowed_org_roles(
    request: Request,
    organization: Organization,
    member: OrganizationMember | None = None,
) -> Collection[Role]:
    """Get the set of org-level roles that the request is allowed to manage.

    In order to change another member's role, the returned set must include both
    the starting role and the new role. That is, the set contains the roles that
    the request is allowed to promote someone to and to demote someone from.
    """

    if is_active_superuser(request):
        return roles.get_all()
    if not request.access.has_scope("member:admin"):
        return ()

    if member is None:
        try:
            member = OrganizationMember.objects.get(user=request.user, organization=organization)
        except OrganizationMember.DoesNotExist:
            # This can happen if the request was authorized by an app integration
            # token whose proxy user does not have an OrganizationMember object.
            return ()

    return member.get_allowed_org_roles_to_invite()


from .details import OrganizationMemberDetailsEndpoint
from .index import OrganizationMemberIndexEndpoint
from .requests.invite.details import OrganizationInviteRequestDetailsEndpoint
from .requests.invite.index import OrganizationInviteRequestIndexEndpoint
from .requests.join import OrganizationJoinRequestEndpoint

__all__ = (
    "OrganizationInviteRequestDetailsEndpoint",
    "OrganizationInviteRequestIndexEndpoint",
    "OrganizationJoinRequestEndpoint",
    "OrganizationMemberDetailsEndpoint",
    "OrganizationMemberIndexEndpoint",
    "get_allowed_org_roles",
    "save_team_assignments",
    "deprecated_save_team_assignments",
)
