# Outlook AI Assistant Add-in

This project is an AI-powered Outlook Add-in designed to assist users while reading and composing emails. It leverages a modern frontend integrated with Microsoft 365, and a robust FastAPI backend connected to an OpenAI-compatible API inference gateway.

## Features

### Read Mode
- **Email Summary**: Concise, detailed, or executive summaries.
- **Thread Summary**: Summarize an entire email conversation thread.
- **Action Items**: Extract tasks, owners, deadlines, and risks from emails.
- **Attachment Summary**: OCR and text extraction for PDF, Word, Excel, PPT, and Images.
- **Priority Detection**: Automatically classify emails as Low, Medium, High, or Urgent.
- **Sentiment Detection**: Analyze the overall sentiment of a message.
- **Suggested Reply**: Generate multiple draft responses based on context.

### Compose Mode
- **Draft Email**: Generate a brand new email from user instructions.
- **Improve Draft**: Rewrite drafts in various tones (Professional, Friendly, Executive, Technical, Concise, Detailed).
- **Rewrite Selection**: Rewrite only highlighted text in the compose window.
- **Grammar Correction & Tone Adjustment**
- **Translation**

## Technology Stack

**Frontend:**
- React 18
- TypeScript
- Fluent UI (React Components v9)
- Office.js
- Zustand (State Management)

**Backend:**
- Python 3
- FastAPI
- Pydantic Settings
- PyTest (Testing)
- PyPDF2, python-docx, pytesseract (Document Extraction)

**Authentication:**
- MSAL
- Azure AD (SSO & On-Behalf-Of Flow)
- Microsoft Graph API

## Setup Instructions

### Prerequisites
- Node.js (v16+)
- Python (v3.10+)
- An Azure AD Application (Client ID, Client Secret, Tenant ID)
- An AI Provider (OpenAI, vLLM, NIM, Ollama)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in `.env`:
   ```env
   CLIENT_ID=your-client-id
   CLIENT_SECRET=your-client-secret
   TENANT_ID=common
   OPENAI_API_KEY=your-key
   OPENAI_API_BASE=https://api.openai.com/v1
   PRIMARY_MODEL=gpt-4
   ```
4. Run the API:
   ```bash
   PYTHONPATH=src uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server (command varies by bundler):
   ```bash
   npm run build
   ```
4. Load the `manifest.xml` into your Outlook client to test the Add-in natively.

## Architecture

Please review `ARCHITECTURE.md` for a detailed breakdown of the high-level infrastructure, SOLID design principles, and module structures utilized throughout this repository.
