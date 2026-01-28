# 🎓 Campus Productivity MVPs

AI-powered study tools for Indonesian university students.

## 🛠️ Projects

### 1. AI Assignment Brainstormer

A Streamlit web app that helps students generate:
- 📋 **Assignment Outlines** - Structured plans for papers/projects
- 💻 **Code Snippets** - Working code with explanations
- 📝 **Essay Structures** - Thesis, body, conclusion frameworks

**Powered by**: Kimi K2 (Moonshot AI)  
**Storage**: SQLite (free, local database)  
**Support**: Donations via [Saweria](https://saweria.co/campusproductivity)

#### Quick Start

```bash
cd ai-assignment-brainstormer
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your Moonshot API key

# Run the app
streamlit run app.py
```

Get your API key: [platform.moonshot.ai](https://platform.moonshot.ai)

---

### 2. Code Debug Tutor

A Google Colab notebook that analyzes error messages and explains fixes.

**Powered by**: Ollama + Kimi-Dev-72B  
**Platform**: Google Colab (free with GPU)

#### Quick Start

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/campus-productivity-mvps/blob/main/code-debug-tutor/Code_Debug_Tutor.ipynb)

1. Click the Colab badge
2. Enable GPU runtime
3. Run all cells
4. Paste your error!

---

## 📁 Project Structure

```
Campus Productivity/
├── ai-assignment-brainstormer/
│   ├── app.py              # Streamlit UI
│   ├── database.py         # SQLite operations
│   ├── kimi_api.py         # Kimi K2 integration
│   ├── requirements.txt    # Dependencies
│   └── .env.example        # API key template
├── code-debug-tutor/
│   ├── Code_Debug_Tutor.ipynb  # Colab notebook
│   └── README.md               # Usage guide
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## ☕ Support

If these tools help your studies, consider supporting:

[![Saweria](https://img.shields.io/badge/Donate-Saweria-orange)](https://saweria.co/campusproductivity)

---

*Built with ❤️ for Indonesian students | © 2026 Campus Productivity MVPs*
