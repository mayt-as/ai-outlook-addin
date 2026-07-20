import React from 'react';
import { MessageBar, MessageBarBody, MessageBarTitle, MessageBarActions, Button } from '@fluentui/react-components';

interface ErrorBannerProps {
  error: string | null;
  onDismiss: () => void;
}

export const ErrorBanner: React.FC<ErrorBannerProps> = ({ error, onDismiss }) => {
  if (!error) return null;
  
  return (
    <MessageBar intent="error" style={{ marginBottom: '10px' }}>
      <MessageBarBody>
        <MessageBarTitle>Error</MessageBarTitle>
        {error}
      </MessageBarBody>
      <MessageBarActions containerAction={<Button appearance="transparent" icon={<span>X</span>} onClick={onDismiss} />} />
    </MessageBar>
  );
};
