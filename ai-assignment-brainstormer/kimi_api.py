# AI API Configuration
# Supports: Moonshot, OpenRouter, and Groq
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def get_api_config():
    """Get API configuration from Streamlit secrets or environment variables."""
    # Try Streamlit secrets first (for Streamlit Cloud)
    try:
        if hasattr(st, 'secrets'):
            # Try different API providers in order of preference
            if 'OPENROUTER_API_KEY' in st.secrets:
                return {
                    'api_key': st.secrets['OPENROUTER_API_KEY'],
                    'base_url': 'https://openrouter.ai/api/v1',
                    'model': 'meta-llama/llama-3.2-1b-instruct:free'  # Free model
                }
            if 'MOONSHOT_API_KEY' in st.secrets:
                return {
                    'api_key': st.secrets['MOONSHOT_API_KEY'],
                    'base_url': 'https://api.moonshot.cn/v1',
                    'model': 'kimi-k2-0711-preview'
                }
            if 'GROQ_API_KEY' in st.secrets:
                return {
                    'api_key': st.secrets['GROQ_API_KEY'],
                    'base_url': 'https://api.groq.com/openai/v1',
                    'model': 'llama-3.1-70b-versatile'
                }

    except Exception:
        pass
    
    # Fall back to environment variables (for local development)
    if os.getenv("OPENROUTER_API_KEY"):
        return {
            'api_key': os.getenv("OPENROUTER_API_KEY"),
            'base_url': 'https://openrouter.ai/api/v1',
            'model': 'meta-llama/llama-3.2-1b-instruct:free'
        }
    if os.getenv("MOONSHOT_API_KEY"):
        return {
            'api_key': os.getenv("MOONSHOT_API_KEY"),
            'base_url': 'https://api.moonshot.cn/v1',
            'model': 'kimi-k2-0711-preview'
        }
    if os.getenv("GROQ_API_KEY"):
        return {
            'api_key': os.getenv("GROQ_API_KEY"),
            'base_url': 'https://api.groq.com/openai/v1',
            'model': 'llama-3.1-70b-versatile'
        }
    
    return None


def get_client():
    """Get OpenAI-compatible client for configured API."""
    config = get_api_config()
    if not config:
        raise ValueError("No API key found. Set OPENROUTER_API_KEY, MOONSHOT_API_KEY, or GROQ_API_KEY in secrets or .env file.")
    
    return OpenAI(
        api_key=config['api_key'],
        base_url=config['base_url']
    ), config['model']


def generate_content_ai(prompt: str, system_prompt: str) -> str:
    """Generate content using configured AI API."""
    client, model = get_client()
    
    response = client.chat.completions.create(
        model=model,
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
    
    return generate_content_ai(
        f"Create a comprehensive outline for an assignment about: {topic}",
        system_prompt
    )


def generate_code_snippet(topic: str) -> str:
    """Generate code snippets for the given programming topic."""
    system_prompt = """You are a coding tutor for Indonesian university students.
    Generate clean, well-commented code snippets with explanations.
    Include examples and best practices. Use appropriate programming language based on context."""
    
    return generate_content_ai(
        f"Generate code snippets and examples for: {topic}",
        system_prompt
    )


def generate_essay_structure(topic: str) -> str:
    """Generate an essay structure for the given topic."""
    system_prompt = """You are an academic writing assistant for Indonesian university students.
    Create detailed essay structures with thesis statement, body paragraphs, and conclusion.
    Include suggested arguments, evidence to look for, and transition phrases.
    Respond in the same language as the user's input."""
    
    return generate_content_ai(
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
