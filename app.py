import os
import time
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv

load_dotenv()

VECTORSTORE_DIR = "vectorstore"
EMBED_MODEL     = "all-MiniLM-L6-v2"
GROQ_MODEL      = "llama-3.1-8b-instant"

PROMPT_TEMPLATE = """You are a helpful and warm assistant for NayePankh Foundation, a registered Indian NGO that uplifts underprivileged people through food, clothes, sanitary pads, and education.

Use the following context to answer the question accurately and warmly. If the answer is not in the context, say "I don't have that information - please contact NayePankh at contact@nayepankh.com or call +91-8318500748."

Context:
{context}

Input: {input}

Answer:"""

@st.cache_resource(show_spinner=False)
def load_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"}
    )
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )
    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "input"]
    )
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, combine_docs_chain)
    return chain

st.set_page_config(page_title="NayePankh Chatbot", page_icon="🕊️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Poppins:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.stApp { background: linear-gradient(135deg, #FFF9F0 0%, #F0F8FF 50%, #F5FFF0 100%); }

.hero {
    background: linear-gradient(135deg, #FF6B6B, #FF8E53, #FFC107);
    border-radius: 24px;
    padding: 32px 28px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(255,107,107,0.25);
}
.hero h1 { font-family:'Nunito',sans-serif; font-size:1.9rem; font-weight:800; color:white; margin:0 0 6px 0; }
.hero p { color:rgba(255,255,255,0.92); font-size:0.95rem; margin:0; }

.stats-bar { display:flex; justify-content:center; gap:10px; margin-bottom:20px; flex-wrap:wrap; }
.stat-chip { background:white; border-radius:50px; padding:7px 16px; font-size:0.82rem; font-weight:600; box-shadow:0 2px 12px rgba(0,0,0,0.08); display:inline-flex; align-items:center; gap:5px; }
.chip-orange { border:2px solid #FF8E53; color:#D4500A; }
.chip-blue   { border:2px solid #4ECDC4; color:#0A7A73; }
.chip-green  { border:2px solid #6BCB77; color:#1A7A27; }
.chip-purple { border:2px solid #A78BFA; color:#5B21B6; }

.section-label { font-size:0.78rem; font-weight:700; color:#888; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:10px; }

.source-card { background:linear-gradient(135deg,#FFF9F0,#FFF3E0); border:1.5px solid #FFD4A3; border-radius:10px; padding:10px 14px; margin-top:6px; font-size:0.78rem; color:#8B4513; line-height:1.5; }
.source-label { font-weight:700; color:#D4500A; display:block; margin-bottom:4px; font-size:0.75rem; }

.footer { text-align:center; color:#aaa; font-size:0.75rem; margin-top:8px; padding:12px; }
.footer a { color:#FF8E53; text-decoration:none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🕊️ NayePankh Foundation</h1>
    <p>Your friendly guide to donations, volunteering, internships and more!</p>
</div>
<div class="stats-bar">
    <span class="stat-chip chip-orange">🍱 Food Distribution</span>
    <span class="stat-chip chip-blue">🎓 Education</span>
    <span class="stat-chip chip-green">👕 Clothes</span>
    <span class="stat-chip chip-purple">💜 2 Lakh+ Helped</span>
</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

SUGGESTIONS = [
    ("🤝", "What does NayePankh do?"),
    ("💸", "How can I donate?"),
    ("🧾", "Is my donation tax-exempt?"),
    ("💼", "How do I get an internship?"),
    ("👤", "Who founded NayePankh?"),
    ("❤️", "How many people have been helped?"),
]

if not st.session_state.chat_history:
    st.markdown('<div class="section-label">✨ Quick questions</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (emoji, q) in enumerate(SUGGESTIONS):
        if cols[i % 3].button(f"{emoji} {q}", key=f"s_{i}", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": q})
            st.session_state.quick_question = q
    st.markdown("<br>", unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🕊️"):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📚 View sources", expanded=False):
                for i, src in enumerate(msg["sources"][:2], 1):
                    st.markdown(f'<div class="source-card"><span class="source-label">📌 Source {i}</span>{src[:200]}...</div>', unsafe_allow_html=True)

if st.session_state.chat_history:
    col1, col2, col3 = st.columns([4, 1, 1])
    with col3:
        if st.button("🗑️ Clear", key="clear"):
            st.session_state.chat_history = []
            st.rerun()

user_input = st.chat_input("Ask anything about NayePankh Foundation...")
question = user_input or st.session_state.pop("quick_question", None)

if question:
    if not st.session_state.chat_history or st.session_state.chat_history[-1]["content"] != question:
        st.session_state.chat_history.append({"role": "user", "content": question})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🕊️"):
        placeholder = st.empty()
        placeholder.markdown("🔍 *Searching knowledge base...*")
        try:
            chain = load_chain()
            result = chain.invoke({"input": question})
            answer = result["answer"]
            sources = [doc.page_content for doc in result.get("context", [])]

            placeholder.empty()
            typed = ""
            type_ph = st.empty()
            words = answer.split(" ")
            for i, word in enumerate(words):
                typed += word + " "
                if i % 5 == 0:
                    type_ph.markdown(typed + "▌")
                    time.sleep(0.03)
            type_ph.markdown(answer)

            if sources:
                with st.expander("📚 View sources", expanded=False):
                    for i, src in enumerate(sources[:2], 1):
                        st.markdown(f'<div class="source-card"><span class="source-label">📌 Source {i}</span>{src[:200]}...</div>', unsafe_allow_html=True)

            st.session_state.chat_history.append({"role": "assistant", "content": answer, "sources": sources})

        except Exception as e:
            placeholder.empty()
            st.error(f"Error: {str(e)}")
            st.session_state.chat_history.append({"role": "assistant", "content": "Sorry, something went wrong. Please try again!"})

st.markdown('<div class="footer">Built with LangChain · Groq LLaMA 3 · ChromaDB · <a href="https://nayepankh.com" target="_blank">nayepankh.com</a></div>', unsafe_allow_html=True)
