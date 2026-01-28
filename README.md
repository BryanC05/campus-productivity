# 🎓 Campus Productivity MVPs

> AI-powered study tools for Indonesian university students

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Kimi K2](https://img.shields.io/badge/AI-Kimi%20K2-blueviolet)](https://www.moonshot.cn/)
[![Saweria](https://img.shields.io/badge/Donate-Saweria-orange)](https://saweria.co/bryanchan)

---

## 🛠️ Projects

### 1. AI Assignment Brainstormer

A Streamlit web app that helps students generate:
- 📋 **Assignment Outlines** - Structured plans for papers/projects
- 💻 **Code Snippets** - Working code with explanations
- 📝 **Essay Structures** - Thesis, body, conclusion frameworks
- 📁 **File Upload** - PDF, PowerPoint, and Image analysis with OCR
- 🌙 **Dark/Light Theme** - Toggle between modes
- 📜 **History Feature** - View past generations

**Tech Stack**: Streamlit + Kimi K2 (Moonshot AI) + SQLite + Tesseract OCR

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

> 🔑 Get your API key: [platform.moonshot.ai](https://platform.moonshot.ai)

---

### 2. Code Debug Tutor

A Google Colab notebook that analyzes error messages and explains fixes.

**Tech Stack**: Google Colab + Ollama + Kimi-Dev-72B

#### Quick Start

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/BryanC05/campus-productivity/blob/main/code-debug-tutor/Code_Debug_Tutor.ipynb)

1. Click the Colab badge above
2. Enable GPU runtime (Runtime → Change runtime type)
3. Run all cells
4. Paste your error message!

---

## 📁 Project Structure

```
campus-productivity/
├── ai-assignment-brainstormer/
│   ├── app.py              # Streamlit UI with themes
│   ├── database.py         # SQLite operations
│   ├── kimi_api.py         # Kimi K2 API integration
│   ├── file_processor.py   # PDF/PPT/Image processing
│   ├── requirements.txt    # Dependencies
│   ├── .streamlit/         # Streamlit config
│   └── .env.example        # API key template
├── code-debug-tutor/
│   ├── Code_Debug_Tutor.ipynb  # Colab notebook
│   └── README.md               # Usage guide
└── README.md               # This file
```

## 🚀 Features

| Feature | AI Brainstormer | Code Debug Tutor |
|---------|-----------------|------------------|
| Text Input | ✅ | ✅ |
| File Upload (PDF/PPT/Images) | ✅ | ❌ |
| OCR (Handwriting/Screenshots) | ✅ | ❌ |
| Dark/Light Theme | ✅ | ❌ |
| History/Save Results | ✅ | ❌ |
| Free Hosting | Streamlit Cloud | Google Colab |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ☕ Support

If these tools help your studies, consider supporting development:

[![Saweria](https://img.shields.io/badge/Donate%20via-Saweria-orange?style=for-the-badge)](https://saweria.co/bryanchan)

## 📄 License

MIT License - Feel free to use and modify!

---

*Built with ❤️ for Indonesian students | © 2026 Bryan Chan*
