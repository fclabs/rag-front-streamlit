import streamlit as st
from pages.lib.common import load_sample_files

from langchain_text_splitters import RecursiveCharacterTextSplitter

from pages.lib.pinecone import (
    get_index,
    stream_to_file,
    load_document,
    store_documents,
    INDEX_NAME,
    create_rag_chain, clear_index
)

SAMPLE_FILES_PATH = "app/sample_files"

\
@st.cache_data
def load_contents(files, path):
    file_content = []
    for f in files:
        with open(f"{path}/{f}", "rb") as file:
            file_content.append(file.read())
    return file_content


st.set_page_config(layout="wide")

## Access The Pinecone index
try:
    pc_index = get_index()
except Exception as e:
    st.write(f"Error accesing pinecone: {e}")
    st.stop()


col1, col2 = st.columns([1, 1])
with col1:
    st.write("## Sample Files, or pick your own")
    files, ext = load_sample_files(SAMPLE_FILES_PATH)
    file_content = load_contents(files, SAMPLE_FILES_PATH)
    ext_cols = st.columns(len(files))
    for i in range(len(files)):
        ext_cols[i].download_button(
            label=ext[i],
            data=file_content[i],
            file_name=files[i],
            mime="application/octet-stream",
        )

    st.write("## File Uploader")
    st.write("Upload a file PDF, Docx or txt to be processed.")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        ## Process the file
        try:
            file_path = stream_to_file(uploaded_file)

            docs = load_document(file_path)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200, add_start_index=True
            )
            all_splits = text_splitter.split_documents(docs)

            store_documents(pc_index, all_splits, uploaded_file.name)

        except Exception as e:
            st.write(f"Error processing file: {e}. Try another file.")
            st.stop()

with col2:
    stats = pc_index.describe_index_stats()
    st.write("## Pinecone Index Stats")
    st.write(f"Index Name: **{INDEX_NAME}**")
    st.write(stats)
    st.button("Clear DB", on_click=lambda: clear_index(pc_index))

## RAG Chatbot
st.divider()

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    rag_chain = create_rag_chain(pc_index)
    st.chat_message("human").write(prompt)

    ## Search for context in the knowledge base
    response = rag_chain.invoke(prompt)
    st.chat_message("ai").write(response)
