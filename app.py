import streamlit as st
import tempfile
import os
import whisper
import google.generativeai as genai
from dotenv import load_dotenv

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ----------------------------
# Streamlit UI Setup
# ----------------------------
st.set_page_config(page_title="Lecture Voice-to-Notes Generator")

st.title("🎙️ Lecture Voice-to-Notes Generator")
st.write("Upload a lecture audio file and convert it into structured study material.")

uploaded_file = st.file_uploader("Upload Lecture Audio", type=["mp3", "wav", "m4a"])

# ----------------------------
# Whisper Model (Load Once)
# ----------------------------
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")  # you can change to small/medium if powerful PC

whisper_model = load_whisper_model()

# ----------------------------
# LLM Generation Functions
# ----------------------------
def generate_with_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text


if uploaded_file:

    # Save temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("🔊 Transcribing audio locally (Whisper)...")

    # Transcription (FREE - local)
    result = whisper_model.transcribe(tmp_path)
    transcript_text = result["text"]

    st.success("✅ Transcription Complete!")

    st.subheader("📝 Transcript")
    st.write(transcript_text)

    st.info("🤖 Generating Study Material with Gemini...")

    # Generate Notes
    notes_prompt = f"""
    Convert this lecture transcript into structured study notes
    with headings and bullet points:

    {transcript_text}
    """

    notes = generate_with_gemini(notes_prompt)

    # Generate Quiz
    quiz_prompt = f"""
    Create 5 multiple-choice questions from this lecture.
    Include answers at the end.

    {transcript_text}
    """

    quiz = generate_with_gemini(quiz_prompt)

    # Generate Flashcards
    flashcard_prompt = f"""
    Create 5 flashcards in Q&A format from this lecture:

    {transcript_text}
    """

    flashcards = generate_with_gemini(flashcard_prompt)

    st.subheader("📘 Summary Notes")
    st.write(notes)

    st.subheader("❓ Quiz Questions")
    st.write(quiz)

    st.subheader("🧠 Flashcards")
    st.write(flashcards)

    st.success("🎉 Done!")