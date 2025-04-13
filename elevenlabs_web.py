import streamlit as st
import requests
import os
from datetime import datetime

XI_API_KEY = "<xi-api-key>"  # Replace this with your actual key

@st.cache_data
def get_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": XI_API_KEY}
    res = requests.get(url, headers=headers)
    return res.json()["voices"] if res.status_code == 200 else []

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
    return response.content if response.status_code == 200 else None

st.set_page_config(page_title="ElevenLabs TTS", page_icon="🎙️")
st.title("🎙️ ElevenLabs Text-to-Speech Web App")

voices = get_voices()
voice_names = [f"{v['name']} ({v['voice_id'][:6]})" for v in voices]
voice_map = {name: v for name, v in zip(voice_names, voices)}

selected_voice_name = st.selectbox("Choose a voice", voice_names)
selected_voice = voice_map[selected_voice_name]
st.caption(selected_voice.get("description", "No description available."))

text_input = st.text_area("Enter text to synthesize")

uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
    st.success("Text loaded from file!")

custom_filename = st.text_input("Save audio as", "output")

if st.button("🎧 Generate Audio"):
    if not text_input.strip():
        st.warning("Please enter or upload some text.")
    else:
        audio = text_to_speech(selected_voice["voice_id"], text_input)
        if audio:
            audio_filename = f"{custom_filename}.mp3"
            with open(audio_filename, "wb") as f:
                f.write(audio)
            st.audio(audio, format="audio/mp3")
            st.success(f"✅ Audio saved as {audio_filename}")

            # Save to session history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append(audio_filename)

# Display session history
if "history" in st.session_state and st.session_state.history:
    st.markdown("### 🎵 Audio History")
    for file in reversed(st.session_state.history[-5:]):
        st.audio(file, format="audio/mp3")
