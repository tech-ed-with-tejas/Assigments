# 01-06-2025 Directory -Assigment 4 RAG 

This directory contains all the necessary files and scripts to build and manage a Retrieval-Augmented Generation (RAG) system. The project is designed to process unstructured PDF data, convert it into vector embeddings, store it in a local vector store, and retrieve relevant information based on user queries.

## Files and Directories

- **`src/`**: Contains all the core code required for the RAG system.
  - **`ProcessPDF` and `DataProcessor` classes**: Used to read PDFs from an unstructured library and convert them into vector embeddings.
  - **Embedding class**: Handles the creation of vector embeddings from text or PDF content.
  - **Local Chroma Manager**: Manages the storage of PDF embeddings in a local vector store and facilitates retrieval. Fetches data from the vector store by converting input strings into embeddings, searching the database, and returning relevant results.

- **`db_updatetion_from_pdf.ipynb`**: A Jupyter Notebook used to process PDFs, generate embeddings, and update the local vector store.

- **`rag.py`**: Implements a RAG agent that uses the vector store to answer questions based on the available context.

- **`main.py`**: A Streamlit application that provides a user interface for querying the RAG system. It supports input as a string, converts it into embeddings, searches the vector store, and returns answers.


- **`pyproject.toml`**: Configuration file for managing dependencies and project settings.
- **`uv.lock`**: Lock file for dependency management.

## Workflow

1. **PDF Processing**:
   - Use the `ProcessPDF` and `DataProcessor` classes to read unstructured PDFs and convert them into vector embeddings.
   - Store the embeddings in the local vector store using the `LocalChromaManager` and `Embeddings`.

2. **Data Retrieval**:
   - Use the Retriever class to fetch relevant data from the vector store by converting input strings into embeddings and searching the database.

3. **RAG Agent**:
   - The `rag.py` file implements a RAG agent that uses the vector store to answer questions based on the stored context.

4. **Streamlit Application**:
   - The `main.py` file provides a user-friendly interface for querying the RAG system.

## Requirements

- Python 3.8 or higher
- Dependencies listed in `pyproject.toml`

