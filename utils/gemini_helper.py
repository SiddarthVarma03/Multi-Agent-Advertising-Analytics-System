"""
Gemini API helper functions.
Handles API initialization and LLM interactions.

This module uses Google's Generative AI API (Gemini).
Key LLM usage: ChatGoogleGenerativeAI from langchain-google-genai
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# ==================== LLM INITIALIZATION ====================

def get_gemini_llm():
    """
    Initialize and return Gemini LLM instance.
    
    This is where the LLM (Large Language Model) is configured.
    Uses gemini-1.5-flash for faster, cost-effective responses.
    
    Returns:
        ChatGoogleGenerativeAI: Initialized Gemini model
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in .env file. "
            "Please set your Google API key in .env"
        )
    
    # Initialize Gemini LLM
    # KEY LLM USAGE: This is how we create the language model instance
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.7,
        convert_system_message_to_human=True
    )
    
    return llm


def generate_response(prompt: str) -> str:
    """
    Generate a response from Gemini API.
    
    Args:
        prompt (str): The prompt to send to Gemini
        
    Returns:
        str: Generated response from the model
    """
    try:
        llm = get_gemini_llm()
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
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        status["message"] = "❌ GOOGLE_API_KEY not configured in .env"
        return status
    
    status["api_key_present"] = True
    
    try:
        llm = get_gemini_llm()
        # Try a simple inference to verify API works
        test_response = llm.invoke("Say 'OK'")
        if test_response:
            status["configured"] = True
            status["message"] = "✅ Gemini API is configured and working"
        else:
            status["message"] = "❌ API returned empty response"
    except Exception as e:
        status["message"] = f"❌ API Error: {str(e)}"
    
    return status
