import round from 'lodash/round';

import {t} from 'sentry/locale';
import {SeriesApi} from 'sentry/types';
import {SamplingInnerName, SamplingRule, SamplingRuleType} from 'sentry/types/sampling';
import {defined} from 'sentry/utils';

import {projectStatsToSampleRates} from './projectStatsToSampleRates';

export const SERVER_SIDE_SAMPLING_DOC_LINK =
  'https://docs.sentry.io/product/data-management-settings/server-side-sampling/';

export function getInnerNameLabel(name: SamplingInnerName) {
  switch (name) {
    case SamplingInnerName.TRACE_ENVIRONMENT:
      return t('Environment');
    case SamplingInnerName.TRACE_RELEASE:
      return t('Release');
    default:
      return '';
  }
}

export const quantityField = 'sum(quantity)';

export function isUniformRule(rule?: SamplingRule) {
  if (!rule) {
    return false;
  }

  return rule.type === SamplingRuleType.TRACE && rule.condition.inner.length === 0;
}

export function isValidSampleRate(sampleRate: number | undefined) {
  if (!defined(sampleRate)) {
    return false;
  }

  return !isNaN(sampleRate) && sampleRate <= 1 && sampleRate >= 0;
}

export function rateToPercentage(rate: number | undefined, decimalPlaces: number = 2) {
  if (!defined(rate)) {
    return rate;
  }

  return round(rate * 100, decimalPlaces);
}

export function percentageToRate(rate: number | undefined, decimalPlaces: number = 4) {
  if (!defined(rate)) {
    return rate;
  }

  return round(rate / 100, decimalPlaces);
}

export function getClientSampleRates(
  projectStats: SeriesApi | undefined,
  specifiedClientRate?: number
) {
  const {trueSampleRate, maxSafeSampleRate} = projectStatsToSampleRates(projectStats);

  const current =
    defined(specifiedClientRate) && !isNaN(specifiedClientRate)
      ? specifiedClientRate
      : defined(trueSampleRate) && !isNaN(trueSampleRate)
      ? trueSampleRate
      : undefined;

  const recommended =
    defined(maxSafeSampleRate) && !isNaN(maxSafeSampleRate)
      ? maxSafeSampleRate
      : undefined;

  const recommendedPercentage = rateToPercentage(recommended);
  const currentPercentage = rateToPercentage(current);

  const diff =
    defined(recommendedPercentage) && defined(currentPercentage)
      ? Math.abs(recommendedPercentage - currentPercentage)
      : undefined;

  return {
    current,
    recommended,
    diff,
  };
}
