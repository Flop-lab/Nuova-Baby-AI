# Phase 10: Minimal Chat UI with React + Vite - Design Document

**Version:** 1.0  
**Date:** November 12, 2025  
**Status:** Draft  
**Prerequisites:** Phase 1-8 (Python backend with AppAgent) completed

---

## Table of Contents

1. [Overview](#overview)
2. [Goals & Scope](#goals--scope)
3. [Architecture](#architecture)
4. [Dependencies (Pinned Versions)](#dependencies-pinned-versions)
5. [API Contract with Backend](#api-contract-with-backend)
6. [UI Components & UX Spec](#ui-components--ux-spec)
7. [Development Workflow](#development-workflow)
8. [Build Output & Handoff to Phase 9](#build-output--handoff-to-phase-9)
9. [Success Criteria](#success-criteria)

---

## Overview

### Purpose

Phase 10 creates a **minimal React + TypeScript + Vite frontend** that provides a chat interface for testing the Python backend (Phase 1-8). This is a **UI-only phase** - no Tauri, no desktop wrapper, no binary bundling. Phase 9 will later wrap this UI with Tauri to create the standalone desktop app.

### What Phase 10 Delivers

- ✅ React 19.2.0 + TypeScript 5.9.3 + Vite 7.2.2 frontend
- ✅ Minimal ChatPage component with message input/output
- ✅ Connection status indicator (backend health check)
- ✅ Support for both streaming and non-streaming responses
- ✅ Tailwind CSS 4.1.17 for styling
- ✅ Dev server running on http://localhost:5173
- ✅ Production build output in `ui/dist/` for Phase 9 bundling

### What Phase 10 Does NOT Include

- ❌ NO Tauri wrapper (that's Phase 9)
- ❌ NO Rust code or src-tauri/ directory (that's Phase 9)
- ❌ NO desktop app features (that's Phase 9)
- ❌ NO Ollama bundling (that's Phase 9)
- ❌ NO PyInstaller backend bundling (that's Phase 9)

---

## Goals & Scope

### Primary Goals

1. **Minimal Chat Interface:** Single ChatPage component for testing backend
2. **Backend Integration:** Connect to Python FastAPI backend on http://127.0.0.1:8000
3. **Health Monitoring:** Visual indicator showing backend connection status
4. **Message Exchange:** Send user messages, receive assistant responses
5. **Streaming Support:** Handle both regular and streaming (NDJSON) responses
6. **Clean Build:** Produce `ui/dist/` that Phase 9 can bundle into Tauri app

### Out of Scope for Phase 10

- Multiple pages/routes (only ChatPage)
- User authentication
- Settings/preferences UI
- File uploads
- Voice input
- Advanced markdown rendering
- Code syntax highlighting
- Message editing/deletion
- Conversation history persistence

---

## Architecture

### Project Structure

```
/Users/alessandro/Nuova Baby AI/
├── src/                      # Python backend (Phase 1-8) ✅ EXISTING
│   ├── agents/
│   │   └── app_agent.py
│   ├── orchestrator/
│   │   └── orchestrator.py
│   ├── llm/
│   │   └── ollama_adapter.py
│   └── main.py
├── tests/                    # Python tests ✅ EXISTING
├── requirements.txt          # Python deps ✅ EXISTING
└── ui/                       # React frontend (Phase 10) ← NEW
    ├── src/
    │   ├── components/
    │   │   └── ChatPage.tsx
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── index.css
    ├── public/
    ├── index.html
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── tailwind.config.js
    ├── postcss.config.js
    └── .env              # VITE_API_BASE_URL
```

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Runtime** | Node.js | 25.1.0 | JavaScript runtime |
| **Package Manager** | npm | 11.6.2 | Dependency management |
| **Framework** | React | 19.2.0 | UI framework |
| **Language** | TypeScript | 5.9.3 | Type safety |
| **Build Tool** | Vite | 7.2.2 | Dev server + bundler |
| **Styling** | Tailwind CSS | 4.1.17 | Utility-first CSS |
| **State** | Zustand | 5.0.8 | Lightweight state management |
| **Notifications** | Sonner | 2.0.7 | Toast notifications |
| **Icons** | Lucide React | 0.553.0 | Icon library |
| **Routing** | React Router DOM | 7.9.5 | Client-side routing |

### Data Flow

```
User Input (ChatPage)
    ↓
HTTP POST /api/chat
    ↓
Python Backend (FastAPI) - /Users/alessandro/Nuova Baby AI/src/main.py
    ↓
Orchestrator → AppAgent
    ↓
Response (JSON or NDJSON stream)
    ↓
ChatPage (display message)
```

---

## Dependencies (Pinned Versions)

### Runtime Dependencies

```json
{
  "react": "19.2.0",
  "react-dom": "19.2.0",
  "@tauri-apps/api": "2.9.0",
  "zustand": "5.0.8",
  "sonner": "2.0.7",
  "lucide-react": "0.553.0",
  "react-router-dom": "7.9.5"
}
```

**Note:** `@tauri-apps/api` is included for future Phase 9 integration but is **NOT used in Phase 10**. The UI runs in a regular browser during development.

### Dev Dependencies

```json
{
  "@types/react": "19.2.2",
  "@types/react-dom": "19.2.2",
  "@vitejs/plugin-react": "5.1.0",
  "@tauri-apps/cli": "2.9.4",
  "typescript": "5.9.3",
  "vite": "7.2.2",
  "tailwindcss": "4.1.17",
  "autoprefixer": "10.4.22",
  "postcss": "8.5.6",
  "clsx": "2.1.1",
  "class-variance-authority": "0.7.1",
  "tailwind-merge": "3.4.0",
  "tailwindcss-animate": "1.0.7"
}
```

**Note:** `@tauri-apps/cli` is included for future Phase 9 integration but is **NOT used in Phase 10**.

### Version Compatibility

All versions have been verified to work with:
- **Node.js 25.1.0**
- **npm 11.6.2**
- **macOS** (Apple Silicon + Intel)

**⚠️ IMPORTANT:** Do NOT change these versions without explicit approval. They have been tested and verified compatible.

---

## API Contract with Backend

### Backend Endpoints

Phase 10 UI expects the following endpoints from the Python backend:

#### 1. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-12T10:00:00Z"
}
```

**Purpose:** UI displays connection status indicator (green = healthy, red = unhealthy)

#### 2. Chat (Non-Streaming)

**Endpoint:** `POST /api/chat`

**Request:**
```json
{
  "message": "Open Safari",
  "stream": false
}
```

**Response:**
```json
{
  "reply": "I've opened Safari for you.",
  "conversation_id": "uuid",
  "step_id": "uuid",
  "trace": null
}
```

#### 3. Chat (Streaming)

**Endpoint:** `POST /api/chat`

**Request:**
```json
{
  "message": "Open Safari",
  "stream": true
}
```

**Response:** NDJSON stream (newline-delimited JSON)
```
{"type":"meta","conversation_id":"uuid","step_id":"uuid"}
{"type":"delta","content":"I"}
{"type":"delta","content":"'"}
{"type":"delta","content":"v"}
{"type":"delta","content":"e"}
{"type":"delta","content":" "}
{"type":"delta","content":"o"}
{"type":"delta","content":"p"}
{"type":"delta","content":"e"}
{"type":"delta","content":"n"}
{"type":"delta","content":"e"}
{"type":"delta","content":"d"}
{"type":"delta","content":" "}
{"type":"delta","content":"S"}
{"type":"delta","content":"a"}
{"type":"delta","content":"f"}
{"type":"delta","content":"a"}
{"type":"delta","content":"r"}
{"type":"delta","content":"i"}
{"type":"final","message":"I've opened Safari for you."}
```

### CORS Requirements

**⚠️ NOTE:** CORS is **ONLY needed for Phase 10 development**. In Phase 9 (Tauri desktop app), the UI and backend will run inside the same app bundle, so CORS will not be needed and should be removed or restricted.

The Python backend **MUST** allow CORS from:
- `http://localhost:5173` (Vite dev server - Phase 10 only)

**Backend CORS Configuration:**
```python
# /Users/alessandro/Nuova Baby AI/src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## UI Components & UX Spec

### ChatPage Component

**File:** `ui/src/components/ChatPage.tsx`

**Features:**
1. **Connection Status Badge**
   - Green: Backend healthy
   - Red: Backend unreachable
   - Updates every 5 seconds

2. **Message List**
   - User messages (right-aligned, blue background)
   - Assistant messages (left-aligned, gray background)
   - Error messages (red background)
   - Auto-scroll to bottom on new message

3. **Input Area**
   - Text input field
   - Send button (disabled when loading)
   - Enter key to send
   - Shift+Enter for new line

4. **Loading State**
   - Disabled input during message processing
   - Loading spinner on send button

### Visual Design

**Color Scheme:**
- Background: `bg-gray-50`
- User messages: `bg-blue-500 text-white`
- Assistant messages: `bg-gray-200 text-gray-900`
- Error messages: `bg-red-500 text-white`
- Connection badge (healthy): `bg-green-500`
- Connection badge (unhealthy): `bg-red-500`

**Typography:**
- Font: System default (sans-serif)
- Message text: `text-sm`
- Input text: `text-base`

**Layout:**
- Full viewport height
- Fixed header with connection status
- Scrollable message area
- Fixed footer with input

---

## Development Workflow

### Environment Setup

1. **Node.js 25.1.0** installed via nvm
2. **npm 11.6.2** (comes with Node 25.1.0)
3. **Python backend** running on http://127.0.0.1:8000

### Development Commands

```bash
# Navigate to project root
cd "/Users/alessandro/Nuova Baby AI"

# Start dev server (runs on http://localhost:5173)
cd ui && npm run dev

# Build for production (outputs to ui/dist/)
npm run build

# Preview production build
npm run preview

# Type check
npm run type-check

# Lint (if configured)
npm run lint
```

### Environment Variables

**File:** `ui/.env`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

**Usage in code:**
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
```

### Development Testing

**Manual Test Checklist:**
1. ✅ Backend running on port 8000
2. ✅ UI dev server running on port 5173
3. ✅ Connection status shows green
4. ✅ Send message "Open Safari"
5. ✅ Receive response from backend
6. ✅ Message appears in chat
7. ✅ Try streaming mode (if backend supports)
8. ✅ Stop backend → connection status turns red
9. ✅ Restart backend → connection status turns green

---

## Build Output & Handoff to Phase 9

### Production Build

**Command:** `npm run build`

**Output Directory:** `ui/dist/`

**Expected Files:**
```
ui/dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── [other assets]
└── vite.svg (or other public assets)
```

### Phase 9 Integration Points

Phase 9 (Tauri Integration) will consume Phase 10's output as follows:

1. **Development Mode:**
   - Tauri's `devUrl` points to `http://localhost:5173`
   - UI dev server must be running
   - Backend runs on port 8000

2. **Production Build:**
   - Tauri's `frontendDist` points to `../ui/dist`
   - Tauri bundles `ui/dist/` into the app
   - Backend is bundled with PyInstaller

**Phase 9 tauri.conf.json (preview):**
```json
{
  "build": {
    "devUrl": "http://localhost:5173",
    "frontendDist": "../ui/dist"
  }
}
```

---

## Success Criteria

### Phase 10 is complete when:

1. ✅ **UI Scaffolded:** `ui/` directory created with Vite + React + TypeScript
2. ✅ **Dependencies Installed:** All pinned versions installed correctly
3. ✅ **ChatPage Implemented:** Minimal chat interface with all features
4. ✅ **Backend Integration:** Successfully connects to backend on port 8000
5. ✅ **Health Check Works:** Connection status indicator updates correctly
6. ✅ **Message Exchange Works:** Can send messages and receive responses
7. ✅ **Streaming Works:** NDJSON streaming responses display correctly (if backend supports)
8. ✅ **Build Succeeds:** `npm run build` produces `ui/dist/` without errors
9. ✅ **Manual Testing Passes:** All items in development testing checklist pass
10. ✅ **Ready for Phase 9:** Output structure matches Phase 9 expectations

### Verification Commands

```bash
# 1. Check Node version
node -v  # Should show v25.1.0

# 2. Check npm version
npm -v   # Should show 11.6.2

# 3. Navigate to project
cd "/Users/alessandro/Nuova Baby AI"

# 4. Install dependencies
cd ui && npm install

# 5. Type check
npm run type-check  # Should pass with no errors

# 6. Build
npm run build  # Should succeed

# 7. Check build output
ls -la dist/  # Should contain index.html and assets/

# 8. Start dev server
npm run dev  # Should start on http://localhost:5173

# 9. Test with backend
# (Backend must be running on http://127.0.0.1:8000)
# Open http://localhost:5173 in browser
# Send test message "Open Safari"
# Verify response appears
```

---

## Next Steps

After Phase 10 is complete:

1. **Commit Phase 10 code** to git
2. **Proceed to Phase 9** (Tauri Integration & Binary Management)
3. Phase 9 will:
   - Install Rust + Tauri CLI
   - Create `src-tauri/` directory
   - Configure Tauri to use `ui/` from Phase 10
   - Bundle Ollama + Python backend
   - Create unsigned DMG for testing

---

## Appendix: Troubleshooting

### Issue: CORS errors in browser console

**Symptom:** `Access-Control-Allow-Origin` errors when calling backend

**Solution:** Ensure Python backend has CORS middleware configured for `http://localhost:5173`

```python
# In /Users/alessandro/Nuova Baby AI/src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Connection status always red

**Symptom:** UI shows "Backend Unreachable" even when backend is running

**Solution:**
1. Check backend is running: `curl http://127.0.0.1:8000/health`
2. Check CORS is configured correctly
3. Check browser console for errors

### Issue: npm install fails

**Symptom:** Dependency installation errors

**Solution:**
1. Verify Node version: `node -v` (should be v25.1.0)
2. Clear npm cache: `npm cache clean --force`
3. Delete `node_modules` and `package-lock.json`
4. Retry: `npm install`

### Issue: Build fails with TypeScript errors

**Symptom:** `npm run build` fails with type errors

**Solution:**
1. Check TypeScript version: `npx tsc --version` (should be 5.9.3)
2. Run type check: `npm run type-check`
3. Fix type errors in code
4. Retry build

### Issue: Vite dev server won't start

**Symptom:** `npm run dev` fails or port 5173 is in use

**Solution:**
1. Check if port 5173 is in use: `lsof -i :5173`
2. Kill process using port: `kill -9 <PID>`
3. Or change port in `vite.config.ts`: `server: { port: 5174 }`

### Issue: Backend not starting

**Symptom:** Cannot connect to http://127.0.0.1:8000

**Solution:**
```bash
# Navigate to project root
cd "/Users/alessandro/Nuova Baby AI"

# Start backend manually
python -m src.main

# Or with uvicorn
uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

---

**End of Phase 10 Design Document**