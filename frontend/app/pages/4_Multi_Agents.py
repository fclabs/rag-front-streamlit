from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from pages.lib.agents import get_multi_agent
from langchain_core.messages import BaseMessage, HumanMessage
import streamlit as st

st.set_page_config(layout="wide")

magent = get_multi_agent()
    
st.write("## Multi Agent Chatbot")
st.write("Write where do you want to go for vacation or ask the bot for suggestions")
# If user inputs a new prompt, generate and draw a new response
if user_input := st.chat_input():
    st.chat_message("human").write(user_input)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {}
    response = magent.invoke(
            {"messages": [HumanMessage(user_input)],
             }, config
        )
    for msg in response["messages"][1:]:
        st.chat_message("ai").write( msg.content )
        
