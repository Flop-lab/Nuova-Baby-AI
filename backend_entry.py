"""
PyInstaller entry point for Baby AI backend.
This file is used to create a standalone executable.
"""
import sys
import os
import uvicorn

# Add src to Python path (src/ is in the same directory as this file)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Start the FastAPI backend server."""
    # Import directly instead of using string import
    # This works better with PyInstaller
    from src.main import app

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()
