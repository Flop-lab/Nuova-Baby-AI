# Phase 9 Document - Fixes Required

## 🚨 Percorsi da Correggere

### Sostituire Tutti i Percorsi

**SBAGLIATO nel documento:**
```bash
cd /path/to/Baby-AI/baby-ai-python
Baby-AI/baby-ai-python/
```

**CORRETTO per il tuo progetto:**
```bash
cd "/Users/alessandro/Nuova Baby AI"
/Users/alessandro/Nuova Baby AI/
```

## 🔧 Struttura Directory Corretta

### Attuale (Phase 1-8 completata)
```
/Users/alessandro/Nuova Baby AI/
├── src/                    # Backend Python esistente
│   ├── agents/
│   │   └── app_agent.py
│   ├── orchestrator/
│   ├── models/
│   └── main.py
├── tests/                  # Test esistenti
├── requirements.txt        # Dipendenze esistenti
└── [docs files]
```

### Target (dopo Phase 9A setup)
```
/Users/alessandro/Nuova Baby AI/
├── backend/               # NUOVO: sposta src/ qui
│   ├── src/              # Backend Python esistente
│   ├── backend_entry.py  # NUOVO: PyInstaller entry
│   └── pyinstaller.spec  # NUOVO: Build config
├── ui/                   # Da Phase 10
│   └── dist/            # Build output
├── src-tauri/           # NUOVO: Tauri wrapper
│   ├── src/
│   │   ├── main.rs
│   │   └── backend_manager.rs
│   ├── binaries/        # NUOVO: Ollama binaries
│   │   ├── ollama-darwin-arm64
│   │   └── ollama-darwin-amd64
│   └── tauri.conf.json
└── scripts/            # NUOVO: Helper scripts
    └── fetch_ollama.sh
```

## 🔗 Fix Versioni (Allineamento)

### Tuo Sistema (da verificare)
- ✅ Python 3.14.0 (confermato)
- ✅ Node.js 25.1.0 (confermato)
- ✅ npm 11.6.2 (confermato)
- 📋 Rust: da installare
- 📋 Tauri CLI: da installare

### Fix nel Documento
```toml
# rust-toolchain.toml
[toolchain]
channel = "1.91.1"  # ✅ Corretto
```

```bash
# Install Tauri CLI
cargo install tauri-cli --version "^2.9"  # Fix: era 2.5
```

## 🗂 SHA256 Checksums da Ottenere

Il documento ha placeholder:
```bash
ARM64_SHA256="REPLACE_WITH_ACTUAL_SHA256_FOR_ARM64"  # ❌
AMD64_SHA256="REPLACE_WITH_ACTUAL_SHA256_FOR_AMD64"  # ❌
```

**Action Required:**
1. Vai su https://github.com/ollama/ollama/releases/tag/v0.12.10
2. Scarica checksums file
3. Trova i SHA256 per:
   - `ollama-darwin-arm64`
   - `ollama-darwin-amd64`

## 📦 Bundle Strategy (Corretto nel Documento)

Il documento è **corretto** per il bundling:

### Development Mode
```bash
cargo tauri dev
# → Usa Ollama sistema se disponibile
# → Usa Python dev environment
```

### Production Build
```bash
cargo tauri build
# → Crea DMG con tutto incluso:
#   ✅ Ollama binaries (arm64 + x86_64)
#   ✅ Python backend (PyInstaller)
#   ✅ React UI (built assets)
#   ✅ Tauri wrapper (Rust)
```

### DMG Finale
```
Baby AI.app/
├── Contents/
│   ├── MacOS/
│   │   └── Baby AI          # Tauri executable
│   └── Resources/
│       ├── ollama-darwin-*   # Ollama binaries
│       └── backend/          # Python backend
```

## 🎯 User Experience Target

**Installazione Utente (Goal):**
1. Scarica `Baby AI.dmg`
2. Drag & drop in Applications
3. Launch app
4. App auto-scarica solo il modello (es. Qwen)
5. Ready to use!

**NO installation requirements:**
- ❌ NO "install Python"
- ❌ NO "install Ollama"
- ❌ NO "install Node.js"
- ❌ NO terminal commands

## 🔧 Immediate Actions

### 1. Fix Percorsi nel Documento
```bash
# Search & replace globally:
"Baby-AI/baby-ai-python" → "/Users/alessandro/Nuova Baby AI"
"/path/to/Baby-AI" → "/Users/alessandro"
```

### 2. Verifica Versioni Sistema
```bash
cd "/Users/alessandro/Nuova Baby AI"

# Check current tools
python3 --version    # Should be 3.14.0
node --version       # Should be v25.1.0
npm --version        # Should be 11.6.2

# Install missing tools
rustup --version     # Install if missing
cargo --version      # Install if missing
```

### 3. Get Real SHA256s
```bash
# Download and verify checksums from Ollama releases
curl -L https://github.com/ollama/ollama/releases/download/v0.12.10/ollama-darwin-arm64 -o /tmp/ollama-arm64
curl -L https://github.com/ollama/ollama/releases/download/v0.12.10/ollama-darwin-amd64 -o /tmp/ollama-amd64

shasum -a 256 /tmp/ollama-arm64
shasum -a 256 /tmp/ollama-amd64
```

## ✅ Document Validation

Il documento Phase 9 è **conceptually sound** per:
- ✅ Bundling strategy (Ollama + Python + UI)
- ✅ Tauri 2.x architecture
- ✅ DMG creation process
- ✅ Development vs Production workflows
- ✅ Auto-startup of services

**Solo i dettagli specifici del tuo progetto vanno sistemati.**