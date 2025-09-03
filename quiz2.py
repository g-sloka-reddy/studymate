import streamlit as st
import PyPDF2
from transformers import pipeline
import random

# Load summarizer (using HuggingFace)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

st.title("📚 StudyMate - AI PDF Summarizer & Quiz Generator")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + " "

    st.subheader("📖 Extracted Text (Preview)")
    st.write(text[:1000] + "..." if len(text) > 1000 else text)

    # Summarize
    st.subheader("📝 Summary (Bullet Points)")
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summary = ""
    for chunk in chunks[:3]:  # limit to 3 chunks
        result = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
        summary += result[0]['summary_text'] + "\n"

    bullet_points = summary.split(". ")
    for point in bullet_points:
        st.write("• " + point.strip())

    # Mindmap (basic simulation)
    st.subheader("🧠 Mindmap (Concept Breakdown)")
    st.write("Here’s a simple breakdown of key ideas:")
    for idx, point in enumerate(bullet_points[:5], 1):
        st.write(f"{idx}. {point.strip()}")

    # Quiz
    st.subheader("❓ Quiz Questions")
    quiz_questions = [
        f"What is the main idea of: '{point.strip()}' ?" for point in bullet_points[:5]
    ]
    for q in quiz_questions:
        st.write("🔹 " + q)

    # Random quiz generator
    if st.button("🎲 Roll Dice for a Random Question"):
        st.write("👉 " + random.choice(quiz_questions))
