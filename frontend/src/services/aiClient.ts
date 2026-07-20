import { apiClient } from './api';

export const AIClient = {
  getSummary: async (messageId: string, summaryType: string = "concise") => {
    const res = await apiClient.post('/summary', { message_id: messageId, summary_type: summaryType });
    return res.data;
  },
  
  extractActions: async (messageId: string) => {
    const res = await apiClient.post('/extract-actions', { message_id: messageId });
    return res.data;
  },
  
  classifyPriority: async (messageId: string) => {
    const res = await apiClient.post('/classify-priority', { message_id: messageId });
    return res.data;
  },
  
  generateDraft: async (instructions: string, tone: string = "professional") => {
    const res = await apiClient.post('/draft', { instructions, tone });
    return res.data;
  },
  
  rewriteText: async (selectedText: string, tone: string = "professional") => {
    const res = await apiClient.post('/rewrite', { selected_text: selectedText, tone });
    return res.data;
  }
};
