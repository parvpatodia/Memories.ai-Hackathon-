# test_api.py - Let's test if we can talk to Memories.ai!

import requests
import os

# Replace this with your actual API key from Step 1
API_KEY = "your_actual_api_key_here"

# Let's see if we can connect to Memories.ai
def test_connection():
    print("🧪 Testing connection to Memories.ai...")
    
    # This is the basic API endpoint
    url = "https://api.memories.ai/v1/memories"
    
    # Headers with your API key
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Try to list memories (even if we have none)
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ SUCCESS! We're connected to Memories.ai!")
            print("Response:", response.json())
        else:
            print(f"❌ Connection failed with status: {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Run the test
if __name__ == "__main__":
    test_connection()