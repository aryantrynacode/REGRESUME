import streamlit as st
import fitz  # PyMuPDF
import json
import os

# 🔽 Safe load for skill list
def load_skills(file_path='skills.txt'):
    if not os.path.exists(file_path):
        st.error(f"⚠️ File '{file_path}' not found. Please make sure it's in the same folder as app.py.")
        return []
    with open(file_path, 'r') as f:
        return [line.strip().lower() for line in f.readlines()]

# 🔽 Extract text from PDF
def extract_text_from_pdf(pdf_file):
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

# 🔽 Extract skills from resume text
def extract_skills(text, skills):
    text_lower = text.lower()
    return [skill for skill in skills if skill in text_lower]

# 🚀 Streamlit app
st.title("📄 Resume Skill Extractor")

uploaded_file = st.file_uploader("Upload a PDF Resume", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("📄 Extracted Resume Text")
    st.text_area("Raw Text", resume_text, height=300)

    skill_list = load_skills()
    extracted = {
        "Name": "John Doe",  # You can use regex to extract name/email/phone
        "Email": "john.doe@example.com",
        "Phone": "+91-9876543210",
        "skills": extract_skills(resume_text, skill_list),
    }

    st.subheader("✅ Extracted Info")
    st.json(extracted)
