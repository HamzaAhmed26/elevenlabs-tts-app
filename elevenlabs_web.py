import streamlit as st
import requests

XI_API_KEY = st.secrets["XI_API_KEY"]

@st.cache_data
def get_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": XI_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["voices"]
    else:
        st.error("Failed to fetch voices.")
        return []

def text_to_speech(voice_id, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": XI_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.7, "similarity_boost": 0.7}
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

st.title("🗣️ ElevenLabs Text to Speech")

voices = get_voices()
voice_names = [f"{v['name']} ({v['voice_id'][:6]})" for v in voices]
voice_map = {name: v['voice_id'] for name, v in zip(voice_names, voices)}

selected_voice = st.selectbox("Choose a voice", voice_names)
text_input = st.text_area("Enter text", "Hello world! This is ElevenLabs.")

if st.button("Generate Audio"):
    audio = text_to_speech(voice_map[selected_voice], text_input)
    if audio:
        st.audio(audio, format="audio/mp3")
        st.success("✅ Audio generated!")
