from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

import streamlit as st

FEW_SHOT_PROMPT = """
You are a film critic and you are writing a review index based on user test description. Answer only with
the review index. Revire index is a number between 1 and 5, where 1 is the worst and 5 is the best.

Examples:
User: "The movie was great, I loved the action scenes!"
Answer: 5

User: "The movie was boring and the acting was terrible."
Answer: 1

User: "The movie was okay, but the ending was disappointing."
Answer: 3

User: {question}
"""



def get_response(chain, prompt , config):
    return chain.stream({"question": prompt}, config)

st.write("## Tuneable Few Shots Movie Critique Chatbot")

col1, col2 = st.columns([1, 2])
with col1:
    system_prompt = st.text_area("System Prompt", FEW_SHOT_PROMPT, height=200)
    st.button("Clear History", on_click=lambda: msgs.clear())
with col2:
    st.text("ID of the model to use")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4", "gpt-4o" ])
    st.text("What sampling temperature to use, between 0 and 2.", help="Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05)
    max_token = st.number_input("Max Tokens", 1, 2048, 1024, 1 , help="The maximum number of tokens to generate in the response. Depends on the model")

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")

# Set up the LangChain, passing in Message History
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}"),
    ]
)
model_params = dict(model=model, temperature=temperature, max_tokens=max_token)
llm_model = ChatOpenAI(**model_params)
chain = prompt | llm_model


# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    st.chat_message("ai").write_stream(chain.stream({"question": prompt}, config))
