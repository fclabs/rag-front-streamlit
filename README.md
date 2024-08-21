# Readme

## LTDR;

This project show how to use LLMs for different tasks. It use Streamlit as frontend and LangChain and OpenAi as backend. 

## How to run

### Requirements

You need to have docker and docker-compose (if you are using an old version of docker) installed in your machine.
To use the system, you need to have an OpenAi API key. You can get one [here](https://platform.openai.com/signup).
The key needs to be loaded in the app using the `Start Here` section in the sidebar.

### Running

To run the project, you need to run the following command in the repo root:

```bash
docker compose up --build
```

After that, you can access the project in your browser at `http://localhost:8501`.

## Testing

To run the tests, you need to run the following command:

```bash
cd frontend
poetry run python -m pytest
```

## Sample files references

The sample files are taken from the following sources:
* AI-for-Education-RAG: [AI for Education](https://ai-for-education.org/wp-content/uploads/2024/03/AI-for-Education-RAG.pdf)
* alice.txt: [Project Gutenberg](https://www.gutenberg.org/ebooks/11)
* ArtOfWar-SunTzu.docx: Exported to Docs from [Project Gutenberg](https://www.gutenberg.org/ebooks/132)