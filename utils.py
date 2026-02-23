import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_notes(text):
    prompt = f"""
    Convert this lecture transcript into structured study notes 
    with headings and bullet points:

    {text}
    """
    response = model.generate_content(prompt)
    return response.text


def generate_quiz(text):
    prompt = f"""
    Create 5 multiple-choice questions from this lecture.
    Include answers at the end.

    {text}
    """
    response = model.generate_content(prompt)
    return response.text


def generate_flashcards(text):
    prompt = f"""
    Create 5 flashcards in Q&A format from this lecture:

    {text}
    """
    response = model.generate_content(prompt)
    return response.text