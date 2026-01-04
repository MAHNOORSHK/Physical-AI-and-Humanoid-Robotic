import requests
import json

# Test the chatbot endpoint
url = "http://localhost:8000/api/chat/query"
data = {
    "message": "What is ROS 2?"
}

try:
    response = requests.post(url, json=data)
    result = response.json()

    print("=" * 60)
    print("CHATBOT RESPONSE:")
    print("=" * 60)
    print(f"\nResponse: {result['response']}\n")

    if result.get('citations'):
        print("Citations:")
        for citation in result['citations']:
            print(f"  - {citation['chapter']} - {citation['section']}")
            print(f"    URL: {citation['url']}")
            print(f"    Relevance: {citation['relevance_score']:.2f}\n")

    print(f"Session ID: {result.get('session_id')}")
    print("=" * 60)

except Exception as e:
    print(f"Error: {e}")
