# Importing the necessary packages
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
import textwrap
import os

# Function to load PDF data from a single file
def load_pdf_data(file_path):
    # Creating a PyMuPDFLoader object with file_path
    loader = PyMuPDFLoader(file_path=file_path)
    
    # Loading the PDF file
    docs = loader.load()
    
    # Returning the loaded document
    return docs

# Function to load and process all PDFs in a folder
def load_and_split_all_pdfs_in_folder(folder_path):
    all_docs = []
    
    # Iterating over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            docs = load_pdf_data(file_path)
            split_docs_list = split_docs(docs)  # Splitting the loaded docs
            all_docs.extend(split_docs_list)
    
    return all_docs

# Responsible for splitting the documents into several chunks
def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    
    # Initializing the RecursiveCharacterTextSplitter with
    # chunk_size and chunk_overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    # Splitting the documents into chunks
    chunks = text_splitter.split_documents(documents=documents)
    
    # returning the document chunks
    return chunks

# Function for creating embeddings using FAISS
def create_embeddings(chunks, embedding_model, storing_path="vectorstore"):
    # Creating the embeddings using FAISS
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    
    # Saving the model in current directory
    vectorstore.save_local(storing_path)
    
    # returning the vectorstore
    return vectorstore


# Prettifying the response
def get_response(query, chain):
    # Getting response from chain
    response = chain({'query': query})
    
    # Wrapping the text for better output in Jupyter Notebook
    wrapped_text = textwrap.fill(response['result'], width=100)
    return wrapped_text

def load_embedding_model(model_path, normalize_embedding=True):
    from langchain.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': normalize_embedding}
    )

def load_vector_store(storing_path="vectorstore", embedding_model=None):
    from langchain.vectorstores import FAISS
    return FAISS.load_local(
        storing_path,
        embedding_model,
        allow_dangerous_deserialization=True
    ).as_retriever(search_kwargs={"k": 2})

def load_qa_chain(retriever, llm, prompt):
    from langchain.chains import RetrievalQA
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
