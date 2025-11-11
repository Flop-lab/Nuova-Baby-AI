"""
Test script for the complete orchestrator flow with Qwen 2.5 7B Instruct
Tests tool calling with think=True enabled
"""
import asyncio
import sys
from src.llm.ollama_adapter import OllamaAdapter
from src.models.config import OrchestratorConfig
from src.orchestrator.orchestrator import orchestrate_with_retry
from src.utils.logger import setup_logging

# Setup logging
setup_logging()


async def test_orchestrator():
    """Test the orchestrator with various requests"""

    print("=" * 80)
    print("Baby AI - Orchestrator Test with Qwen 2.5 7B Instruct")
    print("Testing tool calling with think=True enabled")
    print("=" * 80)
    print()

    # Initialize LLM client with Qwen3 4B Thinking
    llm_client = OllamaAdapter(model="qwen3:4b-thinking-2507-q8_0")
    config = OrchestratorConfig()

    # Test cases
    test_cases = [
        "Open Safari",
        "Close Safari",
        "Open Spotify and then close it",
        "What's the weather?",  # Should respond that it can't do this
    ]

    for i, user_message in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test {i}/{len(test_cases)}")
        print(f"{'=' * 80}")
        print(f"User: {user_message}")
        print("-" * 80)

        try:
            response = await orchestrate_with_retry(
                user_message=user_message,
                llm_client=llm_client,
                config=config
            )

            print(f"Assistant: {response.reply}")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

        print()

        # Wait a bit between requests
        if i < len(test_cases):
            await asyncio.sleep(2)

    print("=" * 80)
    print("All tests completed!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        asyncio.run(test_orchestrator())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
