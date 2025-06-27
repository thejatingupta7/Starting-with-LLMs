# vectorstore_builder.py
# ------------------
# Script to load PDF documents, split into chunks, embed them, and build a FAISS vectorstore

import os
import sys
from langchain_utils import (
    load_and_split_all_pdfs_in_folder,
    load_embedding_model,
    create_embeddings
)

# === Configuration: set your paths here ===
PDF_FOLDER = "data"             # Folder with your PDF files
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # HuggingFace embedding model name
OUTPUT_FOLDER = "vectorstore"        # Directory to save the FAISS vectorstore

# === Preliminary checks ===
if not os.path.isdir(PDF_FOLDER):
    print(f"Error: PDF folder '{PDF_FOLDER}' does not exist or is not a directory.")
    sys.exit(1)

pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]
print(f"Found {len(pdf_files)} PDF(s) in '{PDF_FOLDER}': {pdf_files}")
if not pdf_files:
    print("No PDF files to process. Exiting.")
    sys.exit(0)

# === Execution: build the vectorstore ===
print(f"✅ Loading and splitting PDFs from '{PDF_FOLDER}'...")
chunks = load_and_split_all_pdfs_in_folder(PDF_FOLDER)
print(f"  • Total chunks created: {len(chunks)}")

print(f"✅ Loading embedding model '{EMBEDDING_MODEL}'...")
embedding_model = load_embedding_model(EMBEDDING_MODEL)

print("Creating FAISS vectorstore and saving to disk...")
create_embeddings(chunks, embedding_model, storing_path=OUTPUT_FOLDER)
print(f"✅ Vectorstore saved at '{OUTPUT_FOLDER}'")
