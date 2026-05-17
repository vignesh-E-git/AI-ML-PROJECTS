from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
load_dotenv(r'C:\VKY\02_SKILLS\LANGHAIN\LEVEL-2\.env')

from main import Agent
DEBUG = True

def debug_print(message: str) -> None:
    if DEBUG:
        print(f'[DEBUG] {message}')

def create_db(path):
    debug_print(f'create_db started for PDF path: {path}')

    # load pdf
    pdf_loader = PyPDFLoader(path)
    pdf = pdf_loader().load()
    debug_print(f'PDF loaded successfully. Pages/documents found: {len(pdf)}')

    # chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 400 ,
        chunk_overlap = 50
    )
    chunks = text_splitter.split_documents(pdf)
    debug_print(f'Document split completed. Total chunks created: {len(chunks)}')

    # embedding
    debug_print('Creating embeddings and storing documents in Chroma vector DB.')
    embedding_model = GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-2')
    vector_db = Chroma.from_documents(
        embedding=embedding_model ,
        documents= chunks ,
        persist_directory= 'MY_PROJECTS-main/RAG' ,
        collection_name= 'pdf_data'
    )
    debug_print('Vector DB created successfully.')
    return vector_db



print('=====WELCOME TO CLI RAG AGENT======\n\n')

path = input('Enter the pdf path :')

db = create_db(r'{path}')


query = input('Ask you question :')
while query != 'exit':
    result = Agent(query)
    print(f'Answer : {result}')
    query = input('Ask you question :')




