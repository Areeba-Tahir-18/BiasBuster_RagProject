
import streamlit as st
import os
from dotenv import load_dotenv
from data_intake.file_loader import load_file
from db.chromedb import store_in_chroma
from langchain.schema import Document
from makeChain.mychain import get_doc_qa_chain
from core.bias_detection import (
    detect_bias,
    compute_bias_score,
    fact,
    generate_rewrite_suggestions,
)


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


os.makedirs("temp", exist_ok=True)


st.set_page_config(page_title="BiasBuster", layout="wide")


if "history" not in st.session_state:
    st.session_state.history = []
if "doc_retriever" not in st.session_state:
    st.session_state.doc_retriever = None
if "uploaded_text" not in st.session_state:
    st.session_state.uploaded_text = ""
if "input_mode" not in st.session_state:
    st.session_state.input_mode = None
if "show_qa" not in st.session_state:
    st.session_state.show_qa = False
    
    
st.markdown("""
    <style>
    div.stButton > button {
        padding: 8px 12px;
        font-size: 12px;
        height: auto;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <h1 style='text-align: center; font-size: 60px; font-weight: bold; color: #ff4b4b; margin-bottom: 10px;'>BiasBuster 💥</h1>
""", unsafe_allow_html=True)

if st.session_state.input_mode is None:
    st.markdown("""
        <p style='text-align: center; font-size: 18px;'>Select an input method</p>
    """, unsafe_allow_html=True)


if st.session_state.input_mode is None:
    col_space1, col_buttons, col_space2 = st.columns([3, 2, 3])
    with col_buttons:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Enter Text"):
                st.session_state.input_mode = "text"
        with col2:
            if st.button("Upload File"):
                st.session_state.input_mode = "file"
    st.stop()

st.sidebar.markdown("<span style='color:#ff4b4b; font-size:24px; font-weight:bold;'>💬 Chat History</span>", unsafe_allow_html=True)
if st.session_state.history:
    st.sidebar.markdown("---")
    for i, item in enumerate(reversed(st.session_state.history[-5:])):
        with st.sidebar.expander(f"{item['type'].capitalize()} #{len(st.session_state.history) - i}"):
            st.sidebar.write("**Input:**", item["input"][:100] + "...")
            if item["type"] == "bias_analysis":
                st.sidebar.write("**Bias Score:**", item["score"])
            elif item["type"] == "correction":
                st.sidebar.write("**Corrected:**", item["correction"][:100] + "...")
            elif item["type"] == "doc_chat":
                st.sidebar.write("**Response:**", item["response"][:100] + "...")

user_input = ""
full_text = ""
uploaded_file = None
analyze_btn = correct_btn = qa_btn = False

if st.session_state.input_mode == "text":
    col_input, col_actions = st.columns([3, 1])
    with col_input:
        user_input = st.text_area("Enter your text here:", height=250)
    with col_actions:
        
        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

        analyze_btn = st.button("Analyze Bias", key="analyze_text")
        correct_btn = st.button("Correct Content", key="correct_text")
        qa_btn = st.button("Ask Question", key="ask_text")
    full_text = user_input


# FILE MODE
elif st.session_state.input_mode == "file":
    col_input, col_actions = st.columns([3, 1])
    with col_input:
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx", "csv", "eml", "md"])
        if uploaded_file:
            file_path = os.path.join("temp", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            content = load_file(file_path)
            st.session_state.uploaded_text = content

            with st.spinner("Indexing document..."):
                docs = [Document(page_content=content)]
                retriever = store_in_chroma(docs)
                st.session_state.doc_retriever = retriever
    with col_actions:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        analyze_btn = st.button("Analyze Bias", key="analyze_file")
        correct_btn = st.button("Debug Content", key="correct_file")
        qa_btn = st.button("Ask Question", key="ask_file")
    full_text = st.session_state.uploaded_text


if full_text:
    if analyze_btn:
        with st.spinner("Analyzing bias..."):
            bias_result = detect_bias(full_text)
            score = compute_bias_score(full_text)
            suggestions = generate_rewrite_suggestions(
                bias_result.split("\n")
            ) if "No bias" not in bias_result else "No suggestions needed."

        st.session_state.history.append({
            "type": "bias_analysis",
            "input": full_text,
            "bias": bias_result,
            "score": score,
            "suggestions": suggestions
        })

        st.markdown("### 📋 Detected Bias")
        st.code(bias_result)

        st.markdown("### 📊 Bias Score")
        st.success(f"Bias Score: *{score}/100*")

        st.markdown("### ✍ Suggested Rewrite")
        st.code(suggestions)

    if correct_btn:
        with st.spinner("Checking factual accuracy..."):
            correction_result = fact(full_text)

        st.session_state.history.append({
            "type": "correction",
            "input": full_text,
            "correction": correction_result
        })

        st.markdown("Debug Content")
        st.code(correction_result)

    if qa_btn:
        st.session_state.show_qa = True
        
        
if st.session_state.show_qa and st.session_state.doc_retriever:
    st.markdown("<h4 style='color:#FF4B4B;'>📥 Ask a Question</h4>", unsafe_allow_html=True)
    doc_query = st.text_input("", key="doc_question")
    if doc_query:
        with st.spinner("Answering..."):
            qa_chain = get_doc_qa_chain(st.session_state.doc_retriever)
            doc_response = qa_chain.run(doc_query)

        st.session_state.history.append({
            "type": "doc_chat",
            "input": doc_query,
            "response": doc_response
        })

        st.write(doc_response)
