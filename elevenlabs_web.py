import streamlit as st
import requests
import base64

# 🔐 Set your ElevenLabs API Key and Cloned Voice ID here
XI_API_KEY = st.secrets["XI_API_KEY"]
CLONED_VOICE_ID = "your_cloned_voice_id_here"

# ⛓️ Text-to-speech function using ElevenLabs API
def text_to_speech(voice_id, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": XI_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",  # or multilingual if needed
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.content if response.status_code == 200 else None

# 🎛️ Streamlit UI setup
st.set_page_config(page_title="Cloned Voice TTS", page_icon="🧬")
st.title("🧬 Cloned Voice TTS (ElevenLabs)")

# 📝 Text input area
text_input = st.text_area("Enter text to synthesize", height=150)

# 📁 Optional file upload
uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
    st.success("Text loaded from uploaded file!")

# 🧾 Custom file name input
custom_filename = st.text_input("Save audio as", "cloned_voice_output")

# 🎧 Generate audio button
if st.button("🎧 Generate Audio"):
    if not text_input.strip():
        st.warning("Please enter or upload some text.")
    else:
        audio = text_to_speech(CLONED_VOICE_ID, text_input)
        if audio:
            audio_filename = f"{custom_filename}.mp3"
            
            # 💾 Save locally (optional, mostly for history tracking)
            with open(audio_filename, "wb") as f:
                f.write(audio)

            # 🔊 Playback in app
            st.audio(audio, format="audio/mp3")

            # 📥 Download button
            b64 = base64.b64encode(audio).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="{audio_filename}">📥 Download {audio_filename}</a>'
            st.markdown(href, unsafe_allow_html=True)

            # 📜 Save to session state history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append((audio_filename, b64))
            st.success("Audio generated successfully! 🎉")
        else:
            st.error("Something went wrong with the API request.")

# 🎵 Playback history (optional)
if "history" in st.session_state and st.session_state.history:
    st.markdown("### 🕘 Recent Audio")
    for name, b64_audio in reversed(st.session_state.history[-5:]):
        st.markdown(f"**{name}**")
        st.audio(base64.b64decode(b64_audio), format="audio/mp3")
