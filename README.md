# Agentic AI Campaign Analytics & Insight Assistant

## 🎯 Project Overview

A production-ready, interview-friendly GenAI application that automates campaign analytics and operational analysis in AdTech environments. This project demonstrates practical implementation of modern AI/ML concepts including LangChain, RAG (Retrieval Augmented Generation), LCEL (LangChain Expression Language), vector embeddings, and agentic AI workflows.

**Built for:** Technical interviews, portfolio demonstration, and production deployment.

---

## ✨ Features

### 1. **Campaign Analytics Dashboard**
- Upload advertising campaign CSV data
- Automatic KPI calculations (CTR, CPM, Revenue metrics)
- Interactive Plotly visualizations
- Real-time campaign performance tracking

### 2. **AI-Powered Insights**
- Automatic anomaly detection with ML logic
- Gemini LLM-powered analysis generation
- Smart alerts for underperforming campaigns
- Performance trend analysis

### 3. **RAG Knowledge Base Q&A**
- PDF document upload and processing
- Real vector embeddings with HuggingFace
- FAISS vector store for similarity search
- LangChain LCEL-based retrieval chains
- Natural language Q&A on knowledge documents

### 4. **Agentic Workflow**
Four specialized agents orchestrating the analysis:
- **Analytics Agent**: KPI calculation & anomaly detection
- **Retrieval Agent**: Document management & RAG pipeline
- **Recommendation Agent**: AI-driven optimization suggestions
- **Reporting Agent**: Executive summaries & comprehensive reports

### 5. **Smart Recommendations**
- Budget reallocation suggestions
- Audience targeting optimization
- Performance improvement recommendations
- ROI-focused insights

### 6. **Professional Reporting**
- Executive summaries with AI generation
- Campaign performance reports
- Anomaly analysis reports
- PDF export-ready data structures

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                         │
├─────────────────────────────────────────────────────────────┤
│  Dashboard │ Insights │ Recommendations │ RAG Q&A │ Reports │
├─────────────────────────────────────────────────────────────┤
│                     Agent Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Analytics   │  │  Retrieval   │  │   Rec.       │      │
│  │   Agent      │→ │   Agent      │→ │  Agent       │→     │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                              ↓               │
│                                        ┌──────────────┐      │
│                                        │  Reporting   │      │
│                                        │   Agent      │      │
│                                        └──────────────┘      │
├─────────────────────────────────────────────────────────────┤
│                    Utility Layer                            │
│  ├─ analytics.py       │  ├─ prompts.py                    │
│  ├─ charts.py          │  ├─ gemini_helper.py              │
│  ├─ rag_pipeline.py    │  └─ ...                           │
├─────────────────────────────────────────────────────────────┤
│                    LLM & Vector Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Gemini     │  │ HuggingFace  │  │   FAISS      │      │
│  │   API        │  │ Embeddings   │  │ Vector DB    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Web UI & Dashboard |
| **LLM** | Google Gemini API | AI Insights Generation |
| **LangChain** | LCEL, Chains | Orchestration & Workflows |
| **RAG** | FAISS + Embeddings | Vector Search & Retrieval |
| **Embeddings** | HuggingFace | Text to Vector Conversion |
| **Data** | Pandas | CSV Processing |
| **Viz** | Plotly | Interactive Charts |
| **PDF** | PyPDF2 | Document Extraction |
| **Env** | python-dotenv | Configuration |

---

## 🎓 Learning Outcomes

This project demonstrates:

### **GenAI Concepts**
- ✅ Large Language Models (LLMs)
- ✅ Retrieval Augmented Generation (RAG)
- ✅ Vector Embeddings
- ✅ Semantic Search with FAISS
- ✅ Prompt Engineering
- ✅ AI Automation

### **LangChain Implementation**
- ✅ LCEL (LangChain Expression Language) chains
- ✅ RecursiveCharacterTextSplitter for document chunking
- ✅ HuggingFaceEmbeddings for text vectorization
- ✅ FAISS Retriever for similarity search
- ✅ PromptTemplate for structured prompting
- ✅ RunnablePassthrough for chain composition

