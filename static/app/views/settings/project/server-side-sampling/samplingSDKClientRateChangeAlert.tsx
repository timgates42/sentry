import {useEffect} from 'react';

import Alert from 'sentry/components/alert';
import Button from 'sentry/components/button';
import {t} from 'sentry/locale';
import {Organization, Project, SeriesApi} from 'sentry/types';
import {defined} from 'sentry/utils';
import trackAdvancedAnalyticsEvent from 'sentry/utils/analytics/trackAdvancedAnalyticsEvent';

import {RecommendedStepsModalProps} from './modals/recommendedStepsModal';
import {getClientSampleRates} from './utils';

type Props = Pick<RecommendedStepsModalProps, 'onReadDocs'> & {
  organization: Organization;
  projectId: Project['id'];
  projectStats?: SeriesApi;
};

export function SamplingSDKClientRateChangeAlert({
  projectStats,
  onReadDocs,
  organization,
  projectId,
}: Props) {
  const {diff: clientSamplingDiff} = getClientSampleRates(projectStats);

  const recommendChangingClientSdk =
    defined(clientSamplingDiff) && clientSamplingDiff >= 50;

  useEffect(() => {
    if (!recommendChangingClientSdk) {
      return;
    }

    trackAdvancedAnalyticsEvent('sampling.sdk.client.rate.change.alert', {
      organization,
      project_id: projectId,
    });
  }, [recommendChangingClientSdk, organization, projectId]);

  if (!recommendChangingClientSdk) {
    return null;
  }

  return (
    <Alert
      type="info"
      showIcon
      trailingItems={
        <Button onClick={onReadDocs} priority="link" borderless>
          {t('Learn More')}
        </Button>
      }
    >
      {t(
        'To allow more metrics to be processed, we suggest changing your client(SDK) sample rate.'
      )}
    </Alert>
  );
}
