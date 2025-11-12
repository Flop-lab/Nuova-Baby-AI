# Phase 9: Tauri Integration & Binary Management - Corrected for Nuova Baby AI

**Version:** 1.1 (Corrected)  
**Date:** 12 novembre 2025  
**Target:** Phase 1.1 POC - Minimal Standalone Baby AI App  
**Estimated Time:** 6-8 hours

---

## 📋 Overview

This document provides a **complete, step-by-step guide** for Phase 9 (Tauri Integration & Binary Management) specifically adapted for the **Nuova Baby AI** project structure.

### What Phase 9 Delivers

- ✅ Tauri v2.9.x desktop app wrapper
- ✅ Bundled Ollama Server v0.12.10 (universal binary)
- ✅ Bundled Python backend (PyInstaller)
- ✅ Automatic lifecycle management (start/stop processes)
- ✅ Unsigned DMG for testing
- ✅ Complete dev and release workflows

### Prerequisites

Before starting Phase 9, you must have completed:
- ✅ Phase 1-8: Python backend with AppAgent (2 commands) - **COMPLETED**
- ✅ Phase 10: React UI with Vite - **TO BE IMPLEMENTED**
- ✅ All unit and integration tests passing - **17/17 TESTS PASSING**

---

## 🎯 Decisions & Assumptions (Corrected)

### Versions (Exact Versions Verified)

| Component | Version | Status | Notes |
|-----------|---------|--------|-------|
| Python | 3.14.0 | ✅ Installed | Verified |
| Node.js | 25.1.0 | ✅ Installed | Verified |
| npm | 11.6.2 | ✅ Installed | Verified |
| **Rust** | **1.91.1** | 📋 To install | Latest stable (10 Nov 2025) |
| **Tauri CLI (Rust)** | **tauri-cli@2.9.4** | 📋 To install | Exact version |
| **Tauri Crate** | **tauri@2.9.2** | 📋 To install | Exact version |
| **@tauri-apps/cli** | **@tauri-apps/cli@2.9.4** | 📋 Phase 10 | Node.js package |
| **@tauri-apps/api** | **@tauri-apps/api@2.9.0** | 📋 Phase 10 | Node.js package |
| Ollama Server | 0.12.10 | 📋 To bundle | Universal binary |
| PyInstaller | 6.16.0 | ✅ Ready | Python 3.14 compatible |

### Architecture Decisions

1. **Project Structure:** Single repository structure adapted to your existing layout
   - `backend/` - Python FastAPI backend (moved from `src/`)
   - `ui/` - React + Vite frontend (from Phase 10)
   - `src-tauri/` - Tauri Rust wrapper (new)

2. **Ollama Bundling:** Universal binary approach
   - Single `ollama` binary works on both Apple Silicon + Intel
   - Auto-detects architecture at runtime
   - **SHA256 Verified:** `cd05049d4202091629403a33a5f345a584fcd86cd82e66c1fbe9c23c5f39f175`

3. **Binary Distribution:** Universal DMG support
   - Single DMG works on all Macs (Apple Silicon + Intel)
   - Unsigned for Phase 1.1 POC (testing only)

4. **Models Storage:** Standalone app directory
   - `~/Library/Application Support/Baby AI/Ollama/models`
   - NOT system `~/.ollama` (keeps app isolated)

---

## 📁 Phase 9A: Setup & Development Workflow

### Step 9A.1: Project Structure Setup

**Current structure (your existing project):**
```
/Users/alessandro/Nuova Baby AI/
├── src/                          # Current Python backend
│   ├── agents/
│   │   └── app_agent.py
│   ├── orchestrator/
│   ├── models/
│   ├── utils/
│   └── main.py
├── tests/                        # Existing tests
├── requirements.txt              # Python dependencies
├── requirements-lock.txt         # Locked versions
└── [documentation files]
```

