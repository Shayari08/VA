from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="JARVIS Document Chat", page_icon="🤖", layout="wide")


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return text_splitter.split_text(text)


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)


def get_conversation_chain(vectorstore):
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl",
        model_kwargs={"temperature": 0.5, "max_length": 512},
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),  # was: vectorstore= (wrong param)
        memory=memory,
    )


# ── Session state defaults ────────────────────────────────────────────────────

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ── Sidebar: upload & process ─────────────────────────────────────────────────

with st.sidebar:
    st.title("🤖 JARVIS")
    st.subheader("Documents")
    pdf_docs = st.file_uploader(
        "Upload PDFs here", accept_multiple_files=True, type="pdf"
    )
    if st.button("Process"):
        if not pdf_docs:
            st.warning("Please upload at least one PDF first.")
        else:
            with st.spinner("Processing documents…"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.session_state.chat_history = []
            st.success("Done! Ask me anything about your documents.")


# ── Main: chat interface ──────────────────────────────────────────────────────

st.header("Chat with your documents")

# Render existing chat history
for message in st.session_state.chat_history:
    role = "user" if message.type == "human" else "assistant"
    with st.chat_message(role):
        st.write(message.content)

# Accept new question
user_question = st.chat_input("Ask a question about your documents…")
if user_question:
    if st.session_state.conversation is None:
        st.warning("Please upload and process your documents first (use the sidebar).")
    else:
        with st.chat_message("user"):
            st.write(user_question)

        with st.spinner("Thinking…"):
            response = st.session_state.conversation({"question": user_question})
            st.session_state.chat_history = response["chat_history"]

        # Show the latest assistant reply
        with st.chat_message("assistant"):
            st.write(st.session_state.chat_history[-1].content)