### **Agentic AI**
- ✅ Multi-agent architecture
- ✅ Agent orchestration workflow
- ✅ Task-specific specialization
- ✅ Sequential agent composition

### **Software Engineering**
- ✅ Modular architecture
- ✅ Clean code patterns
- ✅ Error handling
- ✅ Production-ready implementation

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Google API key (from [aistudio.google.com](https://aistudio.google.com/app/apikeys))

### Step 1: Clone/Download Project
```bash
cd ai-campaign-assistant
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Edit .env file and add your API key
GOOGLE_API_KEY=your_actual_api_key_here
```

Get your free API key: https://aistudio.google.com/app/apikeys

### Step 5: Run Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. **Upload Campaign Data**
- Click "📁 Upload Campaign Data" in sidebar
- Upload CSV with columns: Campaign, Impressions, Clicks, Revenue
- Use `data/sample_campaigns.csv` for testing

### 2. **View Dashboard**
- Automatic KPI calculation (CTR, CPM, Revenue)
- Interactive charts update in real-time
- See anomalies and alerts

### 3. **Analyze Insights**
- "🔍 Insights & Anomalies" tab shows AI analysis
- Automatically detects underperformance
- Displays severity-based alerts

### 4. **Get Recommendations**
- "💡 Recommendations" tab generates AI suggestions
- Budget reallocation strategies
- Targeting optimization advice

### 5. **Upload Knowledge Documents**
- Upload PDF files (SOPs, guides, manuals)
- Click "Process PDFs for RAG" button
- System builds FAISS vector store

### 6. **Ask Questions (RAG)**
- "❓ RAG Q&A" tab
- Ask questions about your documents
- System retrieves relevant chunks and generates answers

### 7. **Generate Reports**
- "📋 Reports" tab
- Choose report type (Executive, Performance, Insights)
- View professional formatted report

---

## 📊 Sample Data

`data/sample_campaigns.csv` contains 12 sample campaigns with realistic metrics:
- Search, Display, Social, Video, Email, Affiliate, Mobile campaigns
- Realistic CTR, CPM, and revenue patterns
- Perfect for testing and demonstration

---

## 🧠 Code Walkthrough

### Key LangChain LCEL Implementation
```python
# From utils/rag_pipeline.py
from langchain_core.runnables import RunnablePassthrough

# LCEL Chain Composition - demonstrates RAG
rag_chain = (
    {
        "context": retriever,           # Retrieve relevant chunks
        "question": RunnablePassthrough() # Pass question through
    }
    | prompt          # Format with prompt template
    | llm            # Call Gemini API
)

# Execute the chain
response = rag_chain.invoke(user_question)
```

### Embedding & FAISS Integration
```python
# From utils/rag_pipeline.py
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create vector store
vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

### Agentic Workflow
```python
# Workflow execution (from app.py)
1. User uploads CSV
2. Analytics Agent → calculates KPIs, detects anomalies
3. Retrieval Agent → manages knowledge documents
4. Recommendation Agent → generates optimization suggestions
5. Reporting Agent → creates professional reports
6. Streamlit UI → displays results to user
```

---

## 🎯 Interview Talking Points

### When explaining the project:

1. **Architecture & Modularity**
   - "The application uses four specialized agents, each handling specific responsibilities"
   - "Agents are orchestrated sequentially: Analytics → Retrieval → Recommendation → Reporting"
   - "This modular approach allows easy testing and maintenance"

2. **LangChain & LCEL**
   - "We use LangChain Expression Language for elegant chain composition"
   - "The LCEL pipe operator (`|`) composes components like a Unix pipeline"
   - "This makes complex workflows readable and maintainable"

3. **RAG Implementation**
   - "Real RAG with actual vector embeddings (HuggingFace)"
   - "FAISS provides O(1) similarity search on millions of vectors"
   - "Retriever fetches context, which is passed to LLM for answer generation"

4. **AI Automation**
   - "Anomalies are detected automatically using statistical thresholds"
   - "Gemini LLM generates insights using our structured prompts"
   - "Entire workflow requires minimal human intervention"

5. **Production Readiness**
   - "Error handling at every stage"
   - "Vectorstore persists to disk for consistency"
   - "API key stored in .env for security"
   - "Streamlit provides responsive, professional UI"

---

## 🔒 Security Best Practices

- ✅ API keys stored in `.env` (not in code)
- ✅ `.env` added to `.gitignore`
- ✅ Never commit API keys
- ✅ Error handling without exposing sensitive data
- ✅ Safe PDF file handling

---

## 🚀 Future Enhancements

### Phase 2: Advanced Features
- [ ] Multi-user support with session management
- [ ] Database integration (PostgreSQL for vectorstore)
- [ ] Scheduled report generation
- [ ] Campaign performance predictions

### Phase 3: Enterprise Features
- [ ] Advanced role-based access control
- [ ] Audit logging
- [ ] API endpoint exposure
- [ ] Real-time streaming analytics

### Phase 4: ML Integration
- [ ] Custom embedding models
- [ ] Fine-tuned recommendation engine
- [ ] Predictive anomaly detection
- [ ] Auto-optimization workflows

---

## 📝 File Structure

```
ai-campaign-assistant/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (template)
├── README.md                   # This file
│
├── data/
│   └── sample_campaigns.csv   # Sample campaign data
│
├── docs/
│   └── (PDF documents for RAG testing)
│
├── agents/
│   ├── analytics_agent.py      # KPI & anomaly detection
│   ├── retrieval_agent.py      # RAG & document management
│   ├── recommendation_agent.py # Optimization suggestions
│   └── reporting_agent.py      # Report generation
│
├── utils/
│   ├── analytics.py           # KPI calculations
│   ├── charts.py              # Plotly visualizations
│   ├── rag_pipeline.py        # LCEL RAG implementation
│   ├── prompts.py             # LLM prompt templates
│   └── gemini_helper.py       # Gemini API utilities
│
└── vectorstore/
    └── (FAISS index stored here)
```

---

## 🐛 Troubleshooting

### Error: "GOOGLE_API_KEY not found"
- Add `GOOGLE_API_KEY` to `.env` file
- Restart the Streamlit app

### Error: "Retriever not initialized"
- Upload and process PDF files first
- Wait for "Process PDFs" to complete
- Check that FAISS index was created

### Error: "RecursionError" or slow response
- Check document size (very large PDFs may take time)
- Reduce chunk size in `rag_pipeline.py` if needed
- Monitor memory usage for vectorstore

### Charts not displaying
- Ensure Plotly is installed: `pip install plotly`
- Check CSV has numeric columns

---

## 📚 References

- [LangChain Documentation](https://python.langchain.com/)
- [LangChain Expression Language (LCEL)](https://python.langchain.com/docs/expression_language/)
- [FAISS Vector Search](https://github.com/facebookresearch/faiss)
- [Google Gemini API](https://ai.google.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [HuggingFace Embeddings](https://huggingface.co/spaces/mteb/leaderboard)

---

## 🤝 Contributing

This is a portfolio project. Feel free to fork and extend!

### Ideas for Extensions:
- Add more visualization types
- Implement export to PDF/Excel
- Add user authentication
- Create REST API endpoints
- Deploy to production environment

---

## 📄 License

This project is open source and available for educational and portfolio purposes.

---

## 👨‍💻 Author

**Agentic AI Campaign Analytics & Insight Assistant**

Built as a demonstration of:
- Production-ready GenAI applications
- LangChain & LCEL mastery
- RAG implementation
- Agentic AI workflows
- Professional software engineering

**Perfect for:** Technical interviews, portfolio demonstration, and learning modern AI development.

---

## ✉️ Support

For questions or issues:
1. Check the troubleshooting section
2. Review code comments
3. Check LangChain documentation
4. Review agent implementations

---

**Last Updated:** May 2026

**Status:** ✅ Production Ready | 🎓 Interview Ready | 📚 Learning Resource
