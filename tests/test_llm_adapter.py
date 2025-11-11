import pytest
from src.llm.client import LLMClient
from src.llm.ollama_adapter import OllamaAdapter

# Test 1: LLMClient is abstract and cannot be instantiated
def test_llmclient_is_abstract():
    with pytest.raises(TypeError):
        LLMClient()

# Test 2: OllamaAdapter implements generate and returns a dict
def test_ollama_adapter_generate(monkeypatch):
    # Patch ollama.generate to avoid real API call
    class DummyResponse(dict):
        pass
    def dummy_generate(model, prompt):
        return DummyResponse({"content": "dummy response"})
    monkeypatch.setattr("ollama.generate", dummy_generate)
    adapter = OllamaAdapter()
    result = adapter.generate("Hello", model="mistral:7b-instruct")
    assert isinstance(result, dict)
    assert "content" in result

# Test 3: Import modules
def test_import_modules():
    from src.llm.client import LLMClient
    from src.llm.ollama_adapter import OllamaAdapter
    assert LLMClient is not None
    assert OllamaAdapter is not None
