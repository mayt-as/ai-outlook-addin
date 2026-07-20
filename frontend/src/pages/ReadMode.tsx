import React, { useState } from 'react';
import { Button, Spinner, Text, Card, CardHeader, CardPreview } from '@fluentui/react-components';
import { AIClient } from '../services/aiClient';
import { useAppStore } from '../store/useAppStore';

export const ReadMode: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<string | null>(null);
  const { setError } = useAppStore();
  
  // Note: in a real environment, you'd get the actual ID via Office.context.mailbox.item.itemId
  const currentMessageId = "dummy-item-id"; 

  const handleSummarize = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await AIClient.getSummary(currentMessageId, "concise");
      setSummary(res.summary);
    } catch (err: any) {
      setError(err.message || "Failed to fetch summary.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '16px' }}>
      <Text size={500} weight="semibold">Read Mode - AI Assistant</Text>
      <div style={{ marginTop: '16px' }}>
        <Button appearance="primary" onClick={handleSummarize} disabled={loading}>
          {loading ? <Spinner size="tiny" /> : 'Summarize Email'}
        </Button>
      </div>
      
      {summary && (
        <Card style={{ marginTop: '16px' }}>
          <CardHeader header={<Text weight="semibold">Summary</Text>} />
          <CardPreview style={{ padding: '12px' }}>
            <Text>{summary}</Text>
          </CardPreview>
        </Card>
      )}
    </div>
  );
};