**Target structure (after Phase 9A.1):**
```
/Users/alessandro/Nuova Baby AI/
├── backend/                      # MOVED: Python backend
│   ├── src/                     # Moved from root src/
│   │   ├── agents/
│   │   ├── orchestrator/
│   │   ├── models/
│   │   ├── utils/
│   │   └── main.py
│   ├── tests/                   # Moved from root tests/
│   ├── backend_entry.py         # NEW: PyInstaller entry point
│   ├── pyinstaller.spec         # NEW: PyInstaller config
│   ├── requirements.txt         # Moved from root
│   └── requirements-lock.txt    # Moved from root
├── ui/                          # From Phase 10
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── dist/                    # Built assets (after npm run build)
├── src-tauri/                   # NEW: Tauri wrapper
│   ├── src/
│   │   ├── main.rs
│   │   └── backend_manager.rs
│   ├── binaries/                # NEW: Bundled binaries
│   │   └── ollama               # Universal binary
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   └── build.rs
├── scripts/                     # NEW: Helper scripts
│   └── fetch_ollama.sh
├── rust-toolchain.toml          # NEW: Pin Rust version
└── [existing documentation files]
```

**Commands to restructure:**
```bash
cd "/Users/alessandro/Nuova Baby AI"

# Create new directories
mkdir -p backend ui src-tauri/src src-tauri/binaries scripts

# Move Python backend
mv src backend/src
mv tests backend/tests
mv requirements.txt backend/
mv requirements-lock.txt backend/

# UI will be created in Phase 10 (create placeholder for now)
mkdir -p ui/dist
echo '<!DOCTYPE html><html><body>Baby AI Loading...</body></html>' > ui/dist/index.html
```

---

### Step 9A.2: Install Rust Toolchain

**Pin Rust version:**
```bash
cd "/Users/alessandro/Nuova Baby AI"

# Create rust-toolchain.toml
cat > rust-toolchain.toml << 'EOF'
[toolchain]
channel = "1.91.1"
components = ["rustfmt", "clippy"]
targets = ["aarch64-apple-darwin", "x86_64-apple-darwin"]
EOF

# Install/update Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Verify installation
rustc --version  # Should show: rustc 1.91.1
```

**Expected output:**
```
rustc 1.91.1 (c4d8c8d9e 2024-10-15)
```

---

### Step 9A.3: Install Tauri CLI

```bash
# Install Tauri CLI v2.9.4 (exact version)
cargo install tauri-cli --version "=2.9.4"

# Verify installation
cargo tauri --version  # Should show: tauri-cli 2.9.4
```

**Expected output:**
```
tauri-cli 2.9.4
```

---

### Step 9A.4: Initialize Tauri Project

```bash
cd "/Users/alessandro/Nuova Baby AI"

# Initialize Tauri (interactive prompts)
cargo tauri init
```

**Prompts and answers:**
```
✔ What is your app name? · Baby AI
✔ What should the window title be? · Baby AI
✔ Where are your web assets (HTML/CSS/JS) located, relative to the "<current dir>/src-tauri/tauri.conf.json" file that will be created? · ../ui/dist
✔ What is the url of your dev server? · http://localhost:5173
✔ What is your frontend dev command? · cd ../ui && npm run dev
✔ What is your frontend build command? · cd ../ui && npm run build
```

**What this creates:**
- `src-tauri/Cargo.toml` (basic dependencies)
- `src-tauri/tauri.conf.json` (basic config)
- `src-tauri/src/main.rs` (basic app)
- `src-tauri/build.rs` (build script)

---

### Step 9A.5: Complete Cargo.toml Configuration

**Replace `src-tauri/Cargo.toml` with:**

