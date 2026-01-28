# Local Ollama with Cloud Models (FREE tier)
import requests


# Ollama local server (routes to cloud for cloud models)
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL = "kimi-k2:1t-cloud"  # Uses Ollama Cloud free tier


def generate_content_ollama(prompt: str, system_prompt: str) -> str:
    """Generate content using Ollama (local+cloud)."""
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        },
        timeout=120
    )
    
    if response.status_code == 200:
        return response.json()["message"]["content"]
    else:
        raise ValueError(f"Ollama error: {response.text}")


def generate_outline(topic: str) -> str:
    """Generate an assignment outline for the given topic."""
    system_prompt = """You are an academic assistant helping Indonesian university students. 
    Create detailed assignment outlines with clear sections, bullet points, and suggestions.
    Respond in the same language as the user's input (Indonesian or English)."""
    
    return generate_content_ollama(
        f"Create a comprehensive outline for an assignment about: {topic}",
        system_prompt
    )


def generate_code_snippet(topic: str) -> str:
    """Generate code snippets for the given programming topic."""
    system_prompt = """You are a coding tutor for Indonesian university students.
    Generate clean, well-commented code snippets with explanations.
    Include examples and best practices. Use appropriate programming language based on context."""
    
    return generate_content_ollama(
        f"Generate code snippets and examples for: {topic}",
        system_prompt
    )


def generate_essay_structure(topic: str) -> str:
    """Generate an essay structure for the given topic."""
    system_prompt = """You are an academic writing assistant for Indonesian university students.
    Create detailed essay structures with thesis statement, body paragraphs, and conclusion.
    Include suggested arguments, evidence to look for, and transition phrases.
    Respond in the same language as the user's input."""
    
    return generate_content_ollama(
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
