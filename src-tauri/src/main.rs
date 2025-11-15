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
            eprintln!("🚀 Baby AI starting... (stderr)");

            // Initialize backend manager
            let mut backend_manager = BackendManager::new();

            // Start Ollama server
            println!("📦 Starting Ollama...");
            eprintln!("📦 Starting Ollama... (stderr)");
            match backend_manager.start_ollama() {
                Ok(_) => {
                    println!("✅ Ollama started successfully");
                    eprintln!("✅ Ollama started successfully (stderr)");
                }
                Err(e) => {
                    let error_msg = format!("Failed to start Ollama: {}", e);
                    eprintln!("❌ {}", error_msg);

                    return Err(Box::new(std::io::Error::new(
                        std::io::ErrorKind::Other,
                        error_msg
                    )));
                }
            }

            // Start Python backend
            println!("🐍 Starting Python backend...");
            eprintln!("🐍 Starting Python backend... (stderr)");
            match backend_manager.start_python_backend() {
                Ok(_) => {
                    println!("✅ Python backend started successfully");
                    eprintln!("✅ Python backend started successfully (stderr)");
                }
                Err(e) => {
                    let error_msg = format!("Failed to start Python backend: {}", e);
                    eprintln!("❌ {}", error_msg);

                    return Err(Box::new(std::io::Error::new(
                        std::io::ErrorKind::Other,
                        error_msg
                    )));
                }
            }

            // Store backend manager in app state
            app.manage(AppState {
                backend_manager: Mutex::new(backend_manager),
            });

            println!("✅ Baby AI ready!");
            eprintln!("✅ Baby AI ready! (stderr)");

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
