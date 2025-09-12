# llm.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- This setup part is your original code ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# I've updated the model name to a stable, recommended version
MODEL_NAME = "gemini-1.5-flash" 

def get_gemini_response(chat_session, prompt: str) -> str:
    # --- This is your original, unmodified function ---
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with Gemini API: {e}"


# --- ADDITION: A function to set up and initialize the chat session ---
def initialize_chat_session(paper_data: dict):
    """
    Takes extracted paper data, creates the initial context prompt,
    and returns an initialized Gemini chat session.
    """
    if not GEMINI_API_KEY:
        raise ValueError("Error: GEMINI_API_KEY not found. Please set it in your .env file or Streamlit secrets.")

    paper_content = paper_data.get("content", "No content extracted.")
    metadata = paper_data.get("metadata", {})
    paper_title = metadata.get("title", "Untitled Paper")
    paper_authors = ", ".join(metadata.get("authors", ["Unknown Authors"]))

    initial_context = (
        f"You are a 'Principal AI Researcher' and an expert communicator. Your task is to explain a research paper to a skilled technical colleague. "
        f"You will be given the content of a paper titled '{paper_title}' by {paper_authors}. "
        f"Your goal is to provide answers that are not just technically correct, but also build deep intuition.\n\n"
        f"--- PAPER CONTENT START ---\n{paper_content}\n--- PAPER CONTENT END ---\n\n"
        f"### Your Core Instructions:\n"
        f"1.  **Analogy First, Then Details:** For any complex concept, **always start with a simple, intuitive analogy or a high-level summary.** After building the intuition, then provide the detailed, technical explanation based on the paper's content.\n"
        f"2.  **Grounding and Nuance:** Your primary source of truth is the paper. For factual questions (e.g., 'What was the result in Table 2?'), stick strictly to the text. For conceptual questions (e.g., 'Why is this important?'), use the paper as your foundation but enrich your explanation with analogies and foundational knowledge to provide context and clarity.\n"
        f"3.  **Structured and Clear:** Use Markdown to structure your answers logically. Use headings, bold keywords, and lists to make the information easy to digest.\n"
        f"4.  **No HTML:** Do not use any HTML tags in your response."
        f"5.  **Use LaTeX for Math:** When presenting mathematical formulas or variables, you **must** use LaTeX formatting. Enclose inline math with single dollar signs (e.g., $d_k$) and block equations with double dollar signs (e.g., $$y = mx + b$$)."
    )
    
    model = genai.GenerativeModel(MODEL_NAME)
    chat_session = model.start_chat(history=[])
    
    # Send the initial context to the model to set up the conversation
    chat_session.send_message(initial_context)
    
    return chat_session