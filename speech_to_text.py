import streamlit as st
import whisper

# Streamlit UI
def run():
    st.title("Speech to Text Transcription 🗣️")
    uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, etc.)", type=["mp3", "wav"])

    if uploaded_file is not None:
        # Save the uploaded audio file
        with open("uploaded_audio.mp3", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load Whisper model
        model = whisper.load_model("base")  # You can use "tiny", "base", "small", "medium", or "large" models

        # Transcribe the audio
        result = model.transcribe("uploaded_audio.mp3")

        # Display the transcribed text
        text = result["text"]
        st.write("Transcribed Text:")
        st.write(text)

        # Provide option to download the transcribed text
        with open("transcription.txt", "w") as text_file:
            text_file.write(text)

        st.download_button("Download Transcribed Text", "transcription.txt", file_name="transcription.txt")