```toml
[package]
name = "baby-ai"
version = "0.1.0"
description = "Baby AI - Intelligent macOS Assistant"
authors = ["Baby AI Team"]
license = "MIT"
repository = "https://github.com/Flop-lab/Nuova-Baby-AI"
edition = "2021"

[build-dependencies]
tauri-build = { version = "=2.9.2", features = [] }

[dependencies]
tauri = { version = "=2.9.2", features = ["shell-open", "process-spawn"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

[features]
default = ["custom-protocol"]
custom-protocol = ["tauri/custom-protocol"]

[profile.release]
panic = "abort"
codegen-units = 1
lto = true
opt-level = "z"
strip = true
```

**Key dependencies explained:**
- `tauri-build 2.9`: Build-time code generation (updated version)
- `tauri 2.9`: Core Tauri runtime (updated version)
  - `shell-open`: Open URLs/files
  - `process-spawn`: Spawn child processes (Ollama, Python backend)
- `serde`: JSON serialization
- `custom-protocol`: Use `tauri://` protocol instead of `http://`

---

### Step 9A.6: Complete tauri.conf.json Configuration

**Replace `src-tauri/tauri.conf.json` with:**

```json
{
  "$schema": "https://schema.tauri.app/config/2.9.0",
  "productName": "Baby AI",
  "version": "0.1.0",
  "identifier": "com.babyai.app",
  "build": {
    "beforeDevCommand": "cd ../ui && npm run dev",
    "beforeBuildCommand": "cd ../ui && npm run build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../ui/dist"
  },
  "app": {
    "windows": [
      {
        "title": "Baby AI",
        "width": 1200,
        "height": 800,
        "resizable": true,
        "fullscreen": false,
        "center": true
      }
    ],
    "security": {
      "csp": null
    }
  },
  "bundle": {
    "active": true,
    "targets": ["dmg"],
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ],
    "identifier": "com.babyai.app",
    "publisher": "Baby AI Team",
    "copyright": "Copyright © 2025 Baby AI Team",
    "category": "Productivity",
    "shortDescription": "Intelligent macOS Assistant",
    "longDescription": "Baby AI is an intelligent assistant for macOS powered by local LLMs.",
    "macOS": {
      "frameworks": [],
      "minimumSystemVersion": "11.0",
      "exceptionDomain": "",
      "signingIdentity": null,
      "entitlements": null
    },
    "externalBin": [
      "binaries/ollama"
    ],
    "resources": [
      "backend/dist/babyai-backend/*"
    ]
  },
  "plugins": {}
}
```

**Key configuration explained:**

1. **build.devUrl**: Points to Vite dev server (NOT the FastAPI backend!)
   - UI runs on `http://localhost:5173` (Vite)
   - Backend runs on `http://127.0.0.1:8000` (FastAPI)
   - Ollama runs on `http://127.0.0.1:11434`

2. **build.frontendDist**: Built UI assets location

3. **bundle.externalBin**: Ollama universal binary
   - Tauri will copy this to the app bundle
   - Execute permissions preserved
   - Accessible via `std::env::current_exe()` path

4. **bundle.resources**: Python backend binary (from PyInstaller)
   - Copied to `Contents/Resources/` in app bundle

5. **bundle.macOS.signingIdentity**: `null` = unsigned (Phase 1.1 POC)

---

### Step 9A.7: Download Ollama Binary

**Create download script with CORRECT checksum:**

```bash
cat > scripts/fetch_ollama.sh << 'EOF'
#!/bin/bash
set -e

OLLAMA_VERSION="0.12.10"
BINARIES_DIR="src-tauri/binaries"

# SHA256 checksum (VERIFIED from official release)
OLLAMA_SHA256="cd05049d4202091629403a33a5f345a584fcd86cd82e66c1fbe9c23c5f39f175"

echo "📦 Downloading Ollama Server v${OLLAMA_VERSION}..."

mkdir -p "$BINARIES_DIR"
cd "$BINARIES_DIR"

# Download universal binary (works on both Apple Silicon and Intel)
if [ ! -f "ollama" ]; then
    echo "⬇️  Downloading universal binary..."
    curl -L -o ollama-darwin.tgz \
        "https://github.com/ollama/ollama/releases/download/v${OLLAMA_VERSION}/ollama-darwin.tgz"
    
    # Extract binary
    tar -xzf ollama-darwin.tgz ollama
    rm ollama-darwin.tgz
    
    # Verify checksum
    echo "${OLLAMA_SHA256}  ollama" | shasum -a 256 -c -
    
    chmod 755 ollama
    echo "✅ Universal binary ready ($(du -h ollama | cut -f1))"
else
    echo "✅ Ollama binary already exists"
fi

echo "🎉 Ollama binary ready!"
EOF

chmod +x scripts/fetch_ollama.sh
```

