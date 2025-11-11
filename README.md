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
