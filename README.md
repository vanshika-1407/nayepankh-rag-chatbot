🕊️ NayePankh Foundation RAG Chatbot
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red?style=flat-square&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.1.20-green?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-purple?style=flat-square)
> An AI-powered RAG chatbot for **NayePankh Foundation** — a UP Government registered NGO that has uplifted 2 lakh+ underprivileged people across India. Users can ask anything about donations, volunteering, internships, and the NGO's work — and get accurate, grounded answers instantly.
---
📌 About the Project
NayePankh Foundation is one of India's biggest student-led NGOs, working in food distribution, education, sanitary pads, and clothes for underprivileged communities. However, people visiting their website often have questions that go unanswered — How do I donate? Is it tax-exempt? Can I get an internship?
This chatbot solves that by using Retrieval-Augmented Generation (RAG) — it retrieves the most relevant information from NayePankh's official knowledge base and uses LLaMA 3 to generate accurate, context-aware answers in real time.
Built as a portfolio project to demonstrate practical RAG implementation with real-world social impact.
---
🧠 How RAG Works (Architecture)
```
User types a question
        ↓
HuggingFace Embeddings converts it to a vector
        ↓
ChromaDB searches for the 4 most similar chunks
from the NayePankh knowledge base
        ↓
Retrieved chunks + original question → Prompt Template
        ↓
Groq API sends it to LLaMA 3 (cloud inference)
        ↓
LLaMA 3 generates a grounded answer
        ↓
Streamlit displays it with typing animation + sources
```
This ensures the chatbot only answers from verified NayePankh content — no hallucinations, no made-up information.
---
🛠️ Tech Stack
Technology	Purpose
Python 3.11	Core language
LangChain	RAG pipeline orchestration
ChromaDB	Local vector database for storing embeddings
HuggingFace `all-MiniLM-L6-v2`	Text embedding model (runs locally, free)
Groq API (LLaMA 3)	Cloud LLM inference — fast and free
Streamlit	Web UI framework
python-dotenv	Secure API key management
---
✨ Features
🤖 RAG-powered answers — grounded in NayePankh's actual content, not generic AI responses
⌨️ Typing animation — answers appear word by word for a natural feel
📚 Source transparency — every answer shows which knowledge base chunks were used
💡 Suggested questions — 6 clickable quick-start questions for new users
🎨 Colorful, friendly UI — warm gradient design with stat chips
🗑️ Clear chat — reset conversation with one click
⚡ Fast responses — Groq's LLaMA 3 inference in under 2 seconds
🌐 Fully deployed — accessible via live Streamlit Cloud link
---
📸 Screenshots
> Add a screenshot here after deployment!
> Replace the line below with your actual screenshot.
![NayePankh Chatbot Screenshot](assets/screenshot.png)
---
🚀 Getting Started (Local Setup)
Prerequisites
Python 3.11
A free Groq API key from console.groq.com
Steps
1. Clone the repository
```bash
git clone https://github.com/vanshika-1407/nayepankh-rag-chatbot.git
cd nayepankh-rag-chatbot
```
2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up your API key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free key at console.groq.com
5. Build the vector store
```bash
python ingest.py
```
This chunks the knowledge base, creates embeddings, and stores them in ChromaDB. Run this once before starting the app.
6. Run the app
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` 🎉
---
🌐 Live Demo
👉 Try the live chatbot here ← (update after deployment)
---
📁 Project Structure
```
nayepankh-rag-chatbot/
│
├── app.py                    # Main Streamlit chatbot UI
├── ingest.py                 # Knowledge base ingestion pipeline
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not pushed to GitHub)
├── .gitignore                # Files to exclude from Git
│
├── data/
│   └── knowledge_base.txt    # NayePankh Foundation content
│
├── vectorstore/              # ChromaDB vector store (auto-generated)
│
└── assets/
    └── screenshot.png        # App screenshot for README
```
---
🔮 Future Improvements
[ ] Add Hindi/Hinglish language support
[ ] Add feedback buttons (👍👎) for answer quality
[ ] Expand knowledge base with more NayePankh content
[ ] Add web scraping to auto-update knowledge base
[ ] Integrate WhatsApp API for wider reach
---
🙋 About Me
Built by Vanshika Verma — MCA student at Panjab University, Chandigarh.  
Passionate about AI/ML, LLM integration, and building projects with real-world impact.
![LinkedIn](https://www.linkedin.com/in/vanshika-verma-819a83250/)
![GitHub](https://github.com/vanshika-1407)
---
🤝 Acknowledgements
NayePankh Foundation — for their incredible social work
Groq — for free, blazing-fast LLaMA 3 inference
LangChain — for the RAG framework
Streamlit — for the effortless UI
---
<p align="center">Built with ❤️ for social impact · <a href="https://nayepankh.com">nayepankh.com</a></p>