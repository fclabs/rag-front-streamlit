# LLM Demo App

## Setup

To use this app you need to setup your own API key to test the app. You can do this going to the `Start Here` section in the sidebar and adding the following API keys:
* `OpenAi API Key`: You can get one [here](https://platform.openai.com/signup). Read from OPENAI_API_KEY environment variable.
* `Pinecone API Key`: You can get one [here](https://www.pinecone.io/). Read from PINECONE_API_KEY environment variable.

Remember to press press ENTER to save the values. 

TIP: You can set these variables in the `.env` file in the app folder (frontend/app) to avoid setting them every time you run the app.

## Functionalities

1. **RAG**: You can use this functionality to generate answers to questions using the RAG model. You can upload files and they are going to be added to a Pinecone Index. The RAG model is going to use this index to generate answers to questions. If it cannot answer it just say that it doesn't know the answer.
2. **Chat with History**: You can use this functionality to generate text using short-term memory, stored in streamlit session state.
3. **Tuneable model**: You can use this functionality to generate text using a model that you can tune using the sliders and selection boxes. Also you can see here streaming integrated in the front end.
4. **MultiAgent Chat**: You can use this functionality to chat with multiple agents at the same time.
5. **Documentation**: You can access README files.