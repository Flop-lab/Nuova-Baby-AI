"""
Test script for Baby AI FastAPI backend
Tests the /health and /api/chat endpoints
"""
import requests
import time
import sys

BASE_URL = "http://localhost:8000"


def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n" + "=" * 80)
    print("Testing /health endpoint")
    print("=" * 80)

    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print("✗ Health check failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_chat_endpoint(message: str):
    """Test the chat endpoint with a message"""
    print("\n" + "=" * 80)
    print(f"Testing /api/chat with message: '{message}'")
    print("=" * 80)

    try:
        payload = {"message": message}
        print(f"Sending: {payload}")

        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/chat", json=payload)
        duration = time.time() - start_time

        print(f"Status Code: {response.status_code}")
        print(f"Duration: {duration:.2f}s")

        if response.status_code == 200:
            data = response.json()
            print(f"Reply: {data.get('reply')}")
            print("✓ Chat request successful")
            return True
        else:
            print(f"Response: {response.text}")
            print("✗ Chat request failed")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    print("=" * 80)
    print("Baby AI Backend API Tests")
    print("=" * 80)
    print(f"Base URL: {BASE_URL}")
    print("\nMake sure the backend is running:")
    print("  python src/main.py")
    print()

    # Wait for user to confirm server is running
    input("Press Enter when the server is ready...")

    results = []

    # Test 1: Health check
    results.append(("Health Check", test_health_endpoint()))
    time.sleep(1)

    # Test 2: Simple chat request
    results.append(("Open Safari", test_chat_endpoint("Open Safari")))
    time.sleep(2)

    # Test 3: Multi-step request
    results.append(("Open and Close Spotify", test_chat_endpoint("Open Spotify and then close it")))
    time.sleep(2)

    # Test 4: Out of scope request
    results.append(("Weather Query", test_chat_endpoint("What's the weather?")))

    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(0)
