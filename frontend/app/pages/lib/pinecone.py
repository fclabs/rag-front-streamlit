from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
from io import BytesIO
from tempfile import mkdtemp

INDEX_NAME = "docs-rag-chatbot"


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
    nombre, extension = os.path.splitext(file) 
    if extension == '.html':
        from langchain.document_loaders import UnstructuredHTMLLoader
        loader = UnstructuredHTMLLoader(file)
    elif extension == '.txt':
        from langchain.document_loaders import TextLoader  
        loader = TextLoader(file)
    elif extension == '.pdf':
        from langchain.document_loaders import PyPDFLoader
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        from langchain.document_loaders import Docx2txtLoader
        loader = Docx2txtLoader(file)
    else:
        print('The document format is not supported!')
        return None

    data = loader.load()
    return data