# Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Get API Key (2 minutes)
1. Go to https://aistudio.google.com/app/apikeys
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

### Step 2: Setup Project (2 minutes)
```bash
# Open terminal in project directory
cd ai-campaign-assistant

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure (1 minute)
1. Open `.env` file in project root
2. Replace `your_api_key_here` with your actual API key
3. Save file

### Step 4: Run App (30 seconds)
```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 📊 First Steps After Launch

### 1. Test with Sample Data (1 minute)
- Go to sidebar → "📁 Upload Campaign Data"
- Upload `data/sample_campaigns.csv`
- Dashboard auto-populates!

### 2. Explore Tabs
- **📊 Dashboard**: See KPIs and charts
- **🔍 Insights**: View anomalies and AI analysis
- **💡 Recommendations**: Get optimization suggestions
- **❓ RAG Q&A**: Will be ready after PDF upload
- **📋 Reports**: Generate professional reports

### 3. Upload Knowledge Documents (Optional)
- In sidebar, upload PDF file
- Click "Process PDFs for RAG"
- Wait for ✅ confirmation
- Now you can ask questions in RAG Q&A tab!

---

## 🎯 What to Try

### Test Campaign Analysis
1. Upload `data/sample_campaigns.csv`
2. Go to "🔍 Insights" tab
3. See AI-generated analysis of campaigns

### Generate Recommendations
1. Upload CSV
2. Go to "💡 Recommendations" tab
3. Click "Generate Optimization Recommendations"
4. Read AI suggestions for budget allocation

### Try RAG Q&A
1. Upload PDF from `docs/` folder
2. Process PDFs
3. In "❓ RAG Q&A" tab, try questions like:
   - "What is a good CTR benchmark?"
   - "How should I optimize my budget?"
   - "What are red flags in campaign performance?"

### Generate Report
1. Upload CSV
2. Go to "📋 Reports" tab
3. Select "Executive Report"
4. Click "Generate Report"
5. See professional summary!

---

## 🔧 Common Issues

### "GOOGLE_API_KEY not found"
**Solution:**
- Open `.env` file
- Add your actual API key
- Save file
- Restart Streamlit (Ctrl+C, then `streamlit run app.py`)

### "Retriever not initialized"
**Solution:**
- Upload PDF first
- Click "Process PDFs for RAG"
- Wait for ✅ success message

### "No modules named..."
**Solution:**
- Activate virtual environment: `venv\Scripts\activate`
- Install again: `pip install -r requirements.txt`

### Slow processing
**Solution:**
- Normal for first RAG query (model downloads)
- Subsequent queries are faster
- Check internet connection

---

## 📚 Project Structure

```
ai-campaign-assistant/
├── app.py                 ← Main app (run this!)
├── .env                   ← Add API key here
├── requirements.txt       ← Dependencies
│
├── data/
│   └── sample_campaigns.csv ← Test data
│
├── docs/
│   └── adtech_best_practices.txt ← For RAG demo
│
├── agents/                ← AI agents (don't edit yet)
├── utils/                 ← Helper functions
└── vectorstore/           ← Auto-created by RAG
```

---

## 🎓 Learning Path

**Day 1: Learn Basics**
- [ ] Read README.md
- [ ] Run with sample data
- [ ] Explore all tabs
- [ ] Understand what each tab does

**Day 2: Explore Code**
- [ ] Open `utils/prompts.py` - See LLM prompts
- [ ] Open `utils/rag_pipeline.py` - See LCEL chains
- [ ] Open `agents/analytics_agent.py` - See agent logic
- [ ] Run app with debugger

**Day 3: Modify & Experiment**
- [ ] Change prompts in `prompts.py`
- [ ] Add new chart type in `charts.py`
- [ ] Add new KPI calculation in `analytics.py`
- [ ] Test changes

**Day 4: Interview Prep**
- [ ] Practice explaining architecture
- [ ] Explain RAG workflow
- [ ] Discuss LangChain LCEL
- [ ] Talk about agents

---

## 🎤 Interview Script

When asked "Tell me about this project":

> "This is a production-ready GenAI application called 'Agentic AI Campaign Analytics Assistant'. It demonstrates practical implementation of modern AI/ML concepts.
>
> **Architecture**: Four specialized agents orchestrated sequentially - Analytics (KPI calc), Retrieval (RAG), Recommendation (suggestions), and Reporting (summaries).
>
> **Key Tech**: Built with Streamlit, LangChain LCEL chains, FAISS vector search, HuggingFace embeddings, and Gemini API.
>
> **RAG Implementation**: Real vector embeddings with FAISS for O(1) similarity search. Documents are chunked, embedded, and stored. When users ask questions, relevant chunks are retrieved and passed to LLM.
>
> **LCEL**: Used RunnablePassthrough and pipe operators to compose components elegantly. Shows in `rag_pipeline.py`.
>
> **Automation**: Automatically detects campaign anomalies, generates AI insights, provides optimization recommendations. All AI-powered.
>
> **Production Ready**: Error handling throughout, .env for security, modular architecture, responsive Streamlit UI."

---

## 📖 Next Steps

1. Get comfortable running the app
2. Try with your own CSV data
3. Read through the agent code
4. Practice explaining the architecture
5. Modify features to make it your own

---

## ❓ Need Help?

- **Issues with setup**: Check Troubleshooting in README.md
- **Code questions**: Read inline comments in files
- **LangChain help**: https://python.langchain.com/
- **Gemini API**: https://ai.google.dev/

---

## 🎯 Success Checklist

- [ ] API key added to .env
- [ ] `pip install -r requirements.txt` completed
- [ ] App runs: `streamlit run app.py`
- [ ] Uploaded sample CSV
- [ ] Dashboard populated with metrics
- [ ] Viewed insights/anomalies
- [ ] Generated recommendations
- [ ] Uploaded PDF and tried RAG Q&A
- [ ] Generated executive report
- [ ] Explored agent code
- [ ] Ready for interview!

---

**You're all set! Happy exploring! 🚀**
