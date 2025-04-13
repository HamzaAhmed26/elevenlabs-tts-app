import requests

XI_API_KEY = "<xi-api-key>"  # Replace with your ElevenLabs API key

# Step 1: Get all voices
def get_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['voices']
    else:
        print("Error fetching voices:", response.status_code)
        return []

# Step 2: Display voices and select one
def choose_voice(voices):
    print("\nAvailable Voices:")
    for i, voice in enumerate(voices):
        print(f"{i + 1}. {voice['name']} ({voice['voice_id']})")
    
    index = int(input("\nSelect a voice by number: ")) - 1
    return voices[index]['voice_id'], voices[index]['name']

# Step 3: Convert text to speech
def text_to_speech(voice_id, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": XI_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("✅ Audio saved as output.mp3")
    else:
        print("Error converting text:", response.status_code, response.text)

# Main flow
if __name__ == "__main__":
    voices = get_voices()
    if voices:
        voice_id, voice_name = choose_voice(voices)
        print(f"\nYou selected: {voice_name}")
        text = input("Enter the text you want to convert to speech: ")
        text_to_speech(voice_id, text)
