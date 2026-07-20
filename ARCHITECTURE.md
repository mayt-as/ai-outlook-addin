# Outlook AI Add-in Architecture

## 1. Requirements Analysis
**Goal**: Assist users reading and composing emails using AI across Outlook Desktop, Web, and Microsoft 365.
**Backend**: FastAPI, handling AI inference requests to an OpenAI-compatible API (supporting primary/fallback routing).
**Frontend**: React, TypeScript, Fluent UI, Office.js, Zustand for state management.
**Auth**: Office SSO -> FastAPI (MSAL OBO) -> Microsoft Graph.
**Scale**: Architected to support >100,000 LOC, ensuring SOLID principles, modularity, strict typing, and high testability.

## 2. High-Level Architecture
```
[Outlook Client (Desktop/Web/M365)]
       |
       | (Office.js SSO Token via Context)
       v
[Frontend Taskpane (React + TS + FluentUI)] -> State: Zustand
       |
       | HTTPS + SSO Token
       v
[Backend API (FastAPI)] -> Middleware (Auth, Logging, Correlation, Errors)
       |
       |-- (Auth Service) -> Exhange SSO for Graph Token (MSAL OBO)
       |-- (Graph Service) -> Fetch Email, Thread, Attachments via Graph API
       |-- (Document Processing) -> Extract Text (PDF, Word, Excel, PPT, Image OCR)
       |
       |-- (Prompt Management) -> Load File-based Prompts (YAML/JSON)
       |-- (AI Provider Interface) -> OpenAICompatibleProvider (Primary + Fallback)
       v
[OpenAI-Compatible Inference Server] (e.g. vLLM, NIM, Ollama)
```

## 3. Folder Structure
```text
.
├── backend/
│   ├── src/
│   │   ├── main.py                     # Entry point
│   │   ├── api/
│   │   │   ├── routers/                # FastAPI routers (Read, Compose, Health)
│   │   │   ├── dependencies/           # FastAPI dependency injections (Auth, DB, etc.)
│   │   │   └── middleware/             # Logging, Error handling, Auth
│   │   ├── core/
│   │   │   ├── config.py               # Pydantic Settings
│   │   │   ├── exceptions.py           # Custom exceptions
│   │   │   └── logging.py              # Structured logging (Correlation IDs)
│   │   ├── domain/
│   │   │   ├── dtos/                   # Data Transfer Objects
│   │   │   └── models/                 # Domain entities
│   │   ├── services/
│   │   │   ├── ai/                     # AI interface & OpenAICompatibleProvider
│   │   │   ├── auth/                   # MSAL OBO flow
│   │   │   ├── graph/                  # Graph API client
│   │   │   ├── documents/              # Extraction (PDF, Word, etc.)
│   │   │   └── business/               # Core logic (Summaries, Drafts, etc.)
│   │   ├── prompts/                    # Folder for YAML/JSON prompt definitions
│   │   └── utils/                      # Helper functions
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/                 # Reusable Fluent UI components
│   │   ├── hooks/                      # Custom React hooks
│   │   ├── pages/                      # Page level components (Read, Compose)
│   │   ├── services/                   # API clients, Office.js wrappers
│   │   ├── store/                      # Zustand state management
│   │   ├── types/                      # TypeScript definitions
│   │   ├── utils/                      # Helper functions
│   │   └── index.tsx                   # App entry
│   ├── public/
│   │   └── assets/                     # Icons, etc.
│   ├── manifest.xml                    # Office Add-in Manifest
│   ├── package.json
│   └── tsconfig.json
```

## 4. Identified Modules

### Backend Modules
1. **Core Infrastructure**: Configuration, logging, exception handling, and middleware.
2. **AI & Prompts**: `OpenAICompatibleProvider`, prompt loading from files, fallback logic.
3. **Authentication & Graph API**: MSAL OBO token exchange, Graph API interactions (fetching emails/attachments).
4. **Document Processing**: Modules to parse PDFs (`PyPDF2`), Word documents (`python-docx`), Excel (`openpyxl`), PPT, and Images (`pytesseract`).
5. **Business Logic & Routers**: Implementing endpoints (`/summary`, `/reply`, `/rewrite`, etc.) and tying everything together.

### Frontend Modules
1. **State Management**: Zustand store setup.
2. **Authentication & API**: Office SSO integration, Axios client with interceptors.
3. **UI Components**: Fluent UI wrappers, generic UI elements.
4. **Taskpane Pages**: Compose mode and Read mode views.
5. **Office.js Integration**: Functions for interacting with Outlook.

## 5. Identified Interfaces (Key abstractions)

**Backend:**
- `IAIProvider`: Interface defining `generate_text`, `generate_structured_data`.
- `IDocumentExtractor`: Interface defining `extract_text(file_bytes)`.
- `IGraphService`: Interface defining `get_message(id)`, `get_attachments(id)`.

**Frontend:**
- `ApiClient`: Interface for communicating with the backend.
- `OutlookService`: Interface wrapping Office.js commands.

## 6. Implementation Plan
We will build one module at a time.
1. Define Architecture and Project Structure (Completed here).
2. Initialize Project Scaffolding.
3. Build Backend Module: Core Infrastructure.
4. Build Backend Module: Prompt Management and AI Provider.
5. Build Backend Module: Authentication and Graph API.
6. Build Backend Module: Document Processing (Attachments).
7. Build Backend Module: Business Logic and Routers.
8. Build Frontend Module: Setup and State Management.
9. Build Frontend Module: Authentication and API Client.
10. Build Frontend Module: UI Components and Taskpanes.
11. Build Frontend Module: Office.js Integration and Manifest.