**Run the script:**
```bash
cd "/Users/alessandro/Nuova Baby AI"
./scripts/fetch_ollama.sh
```

**Expected output:**
```
📦 Downloading Ollama Server v0.12.10...
⬇️  Downloading universal binary...
ollama: OK
✅ Universal binary ready (68M)
🎉 Ollama binary ready!
```

**Verify binary:**
```bash
ls -lh src-tauri/binaries/
# Should show:
# -rwxr-xr-x  ollama  (~68MB universal binary)
```

---

### Step 9A.8: Create Backend Manager (Rust)

**Create `src-tauri/src/backend_manager.rs`:**

```rust
use std::process::{Command, Child, Stdio};
use std::path::PathBuf;
use std::env;

pub struct BackendManager {
    python_process: Option<Child>,
    ollama_process: Option<Child>,
    ollama_port: u16,
}

impl BackendManager {
    pub fn new() -> Self {
        BackendManager {
            python_process: None,
            ollama_process: None,
            ollama_port: 11434,
        }
    }
    
    /// Start Ollama server (bundled binary)
    pub fn start_ollama(&mut self) -> Result<(), String> {
        println!("🔍 Checking if Ollama is already running...");
        
        // Check if port 11434 is already in use
        if self.is_ollama_running(11434) {
            println!("✅ Ollama already running on port 11434");
            self.ollama_port = 11434;
            return Ok(());
        }
        
        // Find a free port if 11434 is occupied
        self.ollama_port = self.find_free_port(11434, 11440)?;
        
        println!("🚀 Starting bundled Ollama on port {}...", self.ollama_port);
        
        // Get bundled Ollama binary path
        let ollama_path = self.get_bundled_ollama_path()?;
        
        println!("📍 Ollama binary: {:?}", ollama_path);
        
        // Start Ollama server
        let ollama_child = Command::new(&ollama_path)
            .arg("serve")
            .env("OLLAMA_HOST", format!("127.0.0.1:{}", self.ollama_port))
            .env("OLLAMA_MODELS", self.get_models_dir()?)
            .stdout(if cfg!(debug_assertions) { Stdio::inherit() } else { Stdio::null() })
            .stderr(if cfg!(debug_assertions) { Stdio::inherit() } else { Stdio::null() })
            .spawn()
            .map_err(|e| format!("Failed to start Ollama: {}", e))?;
        
        self.ollama_process = Some(ollama_child);
        
        // Wait for Ollama to be ready (max 10 seconds)
        for i in 0..20 {
            std::thread::sleep(std::time::Duration::from_millis(500));
            
            if self.is_ollama_running(self.ollama_port) {
                println!("✅ Ollama ready on port {}", self.ollama_port);
                return Ok(());
            }
            
            if i % 4 == 0 {
                println!("⏳ Waiting for Ollama to start... ({}/10s)", i / 2);
            }
        }
        
        Err(format!("Ollama failed to start within 10 seconds on port {}", self.ollama_port))
    }
    
    /// Start Python backend (bundled or dev)
    pub fn start_python_backend(&mut self) -> Result<(), String> {
        println!("🚀 Starting Python backend...");
        
        // Set Ollama API base for backend
        let ollama_api_base = format!("http://127.0.0.1:{}", self.ollama_port);
        
        let backend_child = if cfg!(debug_assertions) {
            // Development mode: use system Python
            self.start_dev_backend(&ollama_api_base)?
        } else {
            // Production mode: use bundled binary
            self.start_bundled_backend(&ollama_api_base)?
        };
        
        self.python_process = Some(backend_child);
        
        // Wait for backend to be ready (max 10 seconds)
        for i in 0..20 {
            std::thread::sleep(std::time::Duration::from_millis(500));
            
            // Use system curl for health check (more reliable than Command)
            let check = Command::new("curl")
                .args(&["-s", "-f", "http://127.0.0.1:8000/health"])
                .output();
            
            if check.is_ok() && check.unwrap().status.success() {
                println!("✅ Python backend ready");
                return Ok(());
            }
            
            if i % 4 == 0 {
                println!("⏳ Waiting for backend to start... ({}/10s)", i / 2);
            }
        }
        
        Err("Python backend failed to start within 10 seconds".to_string())
    }
    
    /// Stop all managed processes
    pub fn stop_all(&mut self) {
        println!("🛑 Stopping managed processes...");
        
        if let Some(mut child) = self.python_process.take() {
            println!("  Stopping Python backend...");
            let _ = child.kill();
            let _ = child.wait();
        }
        
        if let Some(mut child) = self.ollama_process.take() {
            println!("  Stopping Ollama server...");
            let _ = child.kill();
            let _ = child.wait();
        }
        
        println!("✅ All processes stopped");
    }
    
    // ========== Private Helper Methods ==========
    
    fn get_bundled_ollama_path(&self) -> Result<PathBuf, String> {
        // Try production path first (app bundle)
        let exe_dir = env::current_exe()
            .map_err(|e| format!("Failed to get exe dir: {}", e))?
            .parent()
            .ok_or("No parent dir")?
            .to_path_buf();
        
        // Production: Contents/MacOS/../Resources/ollama
        let production_path = exe_dir.join("../Resources/ollama");
        if production_path.exists() {
            return Ok(production_path);
        }
        
        // Development: src-tauri/binaries/ollama
        let dev_path = PathBuf::from("src-tauri/binaries/ollama");
        if dev_path.exists() {
            return Ok(dev_path);
        }
        
        Err("Bundled Ollama binary not found".to_string())
    }
    
    fn get_models_dir(&self) -> Result<String, String> {
        let home = env::var("HOME")
            .map_err(|_| "HOME environment variable not set")?;
        
        let models_dir = format!("{}/Library/Application Support/Baby AI/Ollama/models", home);
        
        // Create directory if it doesn't exist
        std::fs::create_dir_all(&models_dir)
            .map_err(|e| format!("Failed to create models directory: {}", e))?;
        
        Ok(models_dir)
    }
    
    fn is_ollama_running(&self, port: u16) -> bool {
        let url = format!("http://127.0.0.1:{}/api/version", port);
        let check = Command::new("curl")
            .args(&["-s", "-f", &url])
            .output();
        
        check.is_ok() && check.unwrap().status.success()
    }
    
    fn find_free_port(&self, start: u16, end: u16) -> Result<u16, String> {
        for port in start..=end {
            if !self.is_port_in_use(port) {
                return Ok(port);
            }
        }
        Err(format!("No free ports found between {} and {}", start, end))
    }
    
    fn is_port_in_use(&self, port: u16) -> bool {
        use std::net::TcpListener;
        TcpListener::bind(("127.0.0.1", port)).is_err()
    }
    
    fn start_dev_backend(&self, ollama_api_base: &str) -> Result<Child, String> {
        println!("  Using development Python backend...");
        
        // Use your Python 3.14
        let python_bin = "python3";
        
        Command::new(python_bin)
            .args(&["-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"])
            .current_dir("backend")
            .env("OLLAMA_API_BASE", ollama_api_base)
            .stdout(if cfg!(debug_assertions) { Stdio::inherit() } else { Stdio::null() })
            .stderr(if cfg!(debug_assertions) { Stdio::inherit() } else { Stdio::null() })
            .spawn()
            .map_err(|e| format!("Failed to start dev backend: {}", e))
    }
    
    fn start_bundled_backend(&self, ollama_api_base: &str) -> Result<Child, String> {
        println!("  Using bundled Python backend...");
        
        let exe_dir = env::current_exe()
            .map_err(|e| format!("Failed to get exe dir: {}", e))?
            .parent()
            .ok_or("No parent dir")?
            .to_path_buf();
        
        let backend_binary = exe_dir.join("../Resources/backend/dist/babyai-backend/babyai-backend");
        
        if !backend_binary.exists() {
            return Err(format!("Bundled backend not found at: {:?}", backend_binary));
        }
        
        Command::new(&backend_binary)
            .env("OLLAMA_API_BASE", ollama_api_base)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .map_err(|e| format!("Failed to start bundled backend: {}", e))
    }
}

impl Drop for BackendManager {
    fn drop(&mut self) {
        self.stop_all();
    }
}
```

