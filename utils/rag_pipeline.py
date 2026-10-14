"""
RAG (Retrieval Augmented Generation) Pipeline using LangChain and FAISS.
Implements real vector search and document retrieval.

KEY CONCEPTS:
- Chunking: Documents split into manageable pieces
- Embeddings: Text converted to vectors using HuggingFaceEmbeddings
- Vector Store: FAISS for similarity search
- Retriever: Fetches relevant chunks
- LCEL: LangChain Expression Language for composing chains
- RAG: Retrieves context and passes to LLM for answer generation
"""

import os
from pathlib import Path
import pickle

from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from utils.groq_helper import get_groq_llm
from utils.prompts import RAG_CONTEXT_PROMPT


class RAGPipeline:
    """
    Manages the complete RAG workflow:
    1. Document loading (PDFs)
    2. Text chunking
    3. Embedding generation
    4. Vector store creation (FAISS)
    5. Retrieval and answer generation using LCEL
    """
    
    def __init__(self, vectorstore_path: str = "vectorstore"):
        """
        Initialize RAG pipeline.
        
        Args:
            vectorstore_path (str): Path to store FAISS index
        """
        self.vectorstore_path = vectorstore_path
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        
        # Create vectorstore directory if it doesn't exist
        os.makedirs(vectorstore_path, exist_ok=True)
        
        # Initialize embeddings
        # EMBEDDINGS USAGE: HuggingFaceEmbeddings converts text to vectors
        self._init_embeddings()
    
    def _init_embeddings(self):
        """Initialize HuggingFace embeddings model."""
        try:
            # Uses 'all-MiniLM-L6-v2' by default - fast and effective
            self.embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"}
            )
        except Exception as e:
            print(f"Error initializing embeddings: {e}")
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            str: Extracted text
        """
        try:
            text = ""
            pdf_reader = PdfReader(pdf_path)
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def process_documents(self, documents: list) -> list:
        """
        Process and chunk documents.
        
        CHUNKING STRATEGY:
        - Splits on multiple separators (paragraphs, sentences, words)
        - Chunk size: 1000 characters
        - Overlap: 200 characters (for context preservation)
        
        Args:
            documents (list): List of document texts
            
        Returns:
            list: Processed chunks
        """
        # LANGCHAIN TEXT SPLITTER: RecursiveCharacterTextSplitter
        # This is KEY RAG COMPONENT: Intelligently chunks text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        all_chunks = []
        for doc in documents:
            if doc:  # Only process non-empty documents
                chunks = text_splitter.split_text(doc)
                all_chunks.extend(chunks)
        
        return all_chunks
    
    def create_vectorstore(self, pdf_files: list) -> bool:
        """
        Create FAISS vectorstore from PDF files.
        
        PROCESS:
        1. Extract text from PDFs
        2. Split into chunks
        3. Generate embeddings for each chunk
        4. Store in FAISS index
        5. Save to disk
        
        Args:
            pdf_files (list): List of PDF file paths
            
        Returns:
            bool: Success status
        """
        try:
            if not self.embeddings:
                print("Embeddings not initialized")
                return False
            
            # Extract text from all PDFs
            documents = []
            for pdf_path in pdf_files:
                if os.path.exists(pdf_path):
                    text = self.extract_pdf_text(pdf_path)
                    if text:
                        documents.append(text)
            
            if not documents:
                print("No documents extracted")
                return False
            
            # CHUNKING: Split documents into manageable pieces
            chunks = self.process_documents(documents)
            
            if not chunks:
                print("No chunks created")
                return False
            
            # VECTOR STORE CREATION: FAISS is a vector similarity search library
            # EMBEDDINGS USAGE: Each chunk is converted to a vector
            self.vectorstore = FAISS.from_texts(
                texts=chunks,
                embedding=self.embeddings
            )
            
            # RETRIEVER: Create retriever for similarity search
            # This is crucial for RAG: retriever fetches relevant chunks
            self.retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Return top 3 relevant chunks
            )
            
            # Save vectorstore to disk
            self._save_vectorstore()
            
            print(f"✅ Vectorstore created with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            print(f"Error creating vectorstore: {e}")
            return False
    
    def _save_vectorstore(self):
        """Save FAISS vectorstore to disk."""
        try:
            if self.vectorstore:
                index_path = os.path.join(self.vectorstore_path, "faiss_index")
                self.vectorstore.save_local(index_path)
                print(f"Vectorstore saved to {index_path}")
        except Exception as e:
            print(f"Error saving vectorstore: {e}")
    
    def load_vectorstore(self) -> bool:
        """Load FAISS vectorstore from disk."""
        try:
            index_path = os.path.join(self.vectorstore_path, "faiss_index")
            if os.path.exists(index_path):
                # LOAD FAISS: Restore vectorstore from disk
                self.vectorstore = FAISS.load_local(
                    index_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                # Create retriever
                self.retriever = self.vectorstore.as_retriever(
                    search_kwargs={"k": 3}
                )
                print("✅ Vectorstore loaded from disk")
                return True
            else:
                print("No saved vectorstore found")
                return False
        except Exception as e:
            print(f"Error loading vectorstore: {e}")
            return False
    
    def retrieve_relevant_documents(self, query: str) -> list:
        """
        Retrieve relevant document chunks for a query.
        
        RETRIEVAL PROCESS:
        1. Convert query to embedding vector
        2. Search FAISS for similar chunk vectors
        3. Return top-k most similar chunks
        
        Args:
            query (str): User question
            
        Returns:
            list: List of relevant chunks
        """
        if not self.retriever:
            print("Retriever not initialized")
            return []
        
        try:
            # RETRIEVER: Fetch documents similar to query
            # This is core RAG: retrieve relevant context
            docs = self.retriever.invoke(query)
            return [doc.page_content for doc in docs]
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
    
    def build_rag_chain(self):
        """
        Build LCEL RAG chain.
        
        LCEL (LangChain Expression Language) CHAIN:
        This is a key requirement - demonstrates LCEL usage.
        
        Chain flow:
        {
            "context": retriever.invoke(question),  # Fetch relevant chunks
            "question": RunnablePassthrough()        # Pass through the question
        }
        | prompt_template        # Format with prompt
        | llm                     # Call Groq
        
        This elegant composition shows RAG in action.
        
        Returns:
            Runnable: LCEL chain
        """
        if not self.retriever:
            print("Retriever not initialized")
            return None
        
        try:
            # Initialize LLM
            llm = get_groq_llm()
            
            # LCEL PROMPT TEMPLATE
            prompt = PromptTemplate.from_template(RAG_CONTEXT_PROMPT)
            
            # LCEL CHAIN COMPOSITION
            # This demonstrates LangChain Expression Language (LCEL)
            # The pipe (|) operator chains components elegantly
            rag_chain = (
                {
                    # RETRIEVAL: For each question, retrieve relevant context
                    "context": self.retriever,
                    # PASS-THROUGH: Keep question as-is
                    "question": RunnablePassthrough()
                }
                | prompt    # Format the retrieved context and question
                | llm       # Call Groq with formatted prompt
            )
            
            print("✅ LCEL RAG chain built successfully")
            return rag_chain
            
        except Exception as e:
            print(f"Error building LCEL chain: {e}")
            return None
    
    def answer_question(self, question: str) -> str:
        """
        Answer user question using RAG pipeline.
        
        RAG WORKFLOW:
        1. Retrieve relevant document chunks
        2. Create prompt with context
        3. Send to LLM (Gemini)
        4. Return AI-generated answer
        
        Args:
            question (str): User question
            
        Returns:
            str: AI-generated answer
        """
        try:
            if not self.retriever:
                return "Knowledge base not loaded. Please upload PDF documents first."
            
            # Build RAG chain using LCEL
            rag_chain = self.build_rag_chain()
            
            if not rag_chain:
                return "Error building RAG chain"
            
            # INVOKE THE LCEL CHAIN
            # This executes: retrieval -> prompt formatting -> LLM call
            response = rag_chain.invoke(question)
            
            # Extract text from response
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
                
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def get_vectorstore_status(self) -> dict:
        """Get status of vectorstore."""
        return {
            "initialized": self.vectorstore is not None,
            "has_retriever": self.retriever is not None,
            "embeddings_model": "all-MiniLM-L6-v2" if self.embeddings else None
        }
