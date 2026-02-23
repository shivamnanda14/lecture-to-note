import streamlit as st
import google.generativeai as genai
import os
import tempfile

# ----------------------------
# Configure Gemini API
# ----------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Lecture Voice-to-Notes Generator")
st.title("🎙️ Lecture Voice-to-Notes Generator")
st.write("Upload a lecture audio file and convert it into structured notes, quizzes, and flashcards.")

uploaded_file = st.file_uploader(
    "Upload Lecture Audio",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file:

    st.info("📁 Saving uploaded file...")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("☁️ Uploading audio to Gemini...")

    try:
        audio_file = genai.upload_file(tmp_path)

        st.info("🤖 Generating transcript and study materials...")

        response = model.generate_content(
            [
                """
                1. First transcribe this lecture.
                2. Then generate structured study notes with headings and bullet points.
                3. Create 5 multiple-choice quiz questions with answers.
                4. Create 5 flashcards in Q&A format.
                """,
                audio_file,
            ]
        )

        st.success("✅ Processing Complete!")

        st.subheader("📘 Generated Study Material")
        st.write(response.text)

    except Exception as e:
        st.error("Something went wrong during processing.")
        st.exception(e)