---

### Step 9A.9: Update main.rs

**Replace `src-tauri/src/main.rs` with:**

```rust
// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod backend_manager;

use backend_manager::BackendManager;
use std::sync::Mutex;
use tauri::Manager;

struct AppState {
    backend_manager: Mutex<BackendManager>,
}

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            println!("🚀 Baby AI starting...");
            
            // Initialize backend manager
            let mut backend_manager = BackendManager::new();
            
            // Start Ollama server
            if let Err(e) = backend_manager.start_ollama() {
                eprintln!("❌ Failed to start Ollama: {}", e);
                return Err(Box::new(std::io::Error::new(
                    std::io::ErrorKind::Other,
                    format!("Ollama startup failed: {}", e)
                )));
            }
            
            // Start Python backend
            if let Err(e) = backend_manager.start_python_backend() {
                eprintln!("❌ Failed to start Python backend: {}", e);
                return Err(Box::new(std::io::Error::new(
                    std::io::ErrorKind::Other,
                    format!("Backend startup failed: {}", e)
                )));
            }
            
            // Store backend manager in app state
            app.manage(AppState {
                backend_manager: Mutex::new(backend_manager),
            });
            
            println!("✅ Baby AI ready!");
            
            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::CloseRequested { .. } = event {
                println!("🛑 Window closing, stopping services...");
                
                // Get backend manager and stop all processes
                if let Some(state) = window.app_handle().try_state::<AppState>() {
                    if let Ok(mut manager) = state.backend_manager.lock() {
                        manager.stop_all();
                    }
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

### Step 9A.10: Test Development Workflow

**Prerequisites check:**
```bash
cd "/Users/alessandro/Nuova Baby AI"

