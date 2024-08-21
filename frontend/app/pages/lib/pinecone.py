from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from io import BytesIO
from tempfile import mkdtemp

INDEX_NAME = "docs-rag-chatbot"
EMBEDDING_MODEL = 'text-embedding-3-large'

def get_index():
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=1024, 
            metric="cosine", 
            spec=ServerlessSpec(
                cloud="aws", 
                region="us-east-1"
            ) 
        ) 
    return pc.Index(INDEX_NAME)    

def stream_to_file( io_stream : BytesIO)->str:
    
    
    path = os.path.join(mkdtemp(), io_stream.name)
    io_stream.seek(0)
    with open(path, "wb") as f:
        f.write(io_stream.read())
    
    return path

def load_document(file: str):
    _, extension = os.path.splitext(file) 
    if extension == '.txt':
        loader = TextLoader(file)
    elif extension == '.pdf':
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        loader = Docx2txtLoader(file)
    else:
        Exception('The document format is not supported!')


    data = loader.load()
    return data

def store_documents(index, docs, filename):
    vec_store = PineconeVectorStore(index, embedding=OpenAIEmbeddings( model=EMBEDDING_MODEL ))
    vec_store.add_documents(docs, ids=[ f'{filename}:{i}'for i in range(len(docs))] )

def get_retriever(index):
    vec_store = PineconeVectorStore(index, embedding=OpenAIEmbeddings( model=EMBEDDING_MODEL ))
    return vec_store.as_retriever(kwargs={ 'k': 2, 'threshold': 0.5 })

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain(pc_index):
    retriever = get_retriever(pc_index)
    prompt_template = ChatPromptTemplate.from_template(
        """You are an assistant for question-answering tasks. Use the following pieces of retrieved 
        context to answer the question. If you don't know the answer, just say that you don't know.   
        Question: {question} 
        Context: {context}  
        Answer:""")
    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | ChatOpenAI()
        | StrOutputParser()
    )

def clear_index(pc_index):
    pc_index.delete(delete_all=True, namespace='')