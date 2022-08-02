import {css} from '@emotion/react';

import {Theme} from 'sentry/utils/theme';

export const INPUT_PADDING = 12;

type Props = {
  theme: Theme;
  disabled?: boolean;
  monospace?: boolean;
  readOnly?: boolean;
};

const inputStyles = (props: Props) =>
  css`
    color: ${props.disabled ? props.theme.disabled : props.theme.formText};
    display: block;
    width: 100%;
    background: ${props.theme.background};
    border: 1px solid ${props.theme.border};
    border-radius: ${props.theme.borderRadius};
    box-shadow: inset ${props.theme.dropShadowLight};
    padding: ${INPUT_PADDING}px;
    resize: vertical;
    height: 40px;
    transition: border 0.1s, box-shadow 0.1s;

    ${props.monospace ? `font-family: ${props.theme.text.familyMono}` : ''};

    ${props.readOnly
      ? css`
          cursor: default;
        `
      : ''};

    &::placeholder {
      color: ${props.theme.formPlaceholder};
    }

    &[disabled] {
      background: ${props.theme.backgroundSecondary};
      color: ${props.theme.gray300};
      border: 1px solid ${props.theme.border};
      cursor: not-allowed;

      &::placeholder {
        color: ${props.theme.disabled};
      }
    }

    &:focus,
    &.focus-visible {
      outline: none;
      border-color: ${props.theme.focusBorder};
      box-shadow: ${props.theme.focusBorder} 0 0 0 1px;
    }
  `;

export {inputStyles};
