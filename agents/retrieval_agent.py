"""
Retrieval Agent: Responsible for document retrieval and RAG operations.

Part of the agentic AI workflow:
CSV Upload → Analytics Agent → Retrieval Agent → Recommendation Agent → Reporting Agent

This agent specifically handles:
- PDF document processing
- RAG pipeline management
- Document retrieval
- Knowledge base interactions
"""

import os
from typing import Optional, List
from utils.rag_pipeline import RAGPipeline


class RetrievalAgent:
    """
    Retrieval Agent for document management and RAG operations.
    
    Responsibilities:
    - Load and process PDF documents
    - Manage FAISS vectorstore
    - Retrieve relevant documents via RAG
    - Answer questions using retrieved context
    
    RAG IMPLEMENTATION: This agent demonstrates real RAG workflow:
    1. PDF upload → text extraction → chunking
    2. Embedding generation
    3. FAISS vectorstore creation
    4. Similarity-based retrieval
    5. LLM response generation
    """
    
    def __init__(self, vectorstore_path: str = "vectorstore"):
        """
        Initialize Retrieval Agent with RAG pipeline.
        
        Args:
            vectorstore_path (str): Path to store FAISS vectorstore
        """
        # RAG PIPELINE INITIALIZATION
        # This creates the vector store and embeddings
        self.rag_pipeline = RAGPipeline(vectorstore_path)
        self.loaded_documents = []
        self.vectorstore_ready = False
        
        # Try to load existing vectorstore
        self._load_existing_vectorstore()
    
    def _load_existing_vectorstore(self):
        """Load existing vectorstore if available."""
        if self.rag_pipeline.load_vectorstore():
            self.vectorstore_ready = True
    
    def process_pdf_documents(self, pdf_paths: List[str]) -> dict:
        """
        Process uploaded PDF documents and create vectorstore.
        
        RAG WORKFLOW:
        1. Extract text from PDFs (PyPDF2)
        2. Split into chunks (RecursiveCharacterTextSplitter)
        3. Generate embeddings (HuggingFaceEmbeddings)
        4. Store in FAISS vector database
        5. Create retriever for similarity search
        
        Args:
            pdf_paths (List[str]): List of PDF file paths
            
        Returns:
            dict: Processing results
        """
        try:
            if not pdf_paths:
                return {'success': False, 'message': 'No PDF files provided'}
            
            # Filter existing files
            valid_pdfs = [p for p in pdf_paths if os.path.exists(p)]
            
            if not valid_pdfs:
                return {'success': False, 'message': 'No valid PDF files found'}
            
            # Create vectorstore from PDFs
            # KEY RAG STEP: PDF → Chunks → Embeddings → FAISS
            success = self.rag_pipeline.create_vectorstore(valid_pdfs)
            
            if success:
                self.vectorstore_ready = True
                self.loaded_documents = valid_pdfs
                
                return {
                    'success': True,
                    'message': f'Successfully processed {len(valid_pdfs)} PDF(s)',
                    'documents_loaded': len(valid_pdfs)
                }
            else:
                return {'success': False, 'message': 'Failed to create vectorstore'}
                
        except Exception as e:
            return {'success': False, 'message': f'Error processing PDFs: {str(e)}'}
    
    def retrieve_documents(self, query: str, k: int = 3) -> dict:
        """
        Retrieve relevant document chunks for a query.
        
        RETRIEVAL PROCESS (FAISS + Embeddings):
        1. Convert query to vector embedding
        2. Search FAISS for similar chunk vectors
        3. Return top-k most relevant chunks
        
        Args:
            query (str): User query/question
            k (int): Number of chunks to retrieve
            
        Returns:
            dict: Retrieved documents with metadata
        """
        try:
            if not self.vectorstore_ready:
                return {
                    'success': False,
                    'message': 'Vectorstore not ready. Please upload PDF documents first.'
                }
            
            # RETRIEVE: Fetch relevant chunks
            # This uses FAISS similarity search
            documents = self.rag_pipeline.retrieve_relevant_documents(query)
            
            return {
                'success': True,
                'query': query,
                'retrieved_chunks': documents,
                'chunk_count': len(documents),
                'retrieval_method': 'FAISS + HuggingFace Embeddings'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Error retrieving documents: {str(e)}'}
    
    def answer_question_with_rag(self, question: str) -> dict:
        """
        Answer user question using RAG pipeline with LCEL.
        
        LCEL RAG CHAIN EXECUTION:
        {context: retriever | question: RunnablePassthrough()} | prompt | llm
        
        Args:
            question (str): User question
            
        Returns:
            dict: AI-generated answer with retrieved context
        """
        try:
            if not self.vectorstore_ready:
                return {
                    'success': False,
                    'answer': 'Knowledge base not initialized. Please upload PDF documents first.'
                }
            
            # Build and execute LCEL RAG chain
            # KEY: Retriever fetches context, LCEL chains components, Groq generates answer
            answer = self.rag_pipeline.answer_question(question)
            
            # Also retrieve context for transparency
            retrieved_docs = self.rag_pipeline.retrieve_relevant_documents(question)
            
            return {
                'success': True,
                'question': question,
                'answer': answer,
                'retrieved_context': retrieved_docs,
                'context_used': len(retrieved_docs) > 0
            }
            
        except Exception as e:
            return {'success': False, 'answer': f'Error: {str(e)}'}
    
    def get_vectorstore_info(self) -> dict:
        """
        Get information about current vectorstore.
        
        Returns:
            dict: Vectorstore status and metadata
        """
        status = self.rag_pipeline.get_vectorstore_status()
        
        return {
            'vectorstore_initialized': status['initialized'],
            'retriever_ready': status['has_retriever'],
            'embeddings_model': status['embeddings_model'],
            'documents_loaded': len(self.loaded_documents),
            'vectorstore_path': self.rag_pipeline.vectorstore_path,
            'storage_method': 'FAISS (vector similarity search)'
        }
    
    def get_knowledge_base_summary(self) -> str:
        """
        Get summary of loaded knowledge base.
        
        Returns:
            str: Summary text
        """
        if not self.vectorstore_ready:
            return "No knowledge base loaded. Please upload PDF documents."
        
        info = self.get_vectorstore_info()
        summary = f"""
        Knowledge Base Status:
        - Documents Loaded: {info['documents_loaded']}
        - Vectorstore Initialized: {info['vectorstore_initialized']}
        - Retriever Ready: {info['retriever_ready']}
        - Embeddings Model: {info['embeddings_model']}
        - Storage Method: {info['storage_method']}
        
        System ready for RAG queries using LCEL pipeline.
        """
        return summary