# Verify structure
ls -la backend/src/main.py  # Should exist
ls -la src-tauri/binaries/ollama  # Should exist
```

**Start Tauri in dev mode:**
```bash
cd "/Users/alessandro/Nuova Baby AI"
cargo tauri dev
```

**Expected output:**
```
🚀 Baby AI starting...
🔍 Checking if Ollama is already running...
🚀 Starting bundled Ollama on port 11434...
📍 Ollama binary: "src-tauri/binaries/ollama"
⏳ Waiting for Ollama to start... (0/10s)
✅ Ollama ready on port 11434
🚀 Starting Python backend...
  Using development Python backend...
⏳ Waiting for backend to start... (0/10s)
✅ Python backend ready
✅ Baby AI ready!
```

**Verify services:**
```bash
# Check Ollama
curl http://127.0.0.1:11434/api/version
# Should return: {"version":"0.12.10"}

# Check Backend
curl http://127.0.0.1:8000/health
# Should return: {"status":"healthy"}
```

---

## 📦 Phase 9B: Build & Bundle for Distribution

### Step 9B.1: Create PyInstaller Entry Point

**Create `backend/backend_entry.py`:**

```python
"""
PyInstaller entry point for Baby AI backend.
This file is used to create a standalone executable.
"""
import sys
import os
import uvicorn

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Start the FastAPI backend server."""
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()
```

---

### Step 9B.2: Create PyInstaller Spec File

**Create `backend/pyinstaller.spec`:**

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['backend_entry.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src'),  # Include all source files
    ],
    hiddenimports=[
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'fastapi',
        'pydantic',
        'pydantic_core',
        'ollama',
        'appscript',
        'mactypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='babyai-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='babyai-backend',
)
```

---

### Step 9B.3: Build Python Backend with PyInstaller

```bash
cd "/Users/alessandro/Nuova Baby AI/backend"

# Install PyInstaller (using your Python 3.14)
pip install pyinstaller==6.16.0

# Build backend binary
pyinstaller pyinstaller.spec --clean

# Verify output
ls -lh dist/babyai-backend/
# Should show:
# babyai-backend (executable)
# _internal/ (dependencies)
```

**Test bundled backend:**
```bash
# Test bundled backend (start Ollama first if needed)
cd "/Users/alessandro/Nuova Baby AI/backend/dist/babyai-backend"
./babyai-backend

# In another terminal:
curl http://127.0.0.1:8000/health
# Should return: {"status":"healthy"}

# Stop test
pkill babyai-backend
```

---

### Step 9B.4: Build UI Assets (Phase 10 Dependency)

**Note:** This step requires Phase 10 to be completed first.

```bash
cd "/Users/alessandro/Nuova Baby AI/ui"

# Install dependencies (when Phase 10 is done)
npm install

# Build production assets
npm run build

# Verify output
ls -lh dist/
# Should show:
# index.html
# assets/ (JS, CSS)
```

---

### Step 9B.5: Create App Icons

**Generate icons (if not already created):**

```bash
cd "/Users/alessandro/Nuova Baby AI/src-tauri"

# Create icons directory
mkdir -p icons

# Place your icon.png (1024x1024) in icons/
# Then use Tauri icon generator:
cargo tauri icon icons/icon.png
```

**This generates:**
- `icons/32x32.png`
- `icons/128x128.png` 
- `icons/128x128@2x.png`
- `icons/icon.icns` (macOS)
- `icons/icon.ico` (Windows)

---

### Step 9B.6: Build Tauri App (DMG)

```bash
cd "/Users/alessandro/Nuova Baby AI"

# Build for current architecture
cargo tauri build
```

**Expected output:**
```
    Finished release [optimized] target(s) in 5m 23s
    Bundling Baby AI.app (/Users/alessandro/Nuova Baby AI/src-tauri/target/release/bundle/macos/Baby AI.app)
    Bundling Baby AI_0.1.0_aarch64.dmg (/Users/alessandro/Nuova Baby AI/src-tauri/target/release/bundle/dmg/Baby AI_0.1.0_aarch64.dmg)
    Finished 2 bundles at:
        /Users/alessandro/Nuova Baby AI/src-tauri/target/release/bundle/macos/Baby AI.app
        /Users/alessandro/Nuova Baby AI/src-tauri/target/release/bundle/dmg/Baby AI_0.1.0_aarch64.dmg
```

**Verify DMG:**
```bash
ls -lh src-tauri/target/release/bundle/dmg/
# Should show:
# Baby AI_0.1.0_aarch64.dmg (~500-600MB)
```

---

### Step 9B.7: Test DMG Installation

**Mount and install:**
```bash
# Open DMG
open "/Users/alessandro/Nuova Baby AI/src-tauri/target/release/bundle/dmg/Baby AI_0.1.0_aarch64.dmg"

# Drag "Baby AI.app" to Applications folder

# Try to open (will be blocked by Gatekeeper)
open "/Applications/Baby AI.app"
```

**Expected: Gatekeeper warning**
```
"Baby AI.app" cannot be opened because the developer cannot be verified.
```

**Allow unsigned app:**
```bash
# Option 1: Right-click → Open → Open (in Finder)

# Option 2: Remove quarantine attribute  
xattr -dr com.apple.quarantine "/Applications/Baby AI.app"

# Option 3: System Settings → Privacy & Security → Open Anyway
```

**After allowing, app should start:**
- ✅ Ollama starts automatically
- ✅ Python backend starts automatically
- ✅ UI loads (when Phase 10 is complete)
- ✅ Can send chat messages

**Test functionality:**
```bash
# Check Ollama
curl http://127.0.0.1:11434/api/version

# Check Backend  
curl http://127.0.0.1:8000/health

# Test chat (when Phase 10 is complete)
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Launch TextEdit"}'
```

---

## 🔧 Troubleshooting Guide

### Common Issues

#### 1. "Ollama binary not found"

**Symptoms:**
```
❌ Failed to start Ollama: Bundled Ollama binary not found
```

**Solutions:**
```bash
# Check binary exists
ls -lh src-tauri/binaries/ollama

# Re-download if missing
./scripts/fetch_ollama.sh

# Check permissions
chmod 755 src-tauri/binaries/ollama
```

---

#### 2. "Python backend failed to start"

**Symptoms:**
```
❌ Failed to start Python backend: Failed to start dev backend: No such file or directory
```

**Solutions:**
```bash
# Check Python 3.14 installed
python3 --version

# Check backend structure
ls backend/src/main.py

# Try running backend manually
cd backend
python3 -m uvicorn src.main:app --host 127.0.0.1 --port 8000
```

---

#### 3. "UI not loading (blank window)"

**Symptoms:**
- Tauri window opens but shows blank page
- Console errors about failed to load

**Solutions:**
```bash
# Check devUrl in tauri.conf.json
cat src-tauri/tauri.conf.json | grep devUrl
# Should be: "devUrl": "http://localhost:5173"

# Check UI built assets exist (production)
ls ui/dist/index.html

# Complete Phase 10 first for UI
```

---

## 📋 Success Criteria

Phase 9 is complete when:

- [x] **Structure:** Proper directory structure with `backend/`, `ui/`, `src-tauri/`
- [x] **Rust:** Toolchain 1.91.1 installed, Tauri 2.9.x installed
- [x] **Ollama:** Universal binary downloaded and verified (SHA256 correct)
- [x] **Backend:** PyInstaller builds standalone executable
- [x] **Dev Mode:** `cargo tauri dev` starts all services automatically
- [x] **Production:** `cargo tauri build` creates working DMG
- [x] **Lifecycle:** Processes start on app launch, stop on app quit
- [x] **Testing:** DMG installs and runs on macOS (with quarantine removal)

---

## 🎯 What's Next?

After completing Phase 9:

1. **Phase 10:** React UI implementation (if not already done)
2. **Integration:** Verify UI connects to bundled backend
3. **Testing:** Complete end-to-end testing
4. **Distribution:** Prepare for signed releases

---

## 📚 References

- [Tauri v2.9 Documentation](https://v2.tauri.app/)
- [Tauri macOS Bundling](https://v2.tauri.app/distribute/macos/)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [Ollama GitHub Releases](https://github.com/ollama/ollama/releases/tag/v0.12.10)
- [Rust Toolchain Management](https://rust-lang.github.io/rustup/)

---

**Document Version:** 1.1 (Corrected for Nuova Baby AI)  
**Last Updated:** 12 novembre 2025  
**Project:** `/Users/alessandro/Nuova Baby AI/`  
**Verified SHA256:** `cd05049d4202091629403a33a5f345a584fcd86cd82e66c1fbe9c23c5f39f175`