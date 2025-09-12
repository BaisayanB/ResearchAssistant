# app.py
import streamlit as st
import arxiv, re

# --- WIRING: Import the functions from your other files ---
from extractor import process_pdf_from_url
from llm import initialize_chat_session, get_gemini_response

# --- All of your original helper functions are preserved ---
def clean_query(query: str, allow_dots: bool = False) -> str:
    # (Your original code)
    query = query.replace("·", "-").replace("“", "\"").replace("”", "\"").replace("‘", "'").replace("’", "'")
    if allow_dots:
        query = re.sub(r"[^\w\s\-:\.']", "", query)
    else:
        query = re.sub(r"[^\w\s\-:']", "", query)
    return query.strip()

def generate_citation(result):
    # (Your original code)
    authors = ", ".join(a.name for a in result.authors)
    year = result.published.year
    title = result.title.strip(".")
    arxiv_id = result.get_short_id()
    apa = f"{authors} ({year}). {title}. arXiv:{arxiv_id}"
    bibtex_key = f"{result.authors[0].name.split()[-1]}{year}"
    bibtex = f"""@article{{{bibtex_key}, title={{ {title} }}, author={{ {authors} }}, year={{ {year} }}, eprint={{ {arxiv_id} }}, archivePrefix={{arXiv}}, primaryClass={{ {result.primary_category} }} }}"""
    return apa, bibtex

# --- State Management for switching between Search and Chat views ---
if "view" not in st.session_state:
    st.session_state.view = "search"
if "active_paper" not in st.session_state:
    st.session_state.active_paper = None
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# ========================= VIEW 1: SEARCH PAGE =======================
def render_search_view():
    st.title("🤖 AI Research Paper Assistant")

    # --- Your entire original sidebar and search logic is here ---
    with st.sidebar:
        st.header("Search")
        mode = st.selectbox("Search Mode", ["Normal Search", "Title Only Search", "Search by arXiv ID"])
        placeholder = {"Normal Search": "e.g., vision transformers", "Title Only Search": "e.g., attention is all you need", "Search by arXiv ID": "e.g., 2102.12092"}[mode]
        query = st.text_input("🔍 Enter Search Query", placeholder=placeholder, key="search_query")
        max_results = st.slider("🔢 Number of Results", 10, 300, 50, 10)

    if not query:
        # --- Your original search tips are preserved ---
        st.subheader("🧠 How to Search Effectively")
        # (Your original guidance text for each mode)
        if mode == "Normal Search": st.markdown("- 🔑 Use **topic keywords**...\n- 👥 Add **author names**...\n- 🧩 Combine topics...\n- ❌ Avoid quotes...")
        elif mode == "Title Only Search": st.markdown("- 🎯 Use **distinct words**...\n- ❌ Avoid full sentences...\n- ✅ Match concepts...")
        elif mode == "Search by arXiv ID": st.markdown("- 🆔 Enter a valid arXiv ID...\n- 📎 Find it in the URL...\n- Only one ID at a time.")
        return

    st.write(f"### Results for: `{query}`")
    with st.spinner("🔎 Searching arXiv..."):
        try:
            # --- Your original search execution logic ---
            client = arxiv.Client()
            if mode == "Search by arXiv ID":
                search = arxiv.Search(id_list=[clean_query(query, allow_dots=True)])
            else:
                search_query = f"ti:{clean_query(query)}" if mode == "Title Only Search" else clean_query(query)
                search = arxiv.Search(query=search_query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
            results = list(client.results(search))

            if not results:
                # --- Your original 'no results' guidance is preserved ---
                st.warning("⚠️ No results found.")
                with st.expander("💡 Search Tips"):
                    # (Your original tips)
                    if mode == "Search by arXiv ID": st.markdown("- Check ID format: should look like `2306.12345`.")
                    else: st.markdown("- 🧠 Use meaningful keywords...\n- 👥 Include author names...\n- 🔢 Increase number of results...\n- 🔄 Try switching...")
            else:
                # --- Your original results display loop ---
                for result in results:
                    with st.expander(result.title):
                        st.markdown(f"**🧑‍🔬 Authors:** {', '.join(a.name for a in result.authors)}")
                        st.markdown(f"**📅 Published:** {result.published.strftime('%Y-%m-%d')}")
                        st.markdown(f"**📝 Summary:** {result.summary.strip()}")
                        st.markdown(f"[🔗 View on arXiv]({result.entry_id})")
                        
                        # --- MODIFICATION: Added the Chat button ---
                        if st.button("💬 Chat with this Paper", key=result.get_short_id()):
                            st.session_state.active_paper = result
                            st.session_state.view = "chat"
                            st.rerun() # This command switches to the chat view

                        # --- Your original citation expander is preserved ---
                        apa, bibtex = generate_citation(result)
                        with st.expander("📌 Export Citation"):
                            st.markdown("**📖 APA Style:**"); st.code(apa, language="markdown")
                            st.markdown("**🔧 BibTeX Format:**"); st.code(bibtex, language="latex")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ===================================================================
# ========================= VIEW 2: CHAT PAGE =======================
# ===================================================================
def render_chat_view():
    paper = st.session_state.active_paper
    st.title(f"💬 Chatting with Paper")
    st.info(f"**Title:** *{paper.title}*")

    if st.button("⬅️ Back to Search Results"):
        st.session_state.view = "search"
        st.session_state.active_paper = None
        st.session_state.chat_session = None
        st.session_state.messages = []
        st.rerun()

    # One-time setup: Process the paper and initialize the chat
    if st.session_state.chat_session is None:
        with st.spinner("Reading paper and preparing AI... This may take a moment."):
            try:
                # --- CONNECTION TO extractor.py ---
                pdf_url = f"https://arxiv.org/pdf/{paper.get_short_id()}.pdf"

                paper_data = process_pdf_from_url(pdf_url, paper.get_short_id())
                
                # --- CONNECTION TO llm.py ---
                st.session_state.chat_session = initialize_chat_session(paper_data)
                st.session_state.messages = [{"role": "assistant", "content": "I've finished reading the paper. Ask me anything about its content!"}]
            except Exception as e:
                st.error(f"Failed to prepare the chat session: {e}")
                st.stop()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Ask a question about the paper..."):
        # 1. Add user message to history.
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 2. Get AI response.
        with st.spinner("AI is thinking..."):
            response = get_gemini_response(st.session_state.chat_session, prompt)
        
        # 3. Add AI response to history.
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # 4. Rerun the app to make the loop above display the new messages.
        st.rerun()

# Main app router 
st.set_page_config(page_title="AI Research Paper Assistant", layout="wide")

# This router decides which view to show based on the session state
if st.session_state.view == "search":
    render_search_view()
else:
    render_chat_view()