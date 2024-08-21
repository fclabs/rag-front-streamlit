import streamlit as st
from utils.files import read_file_text


README_PATH = "app/pages/Documentation.md"

st.markdown(read_file_text(README_PATH))