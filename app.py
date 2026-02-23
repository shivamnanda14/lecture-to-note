import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("Lecture Voice-to-Notes Generator")

uploaded_file = st.file_uploader("Upload Lecture Audio", type=["mp3", "wav", "m4a"])

if uploaded_file:

    st.info("Uploading audio to Gemini...")

    audio_file = genai.upload_file(uploaded_file)

    response = model.generate_content(
        [
            "Transcribe this lecture and provide structured study notes.",
            audio_file,
        ]
    )

    transcript_text = response.text

    st.subheader("📝 Notes + Transcript")
    st.write(transcript_text)
