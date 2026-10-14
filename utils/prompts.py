"""
Prompt templates for AI-generated insights and responses.
Used throughout the application for LLM interactions.
"""

# ==================== ANALYTICS INSIGHTS ====================

CAMPAIGN_ANALYSIS_PROMPT = """
Analyze the following campaign performance data and provide insights:

Campaign Data:
{campaign_data}

KPI Summary:
- Total Revenue: ${total_revenue:,.2f}
- Total Impressions: {total_impressions:,}
- Total Clicks: {total_clicks:,}
- Average CTR: {avg_ctr:.2f}%
- Average CPM: ${avg_cpm:.2f}

Provide:
1. Performance summary (2-3 sentences)
2. Top performing campaigns
3. Underperforming campaigns
4. Key trends observed

Be specific and data-driven.
"""

ANOMALY_DETECTION_PROMPT = """
Identify anomalies in the following campaign data:

Campaign Data:
{campaign_data}

Provide:
1. Abnormal patterns detected
2. Possible reasons for anomalies
3. Recommended actions
4. Severity level (Low/Medium/High)

Format as actionable insights.
"""

OPTIMIZATION_PROMPT = """
Based on the campaign performance data below, provide optimization recommendations:

Campaign Data:
{campaign_data}

Current KPIs:
- Average CTR: {avg_ctr:.2f}%
- Average CPM: ${avg_cpm:.2f}
- Total Revenue: ${total_revenue:,.2f}

Provide specific, actionable recommendations to:
1. Improve CTR
2. Reduce CPM
3. Increase overall revenue
4. Optimize campaign targeting

Each recommendation should include expected impact.
"""

EXECUTIVE_SUMMARY_PROMPT = """
Generate an executive summary for campaign performance:

Campaign Data:
{campaign_data}

KPI Summary:
- Total Revenue: ${total_revenue:,.2f}
- Average CTR: {avg_ctr:.2f}%
- Average CPM: ${avg_cpm:.2f}

Create a professional executive summary (150-200 words) including:
1. Overall performance status
2. Key achievements
3. Areas of concern
4. Strategic recommendations

Use professional business language.
"""

# ==================== RAG RETRIEVAL ====================

RAG_CONTEXT_PROMPT = """
Use the following context from knowledge documents to answer the question:

Context:
{context}

Question: {question}

Provide a comprehensive answer based on the context. If the context doesn't contain relevant information, state that clearly.
"""

# ==================== GENERAL INSIGHTS ====================

QUESTION_ANSWERING_PROMPT = """
Answer the following question based on the provided context:

Context:
{context}

Question: {question}

Provide a clear, accurate, and helpful answer.
"""

# ==================== SAMPLE INSIGHTS ====================

def format_campaign_analysis(df, metrics):
    """Helper function to format campaign data for prompts."""
    campaign_data_str = df.to_string(index=False)
    return CAMPAIGN_ANALYSIS_PROMPT.format(
        campaign_data=campaign_data_str,
        total_revenue=metrics['total_revenue'],
        total_impressions=metrics['total_impressions'],
        total_clicks=metrics['total_clicks'],
        avg_ctr=metrics['avg_ctr'],
        avg_cpm=metrics['avg_cpm']
    )

def format_optimization_prompt(df, metrics):
    """Helper function to format optimization request."""
    campaign_data_str = df.to_string(index=False)
    return OPTIMIZATION_PROMPT.format(
        campaign_data=campaign_data_str,
        avg_ctr=metrics['avg_ctr'],
        avg_cpm=metrics['avg_cpm'],
        total_revenue=metrics['total_revenue']
    )

def format_anomaly_detection(df):
    """Helper function for anomaly detection."""
    campaign_data_str = df.to_string(index=False)
    return ANOMALY_DETECTION_PROMPT.format(campaign_data=campaign_data_str)

def format_executive_summary(df, metrics):
    """Helper function for executive summary."""
    campaign_data_str = df.to_string(index=False)
    return EXECUTIVE_SUMMARY_PROMPT.format(
        campaign_data=campaign_data_str,
        total_revenue=metrics['total_revenue'],
        avg_ctr=metrics['avg_ctr'],
        avg_cpm=metrics['avg_cpm']
    )
