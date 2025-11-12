# Phase 10: Minimal Chat UI with React + Vite - Implementation Plan

**Version:** 1.0  
**Date:** November 12, 2025  
**Status:** Draft  
**Prerequisites:** Phase 1-8 (Python backend with AppAgent) completed

---

## Table of Contents

1. [Overview](#overview)
2. [Step 10.1: Environment Preparation](#step-101-environment-preparation)
3. [Step 10.2: Scaffold UI with Vite](#step-102-scaffold-ui-with-vite)
4. [Step 10.3: Install Dependencies](#step-103-install-dependencies)
5. [Step 10.4: Configure Tailwind CSS](#step-104-configure-tailwind-css)
6. [Step 10.5: Create Environment Configuration](#step-105-create-environment-configuration)
7. [Step 10.6: Implement ChatPage Component](#step-106-implement-chatpage-component)
8. [Step 10.7: Update App Shell](#step-107-update-app-shell)
9. [Step 10.8: Configure Backend CORS](#step-108-configure-backend-cors)
10. [Step 10.9: Test Development Mode](#step-109-test-development-mode)
11. [Step 10.10: Build for Production](#step-1010-build-for-production)
12. [Step 10.11: Verification Checklist](#step-1011-verification-checklist)

---

## Overview

### Implementation Approach

Phase 10 creates a **plain Vite + React + TypeScript frontend** (no Tauri). Each step is self-contained with exact commands, expected output, and verification steps.

### Estimated Timeline

**Total:** 3 hours

| Step | Task | Time |
|------|------|------|
| 10.1 | Environment Preparation | 10 min |
| 10.2 | Scaffold UI with Vite | 15 min |
| 10.3 | Install Dependencies | 20 min |
| 10.4 | Configure Tailwind CSS | 15 min |
| 10.5 | Create Environment Configuration | 10 min |
| 10.6 | Implement ChatPage Component | 60 min |
| 10.7 | Update App Shell | 15 min |
| 10.8 | Configure Backend CORS | 15 min |
| 10.9 | Test Development Mode | 20 min |
| 10.10 | Build for Production | 10 min |
| 10.11 | Verification Checklist | 10 min |

---

## Step 10.1: Environment Preparation

**Goal:** Verify Node.js 25.1.0 and npm 11.6.2 are active

**Commands:**
```bash
# Activate Node 25.1.0 via nvm
nvm use 25

# Verify Node version
node -v
# Expected output: v25.1.0

# Verify npm version
npm -v
# Expected output: 11.6.2

# Navigate to project root
cd "/Users/alessandro/Nuova Baby AI"
pwd
# Expected output: /Users/alessandro/Nuova Baby AI
```

**Verification:**
- ✅ Node version is exactly v25.1.0
- ✅ npm version is exactly 11.6.2
- ✅ Current directory is `/Users/alessandro/Nuova Baby AI/`

**Troubleshooting:**
- If Node version is wrong: `nvm install 25.1.0 && nvm use 25`
- If directory doesn't exist: Verify Phase 1-8 setup is complete

---

## Step 10.2: Scaffold UI with Vite

**Goal:** Create `ui/` directory with Vite + React + TypeScript template

**Commands:**
```bash
# Ensure we're in project root
cd "/Users/alessandro/Nuova Baby AI"

# Create Vite app with React + TypeScript template
npm create vite@latest ui -- --template react-ts

# Navigate into ui directory
cd ui

# Verify structure
ls -la
# Expected: package.json, tsconfig.json, vite.config.ts, src/, public/, index.html
```

**Expected Output:**
```
Scaffolding project in /Users/alessandro/Nuova Baby AI/ui...

Done. Now run:

  cd ui
  npm install
  npm run dev
```

**Verification:**
- ✅ `ui/` directory created
- ✅ `ui/package.json` exists
- ✅ `ui/src/` directory exists with `main.tsx`, `App.tsx`, `index.css`
- ✅ `ui/vite.config.ts` exists

**Project Structure After This Step:**
```
/Users/alessandro/Nuova Baby AI/
├── src/                      # Python backend (Phase 1-8) ✅ EXISTING
│   ├── agents/
│   ├── orchestrator/
│   ├── llm/
│   └── main.py
├── tests/                    # Python tests ✅ EXISTING
├── requirements.txt          # Python deps ✅ EXISTING
└── ui/                       # React frontend (NEW)
    ├── src/
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── index.css
    ├── public/
    ├── index.html
    ├── package.json
    ├── tsconfig.json
    └── vite.config.ts
```

---

## Step 10.3: Install Dependencies

**Goal:** Install all pinned dependencies (runtime + dev)

**Commands:**
```bash
# Ensure we're in ui/
cd "/Users/alessandro/Nuova Baby AI/ui"

# Install runtime dependencies (EXACT versions)
npm install react@19.2.0 react-dom@19.2.0 @tauri-apps/api@2.9.0 zustand@5.0.8 sonner@2.0.7 lucide-react@0.553.0 react-router-dom@7.9.5

# Install dev dependencies (EXACT versions)
npm install -D @types/react@19.2.2 @types/react-dom@19.2.2 @vitejs/plugin-react@5.1.0 @tauri-apps/cli@2.9.4 typescript@5.9.3 vite@7.2.2 tailwindcss@4.1.17 autoprefixer@10.4.22 postcss@8.5.6 clsx@2.1.1 class-variance-authority@0.7.1 tailwind-merge@3.4.0 tailwindcss-animate@1.0.7

# Verify installations
npm list --depth=0
```

**Expected Output:**
```
ui@0.0.0 /Users/alessandro/Nuova Baby AI/ui
├── @tauri-apps/api@2.9.0
├── @tauri-apps/cli@2.9.4
├── @types/react@19.2.2
├── @types/react-dom@19.2.2
├── @vitejs/plugin-react@5.1.0
├── autoprefixer@10.4.22
├── class-variance-authority@0.7.1
├── clsx@2.1.1
├── lucide-react@0.553.0
├── postcss@8.5.6
├── react@19.2.0
├── react-dom@19.2.0
├── react-router-dom@7.9.5
├── sonner@2.0.7
├── tailwind-merge@3.4.0
├── tailwindcss@4.1.17
├── tailwindcss-animate@1.0.7
├── typescript@5.9.3
├── vite@7.2.2
└── zustand@5.0.8
```

**Verification:**
- ✅ All dependencies installed with EXACT versions specified
- ✅ `node_modules/` directory created
- ✅ `package-lock.json` created
- ✅ No version conflicts or warnings

**Note:** `@tauri-apps/api` and `@tauri-apps/cli` are included for Phase 9 but are **NOT used in Phase 10**.

---

## Step 10.4: Configure Tailwind CSS

**Goal:** Set up Tailwind CSS with PostCSS and Autoprefixer

### Step 10.4.1: Initialize Tailwind

**Commands:**
```bash
# Ensure we're in ui/
cd "/Users/alessandro/Nuova Baby AI/ui"

# Initialize Tailwind (creates tailwind.config.js and postcss.config.js)
npx tailwindcss init -p
```

**Expected Output:**
```
Created Tailwind CSS config file: tailwind.config.js
Created PostCSS config file: postcss.config.js
```

### Step 10.4.2: Update tailwind.config.js

**File:** `ui/tailwind.config.js`

**Content:**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Commands:**
```bash
# Overwrite tailwind.config.js with correct content
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF
```

### Step 10.4.3: Update src/index.css

**File:** `ui/src/index.css`

**Content:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Commands:**
```bash
# Overwrite index.css with Tailwind directives
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;
EOF
```

**Verification:**
- ✅ `tailwind.config.js` exists with correct content
- ✅ `postcss.config.js` exists
- ✅ `src/index.css` contains Tailwind directives

---

## Step 10.5: Create Environment Configuration

**Goal:** Create `.env` file with API base URL

**File:** `ui/.env`

**Content:**
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

**Commands:**
```bash
# Ensure we're in ui/
cd "/Users/alessandro/Nuova Baby AI/ui"

# Create .env file
cat > .env << 'EOF'
VITE_API_BASE_URL=http://127.0.0.1:8000
EOF

# Verify
cat .env
```

**Expected Output:**
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

**Verification:**
- ✅ `.env` file exists in `ui/` directory
- ✅ Contains `VITE_API_BASE_URL` variable

---

## Step 10.6: Implement ChatPage Component

**Goal:** Create minimal chat interface with backend integration

**File:** `ui/src/components/ChatPage.tsx`

**Commands:**
```bash
# Ensure we're in ui/
cd "/Users/alessandro/Nuova Baby AI/ui"

# Create components directory
mkdir -p src/components

# Create ChatPage.tsx
cat > src/components/ChatPage.tsx << 'EOF'
import { useState, useEffect, useRef } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'error';
  content: string;
}

export function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Check backend health on mount and every 5 seconds
  useEffect(() => {
    checkBackendStatus();
    const interval = setInterval(checkBackendStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const data = await response.json();
      setIsConnected(data.status === 'healthy');
    } catch (error) {
      setIsConnected(false);
    }
  };

  const sendMessage = async (useStreaming = false) => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      if (useStreaming) {
        // Streaming mode with NDJSON reader
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: userMessage.content,
            stream: true,
          }),
        });

        if (!response.body) throw new Error('No response body');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let assistantContent = '';
        const assistantId = (Date.now() + 1).toString();

        // Add empty assistant message that we'll update
        setMessages((prev) => [
          ...prev,
          { id: assistantId, role: 'assistant', content: '' },
        ]);

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (!line.trim()) continue;

            try {
              const data = JSON.parse(line);

              if (data.type === 'meta') {
                // Handle initial metadata chunk
                if (data.conversation_id) {
                  setConversationId(data.conversation_id);
                }
              } else if (data.type === 'delta') {
                // Handle incremental content chunks
                assistantContent += data.content;
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantId
                      ? { ...msg, content: assistantContent }
                      : msg
                  )
                );
              } else if (data.type === 'final') {
                // Final chunk - message already complete from deltas
                // No action needed, all content already displayed
              }
            } catch (e) {
              console.error('Failed to parse NDJSON line:', line, e);
            }
          }
        }
      } else {
        // Non-streaming mode
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: userMessage.content,
            stream: false,
          }),
        });

        const data = await response.json();

        if (data.conversation_id) {
          setConversationId(data.conversation_id);
        }

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.reply || 'No response from backend',
        };

        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'error',
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header with connection status */}
      <div className="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-200">
        <h1 className="text-xl font-semibold text-gray-900">Baby AI Chat</h1>
        <div className="flex items-center gap-2">
          <div
            className={`w-3 h-3 rounded-full ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            }`}
          />
          <span className="text-sm text-gray-600">
            {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Messages area */}
      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto px-6 py-4 space-y-4"
      >
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg">Welcome to Baby AI!</p>
            <p className="text-sm mt-2">
              Try: "Open Safari" or "Close Safari"
            </p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[70%] rounded-lg px-4 py-2 ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : message.role === 'error'
                  ? 'bg-red-500 text-white'
                  : 'bg-gray-200 text-gray-900'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Input area */}
      <div className="px-6 py-4 bg-white border-t border-gray-200">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message... (Enter to send, Shift+Enter for new line)"
            disabled={isLoading || !isConnected}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
            rows={2}
          />
          <button
            onClick={() => sendMessage(false)}
            disabled={isLoading || !isConnected || !input.trim()}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Backend: {API_BASE_URL}
        </p>
      </div>
    </div>
  );
}
EOF
```

**Verification:**
- ✅ `src/components/ChatPage.tsx` created
- ✅ File contains complete ChatPage component
- ✅ Component uses `VITE_API_BASE_URL` from environment

---

## Step 10.7: Update App Shell

**Goal:** Update App.tsx to render ChatPage

**File:** `ui/src/App.tsx`

**Commands:**
```bash
# Ensure we're in ui/
cd "/Users/alessandro/Nuova Baby AI/ui"

# Overwrite App.tsx
cat > src/App.tsx << 'EOF'
import { ChatPage } from './components/ChatPage';

function App() {
  return <ChatPage />;
}

export default App;
EOF
```

**Verification:**
- ✅ `src/App.tsx` updated to import and render ChatPage
- ✅ No other routes or pages (minimal scope)

---

## Step 10.8: Configure Backend CORS

**Goal:** Ensure Python backend allows CORS from http://localhost:5173

**File:** `/Users/alessandro/Nuova Baby AI/src/main.py` (or wherever FastAPI app is initialized)

**Required Code:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware - MUST allow localhost:5173 for Phase 10 UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Phase 10 Vite dev server
        "http://localhost:1420",  # Phase 9 Tauri dev (future)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Verification Steps:**
```bash
# 1. Check if backend has CORS configured
cd "/Users/alessandro/Nuova Baby AI"
grep -r "CORSMiddleware" src/

# 2. If not found, add CORS middleware to src/main.py
# (Manual step - edit the file to add CORS configuration)

# 3. Restart backend after changes
# python -m src.main
```

**Expected Output:**
- ✅ Backend `src/main.py` includes `CORSMiddleware`
- ✅ `allow_origins` includes `http://localhost:5173`

**Note:** If backend doesn't have CORS configured, Phase 10 UI will fail with CORS errors in browser console.

---

## Step 10.9: Test Development Mode

**Goal:** Run UI dev server and verify integration with backend

### Step 10.9.1: Start Backend

**Commands:**
```bash
# Navigate to project root
cd "/Users/alessandro/Nuova Baby AI"

# Start backend (check existing setup)
python -m src.main

# Or if using uvicorn directly:
# uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verification:**
```bash
# In a new terminal, test backend health
curl http://127.0.0.1:8000/health

# Expected response (if health endpoint exists):
# {"status":"healthy","timestamp":"2025-11-12T10:00:00Z"}
```

### Step 10.9.2: Start UI Dev Server

**Commands:**
```bash
# In a NEW terminal, navigate to ui directory
cd "/Users/alessandro/Nuova Baby AI/ui"

# Ensure Node 25 is active
nvm use 25

# Start Vite dev server
npm run dev
```

**Expected Output:**
```
  VITE v7.2.2  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Verification:**
- ✅ Dev server starts without errors
- ✅ Server runs on http://localhost:5173
- ✅ No TypeScript compilation errors

### Step 10.9.3: Manual Testing in Browser

**Steps:**
1. Open browser to http://localhost:5173
2. Verify UI loads without errors
3. Check connection status badge (should be **green** if backend has /health, **red** if not)
4. Type message: "Open Safari"
5. Click "Send" button
6. Verify response appears in chat
7. Check browser console for errors (should be none if CORS configured)

**Expected Behavior:**
- ✅ UI loads with "Baby AI Chat" header
- ✅ Connection status shows green "Connected" (if /health endpoint exists)
- ✅ Welcome message displays
- ✅ Can type in input field
- ✅ Send button is enabled
- ✅ Message sends successfully
- ✅ Response appears in chat
- ✅ No CORS errors in console

**Troubleshooting:**
- **Connection status red:** Backend not running, no /health endpoint, or CORS not configured
- **CORS errors:** Check backend CORS middleware includes `http://localhost:5173`
- **No response:** Check backend logs for errors or API endpoint mismatch
- **UI doesn't load:** Check Vite dev server is running on port 5173

---

## Step 10.10: Build for Production

**Goal:** Create production build in `ui/dist/` for Phase 9

**Commands:**
```bash
# Ensure we're in ui/
cd "/Users/alessandro/Nuova Baby AI/ui"

# Run production build
npm run build
```

**Expected Output:**
```
vite v7.2.2 building for production...
✓ 150 modules transformed.
dist/index.html                   0.45 kB │ gzip:  0.30 kB
dist/assets/index-[hash].css      8.24 kB │ gzip:  2.15 kB
dist/assets/index-[hash].js     156.78 kB │ gzip: 51.23 kB
✓ built in 2.34s
```

**Verification:**
```bash
# Check dist/ directory exists
ls -la dist/

# Expected files:
# - index.html
# - assets/index-[hash].js
# - assets/index-[hash].css
# - vite.svg (or other public assets)

# Check index.html contains correct asset references
cat dist/index.html | grep "assets/"
```

**Expected Output:**
- ✅ `dist/` directory created
- ✅ `dist/index.html` exists
- ✅ `dist/assets/` directory contains JS and CSS files
- ✅ Build completes without errors
- ✅ No TypeScript errors

**Test Production Build (Optional):**
```bash
# Preview production build locally
npm run preview

# Expected output:
# ➜  Local:   http://localhost:4173/
# Open browser and verify UI works
```

---

## Step 10.11: Verification Checklist

**Goal:** Confirm Phase 10 is complete and ready for Phase 9

### Environment Verification

```bash
# 1. Check Node version
node -v
# ✅ Expected: v25.1.0

# 2. Check npm version
npm -v
# ✅ Expected: 11.6.2

# 3. Check project structure
cd "/Users/alessandro/Nuova Baby AI"
ls -la
# ✅ Expected: src/ and ui/ directories exist
```

### Dependency Verification

```bash
# 4. Check all dependencies installed
cd ui
npm list --depth=0 | grep -E "react@|vite@|typescript@|tailwindcss@|@tauri-apps"
# ✅ Expected: All pinned versions match
```

### Build Verification

```bash
# 5. Type check passes
npm run type-check
# ✅ Expected: No errors

# 6. Build succeeds
npm run build
# ✅ Expected: dist/ created without errors

# 7. Check build output
ls -la dist/
# ✅ Expected: index.html and assets/ directory
```

### Runtime Verification

```bash
# 8. Backend running
cd "/Users/alessandro/Nuova Baby AI"
curl http://127.0.0.1:8000/api/chat -X POST -H "Content-Type: application/json" -d '{"message":"test"}'
# ✅ Expected: JSON response (or CORS error if CORS not configured)

# 9. UI dev server running
cd ui
npm run dev
# In browser: http://localhost:5173
# ✅ Expected: UI loads, shows connection status
```

### Code Quality Verification

```bash
# 10. Check ChatPage component exists
cat src/components/ChatPage.tsx | head -20
# ✅ Expected: Component code visible

# 11. Check environment config
cat .env
# ✅ Expected: VITE_API_BASE_URL=http://127.0.0.1:8000

# 12. Check Tailwind config
cat tailwind.config.js
# ✅ Expected: content includes "./src/**/*.{js,ts,jsx,tsx}"
```

### Integration Verification

```bash
# 13. Check if CORS needs to be added to backend
cd "/Users/alessandro/Nuova Baby AI"
grep -r "CORSMiddleware" src/
# ✅ Expected: CORS middleware found (or manual addition needed)

# 14. Test API endpoint structure
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Open Safari","stream":false}'
# ✅ Expected: JSON response with message field
```

### Phase 9 Readiness Verification

```bash
# 15. Verify dist/ structure for Phase 9
cd "/Users/alessandro/Nuova Baby AI/ui"
ls -la dist/
# ✅ Expected: index.html, assets/ directory

# 16. Check relative paths in dist/index.html
cat dist/index.html | grep -E "href=|src="
# ✅ Expected: Relative paths like "/assets/index-[hash].js"

# 17. Verify dev server port
cat vite.config.ts | grep -A5 "server" || echo "Default port 5173 used"
# ✅ Expected: Default port 5173 (or explicitly set)
```

### Final Checklist

- [ ] Node 25.1.0 and npm 11.6.2 active
- [ ] `ui/` directory created with Vite + React + TypeScript
- [ ] All dependencies installed with exact pinned versions
- [ ] Tailwind CSS configured correctly
- [ ] `.env` file created with `VITE_API_BASE_URL`
- [ ] ChatPage component implemented with all features
- [ ] App.tsx updated to render ChatPage
- [ ] Backend CORS configured for `http://localhost:5173` (or manual addition noted)
- [ ] Dev server runs on http://localhost:5173 without errors
- [ ] UI connects to backend successfully (or shows appropriate status)
- [ ] Can send messages and receive responses (or shows connection issues)
- [ ] Production build succeeds (`npm run build`)
- [ ] `dist/` directory created with correct structure
- [ ] No TypeScript errors (`npm run type-check`)
- [ ] Manual testing checklist attempted
- [ ] Ready for Phase 9 integration

---

## Next Steps

### Commit Phase 10 Code

```bash
# Navigate to project root
cd "/Users/alessandro/Nuova Baby AI"

# Check git status
git status

# Add Phase 10 files
git add ui/

# Commit
git commit -m "Phase 10: Minimal Chat UI with React + Vite

- Scaffolded ui/ with Vite + React 19.2.0 + TypeScript 5.9.3
- Installed all pinned dependencies (Node 25.1.0 compatible)
- Configured Tailwind CSS 4.1.17
- Implemented ChatPage component with backend integration
- Added health check and connection status indicator
- Support for streaming and non-streaming responses
- Production build outputs to ui/dist/ for Phase 9
- Backend CORS ready for localhost:5173

Ready for Phase 9 (Tauri Integration)"

# Push to repository
git push origin main
```

### Proceed to Phase 9

After Phase 10 is complete and committed:

1. **Review Phase 9 Design Document** (to be created)
2. **Begin Phase 9A: Setup & Development Workflow**
   - Install Rust toolchain 1.91.1
   - Install Tauri CLI 2.9.4
   - Create `src-tauri/` directory
   - Configure `tauri.conf.json` to use `ui/` from Phase 10
3. **Continue with Phase 9B: Build & Bundle**
   - Bundle Ollama binaries
   - Bundle Python backend with PyInstaller
   - Create unsigned DMG

---

## Appendix: Common Issues

### Issue: npm install fails with version conflicts

**Symptom:**
```
npm ERR! Could not resolve dependency:
npm ERR! peer react@"^18.0.0" from some-package@x.x.x
```

**Solution:**
1. Verify Node version: `node -v` (must be v25.1.0)
2. Clear npm cache: `npm cache clean --force`
3. Delete `node_modules` and `package-lock.json`
4. Retry with exact versions: `npm install react@19.2.0 react-dom@19.2.0 ...`

### Issue: Vite dev server fails to start

**Symptom:**
```
Error: Port 5173 is already in use
```

**Solution:**
```bash
# Find process using port 5173
lsof -i :5173

# Kill the process
kill -9 <PID>

# Or change port in vite.config.ts
```

### Issue: CORS errors in browser console

**Symptom:**
```
Access to fetch at 'http://127.0.0.1:8000/api/chat' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```

**Solution:**
1. Add CORS middleware to `/Users/alessandro/Nuova Baby AI/src/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
2. Restart backend after adding CORS
3. Clear browser cache and reload

### Issue: Connection status always red

**Symptom:** UI shows "Disconnected" even when backend is running

**Solution:**
1. Verify backend is running: `curl http://127.0.0.1:8000/api/chat -X POST -H "Content-Type: application/json" -d '{"message":"test"}'`
2. Check if backend has `/health` endpoint, or modify ChatPage to use existing endpoint
3. Check `.env` has correct `VITE_API_BASE_URL`
4. Check browser console for network errors
5. Verify CORS is configured correctly

### Issue: TypeScript errors during build

**Symptom:**
```
src/components/ChatPage.tsx:10:5 - error TS2322: Type 'string' is not assignable to type 'number'
```

**Solution:**
1. Run type check: `npm run type-check`
2. Fix type errors in code
3. Verify TypeScript version: `npx tsc --version` (should be 5.9.3)
4. Retry build: `npm run build`

### Issue: Build succeeds but dist/ is empty

**Symptom:** `npm run build` completes but `dist/` directory is missing or empty

**Solution:**
1. Check Vite config: `cat vite.config.ts`
2. Verify `build.outDir` is not set to a different path
3. Check for build errors in output
4. Try clean build: `rm -rf dist && npm run build`

### Issue: UI loads but shows blank page

**Symptom:** Browser shows blank page, no errors in console

**Solution:**
1. Check browser console for JavaScript errors
2. Verify `src/main.tsx` imports and renders App correctly
3. Check `index.html` has `<div id="root"></div>`
4. Verify Vite dev server is running without errors
5. Try hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)

### Issue: Backend not starting

**Symptom:** Cannot connect to http://127.0.0.1:8000

**Solution:**
```bash
# Navigate to project root
cd "/Users/alessandro/Nuova Baby AI"

# Check if backend main exists
ls -la src/main.py

# Start backend manually
python -m src.main

# Or with uvicorn directly
pip install uvicorn
uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload

# Check what's running on port 8000
lsof -i :8000
```

---

**End of Phase 10 Implementation Plan**