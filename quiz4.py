import streamlit as st
import PyPDF2
import requests
import random
import os

HF_TOKEN = "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"  # replace with your token
API_URL = "https://api-inference.huggingface.co/models/ibm-granite/granite-3.2-8b-instruct"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

st.title("📚 StudyMate - IBM Granite (API) PDF Summarizer & Quiz Generator")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
        text += " "

    st.subheader("📖 Extracted Text (Preview)")
    st.write(text[:1000] + "..." if len(text) > 1000 else text)

    # Summarize
    st.subheader("📝 Summary (Bullet Points)")
    chunks = [text[i:i+1500] for i in range(0, len(text), 1500)]
    summary = ""
    for chunk in chunks[:2]:  # limit to 2 chunks to save tokens
        result = query({
            "inputs": f"Summarize the following text in 5 short bullet points:\n\n{chunk}",
            "parameters": {"max_length": 200, "temperature": 0.7}
        })
        if isinstance(result, list):
            summary += result[0]['generated_text'] + "\n"
        elif "generated_text" in result:
            summary += result["generated_text"] + "\n"
        else:
            summary += str(result) + "\n"

    bullet_points = summary.strip().split("\n")
    for point in bullet_points:
        if point.strip():
            st.write("• " + point.strip())

    # Mindmap (basic simulation)
    st.subheader("🧠 Mindmap (Concept Breakdown)")
    for idx, point in enumerate(bullet_points[:5], 1):
        st.write(f"{idx}. {point.strip()}")

    # Quiz
    st.subheader("❓ Quiz Questions")
    quiz_questions = [
        f"What is the main idea of: '{point.strip()}'?" for point in bullet_points[:5] if point.strip()
    ]
    for q in quiz_questions:
        st.write("🔹 " + q)

    # Random quiz generator
    if st.button("🎲 Roll Dice for a Random Question"):
        st.write("👉 " + random.choice(quiz_questions))
