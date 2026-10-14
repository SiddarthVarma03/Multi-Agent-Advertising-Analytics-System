"""
Agentic AI Campaign Analytics & Insight Assistant
Main Streamlit Application

ARCHITECTURE:
- Streamlit UI (Frontend)
- Agent Layer (Analytics, Retrieval, Recommendation, Reporting)
- Utility Layer (Analytics, Charts, RAG, Prompts)
- LLM Layer (Groq API via LangChain)

WORKFLOW:
CSV Upload → Analytics Agent → Retrieval Agent → Recommendation Agent → Reporting Agent → UI Display

KEY TECHNOLOGIES:
- Streamlit: Web UI framework
- Groq API: LLM for insights
- LangChain: LCEL chains and RAG
- FAISS: Vector similarity search
- Plotly: Interactive visualizations
- Pandas: Data processing
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# Import agents
from agents.analytics_agent import AnalyticsAgent
from agents.retrieval_agent import RetrievalAgent
from agents.recommendation_agent import RecommendationAgent
from agents.reporting_agent import ReportingAgent

# Import utilities
from utils.analytics import calculate_kpis, get_campaign_summary
from utils.charts import (
    create_revenue_chart, create_ctr_chart, create_cpm_chart,
    create_impressions_vs_clicks, create_campaign_comparison_table,
    create_performance_gauge, create_metric_distribution
)
from utils.groq_helper import check_api_status


# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="Campaign Analytics AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)


# ==================== SESSION STATE INITIALIZATION ====================

if 'analytics_agent' not in st.session_state:
    st.session_state.analytics_agent = AnalyticsAgent()

if 'retrieval_agent' not in st.session_state:
    st.session_state.retrieval_agent = RetrievalAgent()

if 'recommendation_agent' not in st.session_state:
    st.session_state.recommendation_agent = RecommendationAgent()

if 'reporting_agent' not in st.session_state:
    st.session_state.reporting_agent = ReportingAgent()

if 'campaign_data' not in st.session_state:
    st.session_state.campaign_data = None

if 'kpis' not in st.session_state:
    st.session_state.kpis = None

if 'anomalies' not in st.session_state:
    st.session_state.anomalies = None


# ==================== SIDEBAR ====================

with st.sidebar:
    st.title("📊 Campaign Analytics AI")
    st.markdown("---")
    
    # API Status
    st.subheader("🔌 API Status")
    api_status = check_api_status()
    if api_status['configured']:
        st.success(api_status['message'])
    else:
        st.error(api_status['message'])
    
    st.markdown("---")
    
    # CSV Upload
    st.subheader("📁 Upload Campaign Data")
    csv_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if csv_file:
        try:
            df = pd.read_csv(csv_file)
            st.session_state.campaign_data = df
            
            # Validate columns
            required_columns = ['Campaign', 'Impressions', 'Clicks', 'Revenue']
            if all(col in df.columns for col in required_columns):
                st.success(f"✅ CSV loaded: {len(df)} campaigns")
                
                # Auto-analyze on upload
                with st.spinner("Analyzing campaign data..."):
                    analysis = st.session_state.analytics_agent.analyze_campaign_data(df)
                    st.session_state.kpis = analysis.get('kpis')
                    st.session_state.anomalies = analysis.get('anomalies')
            else:
                st.error(f"Required columns: {required_columns}")
        except Exception as e:
            st.error(f"Error loading CSV: {str(e)}")
    
    st.markdown("---")
    
    # PDF Upload for RAG
    st.subheader("📄 Upload Knowledge Documents")
    st.write("Upload PDFs for RAG-based Q&A")
    
    pdf_files = st.file_uploader(
        "Upload PDF files",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if pdf_files:
        if st.button("Process PDFs for RAG", key="process_pdfs"):
            with st.spinner("Processing PDFs and building vector store..."):
                # Save uploaded files temporarily
                pdf_paths = []
                for pdf_file in pdf_files:
                    temp_path = f"temp_{pdf_file.name}"
                    with open(temp_path, 'wb') as f:
                        f.write(pdf_file.getbuffer())
                    pdf_paths.append(temp_path)
                
                # Process with Retrieval Agent
                result = st.session_state.retrieval_agent.process_pdf_documents(pdf_paths)
                
                if result['success']:
                    st.success(result['message'])
                else:
                    st.error(result['message'])
                
                # Clean up temp files
                for path in pdf_paths:
                    if os.path.exists(path):
                        os.remove(path)
    
    # Vectorstore status
    vectorstore_info = st.session_state.retrieval_agent.get_vectorstore_info()
    if vectorstore_info['retriever_ready']:
        st.info("✅ Knowledge base ready for Q&A")
    
    st.markdown("---")
    st.markdown("Built with Streamlit, LangChain, FAISS, and Groq AI")


# ==================== MAIN CONTENT ====================

# Title and Description
st.title("🤖 Agentic AI Campaign Analytics & Insight Assistant")
st.markdown("""
This application demonstrates production-ready AI automation for campaign analytics.
It combines **Analytics**, **Retrieval (RAG)**, **Recommendation**, and **Reporting** agents.
""")

# Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "🔍 Insights & Anomalies",
    "💡 Recommendations",
    "❓ RAG Q&A",
    "📋 Reports"
])


# ==================== TAB 1: DASHBOARD ====================

with tab1:
    if st.session_state.campaign_data is not None and st.session_state.kpis is not None:
        st.subheader("Campaign Performance Dashboard")
        
        # KPI Cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        kpis = st.session_state.kpis
        
        with col1:
            st.metric(
                "Total Revenue",
                f"${kpis['total_revenue']:,.0f}",
                delta="Campaign Total"
            )
        
        with col2:
            st.metric(
                "Total Impressions",
                f"{kpis['total_impressions']:,}",
                delta="Reach"
            )
        
        with col3:
            st.metric(
                "Total Clicks",
                f"{kpis['total_clicks']:,}",
                delta="Engagement"
            )
        
        with col4:
            st.metric(
                "Avg CTR",
                f"{kpis['avg_ctr']:.2f}%",
                delta="Click-Through Rate"
            )
        
        with col5:
            st.metric(
                "Avg CPM",
                f"${kpis['avg_cpm']:.2f}",
                delta="Cost Per Mille"
            )
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_revenue_chart(kpis['df']),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                create_ctr_chart(kpis['df']),
                use_container_width=True
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_cpm_chart(kpis['df']),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                create_impressions_vs_clicks(kpis['df']),
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Campaign Table
        st.subheader("Campaign Details")
        campaign_table = create_campaign_comparison_table(kpis['df'])
        st.dataframe(campaign_table, use_container_width=True)
        
    else:
        st.info("👆 Upload a CSV file in the sidebar to view the dashboard")


# ==================== TAB 2: INSIGHTS & ANOMALIES ====================

with tab2:
    st.subheader("AI-Powered Insights & Anomalies")
    
    if st.session_state.campaign_data is not None:
        # Alerts
        if st.session_state.anomalies and len(st.session_state.anomalies) > 0:
            st.subheader("⚠️ Detected Anomalies")
            
            for anomaly in st.session_state.anomalies:
                severity = anomaly.get('severity', 'Info')
                severity_icon = "🔴" if severity == "High" else "🟡" if severity == "Medium" else "🟢"
                
                with st.expander(f"{severity_icon} {anomaly['type']} - {anomaly['campaign']}"):
                    st.write(f"**Value:** {anomaly['value']}")
                    st.write(f"**Description:** {anomaly['description']}")
                    st.write(f"**Severity:** {severity}")
        
        # AI-Generated Analysis
        st.markdown("---")
        st.subheader("📈 AI Analysis & Insights")
        
        if 'ai_analysis' in st.session_state.analytics_agent.last_analysis:
            analysis_text = st.session_state.analytics_agent.last_analysis['ai_analysis']
            st.markdown(analysis_text)
        else:
            st.info("Generate analysis by uploading CSV data")
        
        # Alert Status
        st.markdown("---")
        st.subheader("Alert Status")
        alerts = st.session_state.analytics_agent.get_alert_metrics()
        
        if alerts:
            for alert in alerts:
                if alert['type'] == 'error':
                    st.error(alert['message'])
                elif alert['type'] == 'warning':
                    st.warning(alert['message'])
                else:
                    st.info(alert['message'])
        else:
            st.success("✅ No critical alerts at this time")
        
    else:
        st.info("👆 Upload a CSV file to view insights")


# ==================== TAB 3: RECOMMENDATIONS ====================

with tab3:
    st.subheader("💡 AI Optimization Recommendations")
    
    if st.session_state.campaign_data is not None:
        if st.button("Generate Optimization Recommendations", key="gen_rec"):
            with st.spinner("Generating AI recommendations..."):
                recommendations = st.session_state.recommendation_agent.generate_optimization_recommendations(
                    st.session_state.campaign_data
                )
                
                if 'error' in recommendations:
                    st.error(recommendations['error'])
                else:
                    # AI-Generated Recommendations
                    st.subheader("🤖 AI-Generated Recommendations")
                    st.markdown(recommendations['ai_generated_recommendations'])
                    
                    st.markdown("---")
                    
                    # Specific Recommendations
                    st.subheader("📋 Specific Action Items")
                    
                    for rec in recommendations['specific_recommendations']:
                        with st.expander(f"{rec['area']} (Priority: {rec['priority']})"):
                            st.write(f"**Current Value:** {rec['current_value']}")
                            st.write(f"**Recommendation:** {rec['recommendation']}")
                    
                    st.markdown("---")
                    
                    # Budget Optimization
                    st.subheader("💰 Budget Optimization Strategy")
                    budget_strategy = st.session_state.recommendation_agent.get_budget_optimization_suggestions(
                        st.session_state.campaign_data
                    )
                    
                    if 'error' not in budget_strategy:
                        st.write(f"**Total Campaign Budget:** ${budget_strategy['total_budget']:,.2f}")
                        
                        for suggestion in budget_strategy['reallocation_suggestions']:
                            st.info(f"**{suggestion['action']}**")
                            st.write(f"Campaigns: {', '.join(suggestion['campaigns'])}")
                            if 'budget_freed' in suggestion:
                                st.write(f"Budget Impact: ${suggestion['budget_freed']:,.2f}")
                            if 'suggested_increase' in suggestion:
                                st.write(f"Suggested Increase: ${suggestion['suggested_increase']:,.2f}")
    else:
        st.info("👆 Upload a CSV file to generate recommendations")


# ==================== TAB 4: RAG Q&A ====================

with tab4:
    st.subheader("❓ Knowledge Base Q&A (RAG)")
    
    vectorstore_status = st.session_state.retrieval_agent.get_vectorstore_info()
    
    if vectorstore_status['retriever_ready']:
        st.success("✅ Knowledge base is ready for questions")
        
        # Question Input
        user_question = st.text_input(
            "Ask a question about your knowledge documents:",
            placeholder="e.g., What are the best practices for campaign optimization?"
        )
        
        if user_question and st.button("Get AI Answer", key="rag_answer"):
            with st.spinner("Searching knowledge base and generating answer..."):
                # RAG Agent processes question
                result = st.session_state.retrieval_agent.answer_question_with_rag(user_question)
                
                if result['success']:
                    st.subheader("💬 AI Answer")
                    st.markdown(result['answer'])
                    
                    st.markdown("---")
                    
                    # Show Retrieved Context
                    st.subheader("📚 Retrieved Context")
                    if result['retrieved_context']:
                        for i, chunk in enumerate(result['retrieved_context'], 1):
                            with st.expander(f"Context Chunk {i}"):
                                st.write(chunk[:500] + "..." if len(chunk) > 500 else chunk)
                else:
                    st.error(result['answer'])
        
        # Knowledge Base Summary
        st.markdown("---")
        st.subheader("Knowledge Base Status")
        kb_info = st.session_state.retrieval_agent.get_knowledge_base_summary()
        st.info(kb_info)
        
    else:
        st.warning("📄 Upload PDF documents in the sidebar to enable Q&A")


# ==================== TAB 5: REPORTS ====================

with tab5:
    st.subheader("📋 Reports & Export")
    
    if st.session_state.campaign_data is not None:
        # Report Type Selection
        report_type = st.selectbox(
            "Select Report Type",
            ["Executive Report", "Campaign Performance Report", "Insights Report"]
        )
        
        if st.button("Generate Report", key="gen_report"):
            with st.spinner("Generating report..."):
                
                if report_type == "Executive Report":
                    report = st.session_state.reporting_agent.generate_executive_report(
                        st.session_state.campaign_data
                    )
                
                elif report_type == "Campaign Performance Report":
                    report = st.session_state.reporting_agent.generate_campaign_performance_report(
                        st.session_state.campaign_data,
                        st.session_state.anomalies
                    )
                
                else:  # Insights Report
                    analytics_results = st.session_state.analytics_agent.last_analysis or {}
                    report = st.session_state.reporting_agent.generate_insights_report(
                        analytics_results
                    )
                
                if 'error' in report:
                    st.error(report['error'])
                else:
                    # Display Report
                    st.markdown("---")
                    
                    if 'report_type' in report:
                        st.subheader(report['report_type'])
                    
                    if 'generated_at' in report:
                        st.caption(f"Generated: {report['generated_at']}")
                    
                    if 'executive_summary' in report:
                        st.write(report['executive_summary'])
                    
                    if 'kpi_summary' in report:
                        st.subheader("KPI Summary")
                        kpi_cols = st.columns(len(report['kpi_summary']))
                        for col, (key, value) in zip(kpi_cols, report['kpi_summary'].items()):
                            with col:
                                st.metric(key.replace('_', ' ').title(), value)
                    
                    if 'top_revenue_campaigns' in report and report['top_revenue_campaigns']:
                        st.subheader("Top Revenue Campaigns")
                        top_df = pd.DataFrame(report['top_revenue_campaigns'])
                        st.dataframe(top_df, use_container_width=True)
                    
                    if 'anomalies' in report:
                        st.subheader("Anomalies Detected")
                        if report['anomalies']:
                            for anom in report['anomalies']:
                                st.info(f"{anom.get('type')}: {anom.get('description')}")
                        else:
                            st.success("No anomalies detected")
    
    else:
        st.info("👆 Upload a CSV file to generate reports")


# ==================== FOOTER ====================

st.markdown("---")
st.markdown("""
**Agentic AI Campaign Analytics & Insight Assistant** | 
Built with Streamlit, LangChain, FAISS, and Groq API

**Key Features:**
- 🤖 Agentic Workflow (Analytics → Retrieval → Recommendation → Reporting)
- 📊 Interactive Dashboard with Plotly Charts
- 🧠 LangChain LCEL Chains for RAG
- 🔍 FAISS Vector Search for Document Retrieval
- 🤖 Groq AI for Intelligent Insights
- 📄 Comprehensive Reporting

**Interview Highlights:**
- Real LangChain LCEL implementation
- Production-ready RAG with FAISS
- AI Automation workflow
- Modular agent architecture
- Professional UI with Streamlit
""")
