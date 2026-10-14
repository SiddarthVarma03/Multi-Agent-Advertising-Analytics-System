"""
Groq API helper functions.
Handles API initialization and LLM interactions.

This module uses Groq's LLM API (llama3-8b-8192).
Key LLM usage: ChatGroq from langchain-groq
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# ==================== LLM INITIALIZATION ====================

def get_groq_llm():
    """
    Initialize and return Groq LLM instance.
    
    This is where the LLM (Large Language Model) is configured.
    Uses llama3-8b-8192 for fast, cost-effective responses.
    
    Returns:
        ChatGroq: Initialized Groq model
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in .env file. "
            "Please set your Groq API key in .env"
        )
    # Initialize Groq LLM
    # KEY LLM USAGE: This is how we create the language model instance
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        groq_api_key=api_key,
        temperature=0.3
    )

    return llm


def generate_response(prompt: str) -> str:
    """
    Generate a response from Groq API.
    
    Args:
        prompt (str): The prompt to send to Groq
        
    Returns:
        str: Generated response from the model
    """
    try:
        llm = get_groq_llm()
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating response: {str(e)}"


def check_api_status() -> dict:
    """
    Check if API is properly configured and accessible.
    
    Returns:
        dict: Status information
    """
    status = {
        "configured": False,
        "message": "",
        "api_key_present": False
    }
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        status["message"] = "❌ GROQ_API_KEY not configured in .env"
        return status
    
    status["api_key_present"] = True
    
    try:
        llm = get_groq_llm()
        # Try a simple inference to verify API works
        test_response = llm.invoke("Say 'OK'")
        if test_response:
            status["configured"] = True
            status["message"] = "✅ Groq API is configured and working"
        else:
            status["message"] = "❌ API returned empty response"
    except Exception as e:
        status["message"] = f"❌ API Error: {str(e)}"
    
    return status
