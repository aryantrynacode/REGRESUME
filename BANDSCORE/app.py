import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Resume Skill Extractor")
st.title("📄 Resume Skill Extractor")

# Load skill list
with open("skills.txt") as f:
    skill_list = [line.strip().lower() for line in f.readlines()]

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_details(text):
    name = re.findall(r"(?i)([A-Z][a-z]+ [A-Z][a-z]+)", text[:100])[0] if text else "Not found"
    email = re.findall(r"\b[\w.-]+?@\w+?\.\w+?\b", text)
    phone = re.findall(r"\+?\d[\d\-\(\) ]{8,}\d", text)

    found_skills = [skill for skill in skill_list if skill in text.lower()]
    
    return {
        "Name": name,
        "Email": email[0] if email else "Not found",
        "Phone": phone[0] if phone else "Not found",
        "Skills": found_skills
    }

uploaded_file = st.file_uploader("Upload a PDF Resume", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.subheader("📄 Extracted Resume Text")
    st.text_area("Raw Text", text, height=300)

    results = extract_details(text)
    
    st.subheader("✅ Extracted Info")
    st.write(results)
