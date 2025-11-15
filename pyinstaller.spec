# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Baby AI Backend with Pydantic AI support
Created: November 14, 2025
Version: 1.0

This spec file ensures all Pydantic AI dependencies are properly included
in the standalone executable.
"""

import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

# ============================================================================
# Hidden Imports - Modules that PyInstaller doesn't detect automatically
# ============================================================================

# Pydantic AI core modules (imported dynamically)
pydantic_ai_modules = [
    'pydantic_ai',
    'pydantic_ai.agent',
    'pydantic_ai.tools',
    'pydantic_ai.models',
    'pydantic_ai.models.openai',
    'pydantic_ai.providers.ollama',
    'pydantic_ai.messages',
    'pydantic_ai.result',
    'pydantic_ai._utils',
    'pydantic_ai._agent_graph',
    'pydantic_ai._function_schema',
    'pydantic_ai._griffe',
    'pydantic_ai._run_context',
    'pydantic_ai._output',
    'pydantic_ai._tool_manager',
    'pydantic_ai._parts_manager',
    'pydantic_ai.run',
]

# Pydantic and related modules (slim version - NO pydantic_graph!)
pydantic_modules = [
    'pydantic',
    'pydantic_core',
    'pydantic_settings',
]

# FastAPI and dependencies
fastapi_modules = [
    'fastapi',
    'starlette',
    'uvicorn',
    'httpx',
]

# Ollama client
ollama_modules = [
    'ollama',
    'ollama._client',
]

# AppScript for macOS automation
appscript_modules = [
    'appscript',
    'aem',
    'aeosa',
]

# Logging and utilities
util_modules = [
    'structlog',
    'anyio',
    'sniffio',
]

# Combine all hidden imports
hiddenimports = (
    pydantic_ai_modules +
    pydantic_modules +
    fastapi_modules +
    ollama_modules +
    appscript_modules +
    util_modules
)

# ============================================================================
# Collect Data Files and Binaries
# ============================================================================

datas = []
binaries = []

# Collect all data files from pydantic_ai
pydantic_ai_datas, pydantic_ai_binaries, pydantic_ai_hidden = collect_all('pydantic_ai')
datas += pydantic_ai_datas
binaries += pydantic_ai_binaries
hiddenimports += pydantic_ai_hidden

# Collect all data files from pydantic
pydantic_datas, pydantic_binaries, pydantic_hidden = collect_all('pydantic')
datas += pydantic_datas
binaries += pydantic_binaries
hiddenimports += pydantic_hidden

# Collect all data files from pydantic_core
pydantic_core_datas, pydantic_core_binaries, pydantic_core_hidden = collect_all('pydantic_core')
datas += pydantic_core_datas
binaries += pydantic_core_binaries
hiddenimports += pydantic_core_hidden

# Collect all data files from genai_prices (needed for pydantic-ai metadata)
genai_prices_datas, genai_prices_binaries, genai_prices_hidden = collect_all('genai_prices')
datas += genai_prices_datas
binaries += genai_prices_binaries
hiddenimports += genai_prices_hidden

# ============================================================================
# Analysis
# ============================================================================

a = Analysis(
    ['backend_entry.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude test and development modules to reduce size
        'pytest',
        'pytest_asyncio',
        'pytest_cov',
        'coverage',
        'mypy',
        'black',
        'ruff',
        # Exclude unused logfire (removed from project)
        'logfire',
        'logfire._internal',
        'logfire.integrations',
        # Exclude large unused modules
        'matplotlib',
        'scipy',
        'pandas',
        'tensorflow',
        'torch',
        'PIL',
        'tkinter',
    ],
    noarchive=False,
    optimize=0,
)

# ============================================================================
# PYZ (Python ZIP archive)
# ============================================================================

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

# ============================================================================
# EXE (Executable)
# ============================================================================

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
    console=True,  # Keep console for logging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ============================================================================
# COLLECT (Bundle all files together)
# ============================================================================

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
