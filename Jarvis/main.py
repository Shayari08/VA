import requests
# from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
# from pprint import pprint
# from jarvis import speak, greet_user, take_user_input
#from face import main as face_recognition_main
# import utils
from PyPDF2 import PdfFileReader
import numpy as np
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
# import InstructorEmbedding
# from langchain.embeddings import InstructorEmbedding
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub

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
        length_function=len
    )
    chunks=text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding = embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.5, "max_length": 512})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        vectorstore=vectorstore  # You might need to pass the vectorstore here
    )
    
    return conversation_chain

if __name__ == '__main__':
    #face_recognition_main()
    # greet_user()
    st.text_input("Ask a question")
    with st.sidebar:
        st.subheader("Documents")
        pdf_docs = st.file_uploader("Upload Documents here", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                #get pdf text
                raw_text = get_pdf_text(pdf_docs)
                st.write(raw_text)
                #get text chunks
                text_chunks = get_text_chunks(raw_text)
                #create vector store
                vectorstore = get_vectorstore(text_chunks)
                #create conversation chain
                conversation = get_conversation_chain(vectorstore)
    # while True:
    #     query = take_user_input().lower()

    #     if 'open notepad' in query:
    #         open_notepad()

    #     elif 'open discord' in query:
    #         open_discord()

    #     elif 'open command prompt' in query or 'open cmd' in query:
    #         open_cmd()

    #     elif 'open camera' in query:
    #         open_camera()

    #     elif 'open calculator' in query:
    #         open_calculator()

    #     elif 'ip address' in query:
    #         ip_address = find_my_ip()
    #         speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen.')
    #         print(f'Your IP Address is {ip_address}')
        
