import {Fragment, useMemo} from 'react';
// eslint-disable-next-line no-restricted-imports
import {withRouter} from 'react-router';
import styled from '@emotion/styled';
import pick from 'lodash/pick';

import _EventsRequest from 'sentry/components/charts/eventsRequest';
import {getInterval, getPreviousSeriesName} from 'sentry/components/charts/utils';
import {t} from 'sentry/locale';
import {axisLabelFormatter} from 'sentry/utils/discover/charts';
import DiscoverQuery from 'sentry/utils/discover/discoverQuery';
import {QueryBatchNode} from 'sentry/utils/performance/contexts/genericQueryBatcher';
import {useMEPSettingContext} from 'sentry/utils/performance/contexts/metricsEnhancedSetting';
import {usePageError} from 'sentry/utils/performance/contexts/pageError';
import withApi from 'sentry/utils/withApi';
import _DurationChart from 'sentry/views/performance/charts/chart';

import {GenericPerformanceWidget} from '../components/performanceWidget';
import {transformDiscoverToSingleValue} from '../transforms/transformDiscoverToSingleValue';
import {transformEventsRequestToArea} from '../transforms/transformEventsToArea';
import {PerformanceWidgetProps, QueryDefinition, WidgetDataResult} from '../types';
import {eventsRequestQueryProps, getMEPQueryParams} from '../utils';

type DataType = {
  chart: WidgetDataResult & ReturnType<typeof transformEventsRequestToArea>;
  overall: WidgetDataResult & ReturnType<typeof transformDiscoverToSingleValue>;
};

export function SingleFieldAreaWidget(props: PerformanceWidgetProps) {
  const {ContainerActions} = props;
  const globalSelection = props.eventView.getPageFilters();
  const pageError = usePageError();
  const mepSetting = useMEPSettingContext();
  const useEvents = props.organization.features.includes(
    'performance-frontend-use-events-endpoint'
  );

  if (props.fields.length !== 1) {
    throw new Error(`Single field area can only accept a single field (${props.fields})`);
  }
  const field = props.fields[0];

  const chartQuery = useMemo<QueryDefinition<DataType, WidgetDataResult>>(
    () => ({
      fields: props.fields[0],
      component: provided => (
        <QueryBatchNode batchProperty="yAxis">
          {({queryBatching}) => (
            <EventsRequest
              {...pick(provided, eventsRequestQueryProps)}
              limit={1}
              queryBatching={queryBatching}
              includePrevious
              includeTransformedData
              partial
              currentSeriesNames={[field]}
              previousSeriesNames={[getPreviousSeriesName(field)]}
              query={provided.eventView.getQueryWithAdditionalConditions()}
              interval={getInterval(
                {
                  start: provided.start,
                  end: provided.end,
                  period: provided.period,
                },
                'medium'
              )}
              hideError
              onError={pageError.setPageError}
              queryExtras={getMEPQueryParams(mepSetting)}
            />
          )}
        </QueryBatchNode>
      ),
      transform: transformEventsRequestToArea,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [props.chartSetting, mepSetting.memoizationKey]
  );

  const overallQuery = useMemo<QueryDefinition<DataType, WidgetDataResult>>(
    () => ({
      fields: field,
      component: provided => {
        const eventView = provided.eventView.clone();

        eventView.sorts = [];
        eventView.fields = props.fields.map(fieldName => ({field: fieldName}));

        return (
          <DiscoverQuery
            {...provided}
            eventView={eventView}
            location={props.location}
            queryExtras={getMEPQueryParams(mepSetting)}
            useEvents={useEvents}
          />
        );
      },
      transform: transformDiscoverToSingleValue,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [props.chartSetting, mepSetting.memoizationKey]
  );

  const Queries = {
    chart: chartQuery,
    overall: overallQuery,
  };

  return (
    <GenericPerformanceWidget<DataType>
      {...props}
      Subtitle={() => (
        <Subtitle>
          {globalSelection.datetime.period
            ? t('Compared to last %s ', globalSelection.datetime.period)
            : t('Compared to the last period')}
        </Subtitle>
      )}
      HeaderActions={provided => (
        <Fragment>
          {provided.widgetData?.overall?.hasData ? (
            <Fragment>
              {props.fields.map(fieldName => (
                <HighlightNumber key={fieldName} color={props.chartColor}>
                  {axisLabelFormatter(
                    provided.widgetData?.overall?.[fieldName],
                    fieldName
                  )}
                </HighlightNumber>
              ))}
            </Fragment>
          ) : null}
          <ContainerActions {...provided.widgetData.chart} />
        </Fragment>
      )}
      Queries={Queries}
      Visualizations={[
        {
          component: provided => (
            <DurationChart
              {...provided.widgetData.chart}
              {...provided}
              disableMultiAxis
              disableXAxis
              definedAxisTicks={4}
              chartColors={props.chartColor ? [props.chartColor] : undefined}
            />
          ),
          height: props.chartHeight,
        },
      ]}
    />
  );
}

const EventsRequest = withApi(_EventsRequest);
export const DurationChart = withRouter(_DurationChart);
export const Subtitle = styled('span')`
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeMedium};
`;

export const HighlightNumber = styled('div')<{color?: string}>`
  color: ${p => p.color};
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
