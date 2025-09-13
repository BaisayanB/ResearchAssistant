# 📚 ResearchPaper Assistant

_“Your AI study buddy for understanding complex research papers.”_

---

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)  
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)  
![License](https://img.shields.io/badge/License-Personal-lightgrey.svg)  
![arXiv](https://img.shields.io/badge/arXiv-API-orange.svg)  
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4.svg)

---

## 📖 Introduction

ResearchPaper Assistant is a **Streamlit-based web application** that helps students and learners interact with research papers from **arXiv**.  
With just a search query or paper ID, you can:

- 🔎 **Search** for relevant research papers on arXiv
- 📄 **View metadata, abstracts, and citations** instantly
- 🤖 **Chat with the paper** using Google’s Gemini LLM to break down complex concepts
- 🎓 Learn through **analogy-first explanations** that build intuition before diving into technical details

This project was built as part of my learning journey — exploring **PDF text extraction**, **arXiv APIs**, and the power of **Large Language Models (LLMs)**. While originally a learning project, it is designed to feel like a **real-world tool for students** who want to make sense of research papers quickly.

---

## ✨ Features

- **Smart Search** – Find papers by topic, title, or arXiv ID
- **One-click Paper Chat** – Turn any paper into an interactive AI conversation
- **Citation Export** – Get APA and BibTeX formats instantly
- **PDF Text Extraction** – Clean extraction from PDFs using PyMuPDF (`fitz`)
- **Context-aware LLM Responses** – Answers are grounded in the paper, structured, and math-friendly with LaTeX support

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/researchpaper-assistant.git
cd researchpaper-assistant

2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

3. Install dependencies
pip install -r requirements.txt

4. Set up your API key

Create a .env file in the root directory and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

⚡ Usage

Run the app with Streamlit:

streamlit run app.py


Then open your browser at http://localhost:8501.

⚙️ Project Structure
📂 researchpaper-assistant
 ├── app.py          # Main Streamlit app (search & chat views)
 ├── extractor.py    # Handles PDF download, extraction, metadata
 ├── llm.py          # Sets up Gemini LLM and manages chat sessions
 ├── requirements.txt
 └── README.md

🗂️ How It Works
flowchart TD
    A[User enters query / arXiv ID] --> B[Search arXiv API<br/>(fetch metadata)]
    B --> C[Download PDF<br/>from arXiv]
    C --> D[Extract text with PyMuPDF<br/>(clean & preprocess)]
    D --> E[Prepare context with metadata]
    E --> F[Initialize Gemini LLM Chat]
    F --> G[User asks questions]
    G --> H[Gemini generates structured<br/>analogy-first answers]
    H --> G[[Loop: Ask more questions]]

🔑 Key Technologies

Streamlit
 – Web interface

arxiv
 – Paper search API

PyMuPDF (fitz)
 – PDF text extraction

Requests
 – Downloading PDFs

Google Generative AI
 – Gemini LLM integration

python-dotenv
 – Environment variable management

🧭 Planned Enhancements

 (Your future ideas here…)

📜 License

This project is released as a personal showcase project. Feel free to explore, learn, and adapt it.

🙌 Acknowledgements

arXiv for open-access research

PyMuPDF for PDF parsing

Google Gemini for LLM-powered Q&A

Streamlit for making ML apps so easy to build
```
