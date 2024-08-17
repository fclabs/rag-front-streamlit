from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

import streamlit as st

def get_response(chain, prompt , config):
    return chain.stream({"question": prompt}, config)

st.write("## Tuneable Chat with History")

col1, col2 = st.columns([1, 2])
with col1:
    system_prompt = st.text_area("System Prompt", "You are an AI chatbot having a conversation with a human.")
    st.button("Clear History", on_click=lambda: msgs.clear())
with col2:
    st.text("ID of the model to use")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4", "gpt-4o" ])
    st.text("What sampling temperature to use, between 0 and 2.", help="Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05)
    max_token = st.number_input("Max Tokens", 1, 2048, 1024, 1 , help="The maximum number of tokens to generate in the response. Depends on the model")

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# Set up the LangChain, passing in Message History
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)
model_params = dict(model=model, temperature=temperature, max_tokens=max_token)
llm_model = ChatOpenAI(**model_params)
chain = prompt | llm_model
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda _: msgs,
    input_messages_key="question",
    history_messages_key="history",
)

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    st.chat_message("ai").write_stream(chain_with_history.stream({"question": prompt}, config))
