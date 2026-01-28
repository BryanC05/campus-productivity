# Moonshot Kimi K2 Cloud API
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Moonshot API Configuration - works with both .env and Streamlit secrets
def get_api_key():
    """Get API key from Streamlit secrets or environment variables."""
    # Try Streamlit secrets first (for Streamlit Cloud)
    try:
        if hasattr(st, 'secrets') and 'MOONSHOT_API_KEY' in st.secrets:
            return st.secrets['MOONSHOT_API_KEY']
    except Exception:
        pass
    
    # Fall back to environment variable (for local development)
    return os.getenv("MOONSHOT_API_KEY")

MOONSHOT_BASE_URL = "https://api.moonshot.cn/v1"
MODEL = "kimi-k2-0711-preview"  # Latest Kimi K2 model


def get_client():
    """Get OpenAI-compatible client for Moonshot API."""
    api_key = get_api_key()
    if not api_key:
        raise ValueError("MOONSHOT_API_KEY not found. Set it in Streamlit secrets or .env file.")
    
    return OpenAI(
        api_key=api_key,
        base_url=MOONSHOT_BASE_URL
    )


def generate_content_moonshot(prompt: str, system_prompt: str) -> str:
    """Generate content using Moonshot Kimi K2 Cloud API."""
    client = get_client()
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4096
    )
    
    return response.choices[0].message.content


def generate_outline(topic: str) -> str:
    """Generate an assignment outline for the given topic."""
    system_prompt = """You are an academic assistant helping Indonesian university students. 
    Create detailed assignment outlines with clear sections, bullet points, and suggestions.
    Respond in the same language as the user's input (Indonesian or English)."""
    
    return generate_content_moonshot(
        f"Create a comprehensive outline for an assignment about: {topic}",
        system_prompt
    )


def generate_code_snippet(topic: str) -> str:
    """Generate code snippets for the given programming topic."""
    system_prompt = """You are a coding tutor for Indonesian university students.
    Generate clean, well-commented code snippets with explanations.
    Include examples and best practices. Use appropriate programming language based on context."""
    
    return generate_content_moonshot(
        f"Generate code snippets and examples for: {topic}",
        system_prompt
    )


def generate_essay_structure(topic: str) -> str:
    """Generate an essay structure for the given topic."""
    system_prompt = """You are an academic writing assistant for Indonesian university students.
    Create detailed essay structures with thesis statement, body paragraphs, and conclusion.
    Include suggested arguments, evidence to look for, and transition phrases.
    Respond in the same language as the user's input."""
    
    return generate_content_moonshot(
        f"Create a detailed essay structure for: {topic}",
        system_prompt
    )


def generate_content(topic: str, generation_type: str) -> str:
    """Main function to generate content based on type."""
    generators = {
        "outline": generate_outline,
        "code": generate_code_snippet,
        "essay": generate_essay_structure
    }
    
    generator = generators.get(generation_type)
    if not generator:
        raise ValueError(f"Unknown generation type: {generation_type}")
    
    return generator(topic)
