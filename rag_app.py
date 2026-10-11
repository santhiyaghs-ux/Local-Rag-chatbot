
import streamlit as st
import ollama
from pypdf import PdfReader

st.set_page_config(page_title="My RAG Chatbot")
st.title("My RAG Chatbot")
st.write("Upload a PDF or TXT file and ask questions.")

uploaded_file = st.file_uploader(
    "Upload your book or notes",
    type=["pdf", "txt"]
)

if uploaded_file:
    if uploaded_file.name.lower().endswith(".txt"):
        text = uploaded_file.getvalue().decode(
            "utf-8", errors="ignore"
        )
    else:
        reader = PdfReader(uploaded_file)
        text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )

    st.success("File uploaded successfully!")

    if text.strip():
        question = st.text_input("Ask a question about your file")

        if st.button("Get Answer") and question.strip():
            prompt = f"""
Use the document to answer the question in simple English.
Explain word meanings even if the question uses different wording.
If the document lacks the answer, say so and give a general
definition when appropriate.

DOCUMENT:
{text[:12000]}

QUESTION:
{question}
"""
            try:
                with st.spinner("Thinking..."):
                    response = ollama.chat(
                        model="llama3.2:1b",
                        messages=[{"role": "user", "content": prompt}]
                    )
                st.write(response["message"]["content"])
            except Exception as e:
                st.error(f"Ollama error: {e}")
    else:
        st.warning("No readable text was found in this file.")
