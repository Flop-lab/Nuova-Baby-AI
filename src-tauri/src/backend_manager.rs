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

        // Production: Contents/MacOS/ollama (same directory as baby-ai executable)
        let production_path = exe_dir.join("ollama");
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

        // Use standard Ollama models directory instead of custom path
        // This allows Baby AI to use models already downloaded by the user
        let models_dir = format!("{}/.ollama/models", home);

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

        // Get project root from current exe location (exe is in target/debug, so ../.. = project root)
        let exe_dir = env::current_exe()
            .ok()
            .and_then(|p| p.parent().map(|p| p.to_path_buf()))
            .unwrap_or_else(|| PathBuf::from("."));

        // In dev mode, exe is at src-tauri/target/debug/baby-ai
        // So we need to go up 3 levels to get to project root
        let project_root = exe_dir
            .parent()
            .and_then(|p| p.parent())
            .and_then(|p| p.parent())
            .map(|p| p.to_path_buf())
            .unwrap_or_else(|| PathBuf::from("."));

        let python_bin = project_root.join("venv/bin/python");

        println!("  Python binary: {:?}", python_bin);
        println!("  Project root: {:?}", project_root);

        Command::new(&python_bin)
            .args(&["-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"])
            .current_dir(&project_root)
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

        let backend_binary = exe_dir.join("../Resources/_up_/dist/babyai-backend/babyai-backend");

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
