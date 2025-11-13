# Baby AI - Phase 1.1 POC

Python rewrite of Baby AI with multi-agent architecture. Phase 1.1 implements the App Agent for macOS application control.

## ⚠️ DEPENDENCY MANAGEMENT

**CRITICAL:** This project uses **pinned dependencies** for stability. Do NOT modify versions without approval.

### Setup Instructions (EXACT STEPS)

1. **Use exact Python version**
```bash
python3.14 -m venv venv
source venv/bin/activate
```

2. **Install EXACT dependency versions**
```bash
# Option 1: Install from requirements.txt (flexible versions)
pip install -r requirements.txt

# Option 2: Install from requirements-lock.txt (EXACT versions - RECOMMENDED)
pip install -r requirements-lock.txt
```

3. **Verify installation**
```bash
python -c "import ollama, fastapi, pydantic; print('✅ Dependencies OK')"
```

### 🚨 Dependency Rules

- **DO NOT** run `pip install <package>` without updating requirements.txt
- **DO NOT** change versions in requirements.txt without testing
- **DO NOT** add new dependencies without discussion
- **ALWAYS** use `pip freeze > requirements-lock.txt` after changes
- **TEST** thoroughly after any dependency changes

### Adding New Dependencies

1. Add to `requirements.txt` with pinned version
2. Install: `pip install -r requirements.txt`  
3. Update lock file: `pip freeze > requirements-lock.txt`
4. Test: `python -m pytest tests/`
5. Commit both files

## Architecture

For detailed architecture diagrams and technical specifications, see:
- **[PHASE_1.1_DESIGN_DOCUMENT.md](./PHASE_1.1_DESIGN_DOCUMENT.md)** - Complete system architecture with visual diagrams
- **[AGENT_CAPABILITIES.md](./AGENT_CAPABILITIES.md)** - Unique agent capabilities and what Baby AI can do differently

The design document includes:
- High-level architecture flow (User Input → FastAPI → Pydantic AI → LLM → App Agent → macOS)
- Tauri desktop architecture 
- Component specifications and interactions

The agent capabilities document explains:
- What Baby AI can do differently compared to other AI assistants
- Detailed capabilities of AppAgent (10 functions) and BrowserAgent (15 functions)
- Multi-agent orchestration system
- Comparisons with ChatGPT, Apple Shortcuts, and Selenium

## Prerequisites

- **Operating System:** macOS (required for Appscript automation)
- **Python:** 3.14.0 
- **Ollama:** v0.12.10 server (for local LLM inference)

### Install Ollama

```bash
# Download and install Ollama from https://ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the Mistral 7B model
ollama pull mistral:7b-instruct-v0.3-q4_K_M
```

## Quick Start

1. **Clone and setup**
```bash
git clone https://github.com/Flop-lab/Nuova-Baby-AI.git
cd "Nuova Baby AI"
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements-lock.txt
```

2. **Start Ollama server**
```bash
ollama serve
```

3. **Start Baby AI server**
```bash
python -m src.main
```

4. **Test the API**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "open TextEdit"}'
```

## Usage Examples

### Basic App Control
```bash
# Open an application
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "open Safari"}'

# Close an application  
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "close Safari"}'
```

### Streaming Mode
```bash
# Get streaming response
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "open TextEdit", "stream": true}'
```

## API Documentation

### Endpoint: `POST /api/chat`

**Request Body:**
```json
{
  "message": "string (required) - Natural language command",
  "conversation_id": "string (optional) - For conversation tracking", 
  "stream": "boolean (optional) - Enable streaming response"
}
```

**Response (Non-streaming):**
```json
{
  "response": "string - Natural language response",
  "conversation_id": "string - Conversation identifier",
  "success": "boolean - Operation success status"
}
```

**Response (Streaming):**
NDJSON chunks with partial responses.

## Testing

### Run Unit Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Results (Phase 6)
- **Total Tests:** 17/17 ✅
- **Coverage:** 44%
- **Status:** All tests passing

## Development

### Project Structure
```
src/
├── main.py              # FastAPI server entry point
├── agents/              # Domain agents (App Agent)
├── llm/                 # LLM client and adapters  
├── models/              # Pydantic schemas and config
├── orchestrator/        # Pydantic AI orchestrator
└── utils/               # Utilities and logging
```

### Development Workflow

<!-- TODO: Add development guidelines -->

## Troubleshooting

### Common Issues

**Ollama Connection Error:**
- Ensure Ollama server is running: `ollama serve`
- Check if model is available: `ollama list`

**Permission Denied (macOS):**
- Grant accessibility permissions to Terminal/IDE
- System Preferences → Privacy & Security → Accessibility

**Import Errors:**
- Verify Python version: `python --version` (should be 3.14.0)
- Reinstall dependencies: `pip install -r requirements-lock.txt`

## Project Status

**Current Phase:** 1.1 - App Agent POC  
**Status:** Development Complete, Testing in Progress

### Completed Features
- ✅ FastAPI backend with Pydantic AI orchestrator
- ✅ Ollama LLM integration (Mistral 7B)
- ✅ App Agent for macOS application control
- ✅ JSON validation and error handling
- ✅ Streaming response support
- ✅ Conversation tracking
- ✅ Comprehensive test suite (17 tests)

### Current Limitations
- **Single Domain:** Only App Agent implemented (open/close apps)
- **macOS Only:** Requires Appscript for system automation
- **Local LLM:** Uses Ollama/Mistral (no cloud LLM support yet)

### Next Phases
- **Phase 2:** Additional domain agents (File, Web, System, etc.)
- **Phase 3:** Cloud LLM adapters (Gemini, Claude)
- **Phase 4:** Tauri desktop application
- **Phase 5:** Multi-platform support

## License

<!-- TODO: Add license information -->

## Contributing

<!-- TODO: Add contributing guidelines -->

```
