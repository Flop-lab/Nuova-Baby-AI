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
