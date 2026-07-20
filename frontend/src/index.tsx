import React, { useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { FluentProvider, webLightTheme } from '@fluentui/react-components';
import { useAppStore } from './store/useAppStore';
import { getSSOToken } from './services/auth';
import { ReadMode } from './pages/ReadMode';
import { ComposeMode } from './pages/ComposeMode';
import { ErrorBanner } from './components/ErrorBanner';

const App: React.FC = () => {
  const { isInitialized, mode, setInitialized, setMode, setAccessToken, error, setError } = useAppStore();

  useEffect(() => {
    Office.onReady((info) => {
      setInitialized(true);
      
      // Determine mode based on host capabilities
      if (info.host === Office.HostType.Outlook) {
        const item = Office.context.mailbox.item;
        if (item?.displayReplyForm !== undefined) {
          setMode('read');
        } else {
          setMode('compose');
        }
        
        // Attempt SSO silently
        getSSOToken()
          .then(token => setAccessToken(token))
          .catch(err => {
            console.warn("Failed silent SSO", err);
            // Non-blocking for UI, but API calls will fail until auth is solved
          });
      }
    });
  }, []);

  if (!isInitialized) {
    return <div style={{ padding: '20px' }}>Loading Outlook context...</div>;
  }

  return (
    <FluentProvider theme={webLightTheme}>
      <ErrorBanner error={error} onDismiss={() => setError(null)} />
      {mode === 'read' ? <ReadMode /> : <ComposeMode />}
    </FluentProvider>
  );
};

const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<App />);
}
