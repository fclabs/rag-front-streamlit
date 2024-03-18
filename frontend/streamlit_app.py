
import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

if st.checkbox('Enter your name'):
    st.text_input("Your name", key="name")
    # You can access the value at any point with:
    st.write( "Name:", st.session_state.name)