import React, { useState } from 'react';
import { Button, Spinner, Text, Textarea, Field } from '@fluentui/react-components';
import { AIClient } from '../services/aiClient';
import { useAppStore } from '../store/useAppStore';

export const ComposeMode: React.FC = () => {
  const [instructions, setInstructions] = useState('');
  const [draft, setDraft] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { setError } = useAppStore();

  const handleDraft = async () => {
    if (!instructions) return;
    setLoading(true);
    setError(null);
    try {
      const res = await AIClient.generateDraft(instructions, "professional");
      setDraft(res.text);
    } catch (err: any) {
      setError(err.message || "Failed to generate draft.");
    } finally {
      setLoading(false);
    }
  };

  const insertDraft = () => {
    if (draft && Office.context.mailbox.item) {
      Office.context.mailbox.item.body.setSelectedDataAsync(
        draft,
        { coercionType: Office.CoercionType.Html },
        (result) => {
          if (result.status === Office.AsyncResultStatus.Failed) {
            setError(result.error.message);
          }
        }
      );
    }
  };

  return (
    <div style={{ padding: '16px' }}>
      <Text size={500} weight="semibold">Compose Mode - AI Assistant</Text>
      <Field label="Instructions" style={{ marginTop: '16px', marginBottom: '16px' }}>
        <Textarea 
          placeholder="e.g. Write an email to the team asking for Q3 reports."
          value={instructions}
          onChange={(e, data) => setInstructions(data.value)}
        />
      </Field>
      
      <Button appearance="primary" onClick={handleDraft} disabled={loading || !instructions}>
        {loading ? <Spinner size="tiny" /> : 'Generate Draft'}
      </Button>

      {draft && (
        <div style={{ marginTop: '24px' }}>
          <Text weight="semibold">Generated Draft:</Text>
          <div style={{ padding: '12px', backgroundColor: '#f3f2f1', marginTop: '8px', marginBottom: '8px' }}>
            {draft}
          </div>
          <Button onClick={insertDraft}>Insert into Email</Button>
        </div>
      )}
    </div>
  );
};
