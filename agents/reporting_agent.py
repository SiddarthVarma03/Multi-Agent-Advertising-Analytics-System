"""
Reporting Agent: Responsible for generating executive reports and summaries.

Part of the agentic AI workflow:
CSV Upload → Analytics Agent → Retrieval Agent → Recommendation Agent → Reporting Agent

This agent specifically handles:
- Executive summaries
- Campaign reports
- Performance visualizations
- AI-generated insights compilation
"""

import pandas as pd
from datetime import datetime
from utils.analytics import calculate_kpis, get_top_campaigns, get_campaign_summary
from utils.prompts import format_executive_summary
from utils.groq_helper import generate_response


class ReportingAgent:
    """
    Reporting Agent for generating comprehensive reports.
    
    Responsibilities:
    - Generate executive summaries
    - Compile campaign reports
    - Create performance reports
    - Generate AI-powered insights summaries
    
    AI AUTOMATION: Uses Groq LLM to create professional, narrative reports
    from structured campaign data.
    """
    
    def __init__(self):
        self.report_history = []
        self.last_report = None
    
    def generate_executive_report(self, df: pd.DataFrame, include_recommendations: dict = None) -> dict:
        """
        Generate comprehensive executive report.
        
        AI AUTOMATION: LLM creates professional executive summary.
        
        Args:
            df (pd.DataFrame): Campaign data
            include_recommendations (dict): Optional recommendations to include
            
        Returns:
            dict: Complete executive report
        """
        try:
            # Calculate KPIs
            kpis = calculate_kpis(df)
            
            # Generate executive summary using LLM
            # AI AUTOMATION: Groq generates professional narrative
            executive_prompt = format_executive_summary(df, kpis)
            executive_summary = generate_response(executive_prompt)
            
            # Get top campaigns
            top_revenue_campaigns = get_top_campaigns(kpis['df'], 'Revenue', 3)
            top_ctr_campaigns = get_top_campaigns(kpis['df'], 'CTR', 3)
            
            # Compile report
            report = {
                'report_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'report_type': 'Executive Campaign Performance Report',
                'executive_summary': executive_summary,
                'kpi_summary': {
                    'total_revenue': f"${kpis['total_revenue']:,.2f}",
                    'total_impressions': f"{kpis['total_impressions']:,}",
                    'total_clicks': f"{kpis['total_clicks']:,}",
                    'average_ctr': f"{kpis['avg_ctr']:.2f}%",
                    'average_cpm': f"${kpis['avg_cpm']:.2f}",
                    'campaign_count': kpis['campaign_count']
                },
                'top_revenue_campaigns': top_revenue_campaigns.to_dict('records') if len(top_revenue_campaigns) > 0 else [],
                'top_ctr_campaigns': top_ctr_campaigns.to_dict('records') if len(top_ctr_campaigns) > 0 else [],
                'recommendations': include_recommendations if include_recommendations else None
            }
            
            self.last_report = report
            self.report_history.append(report)
            
            return report
            
        except Exception as e:
            return {'error': f"Report generation failed: {str(e)}"}
    
    def generate_campaign_performance_report(self, df: pd.DataFrame, anomalies: list = None) -> dict:
        """
        Generate detailed campaign performance report.
        
        Args:
            df (pd.DataFrame): Campaign data
            anomalies (list): Optional list of detected anomalies
            
        Returns:
            dict: Detailed performance report
        """
        try:
            kpis = calculate_kpis(df)
            
            report = {
                'report_type': 'Campaign Performance Report',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'performance_overview': {
                    'total_campaigns': kpis['campaign_count'],
                    'total_revenue': kpis['total_revenue'],
                    'total_impressions': kpis['total_impressions'],
                    'total_clicks': kpis['total_clicks'],
                    'average_ctr': kpis['avg_ctr'],
                    'average_cpm': kpis['avg_cpm']
                },
                'campaign_details': kpis['df'][['Campaign', 'Impressions', 'Clicks', 'Revenue', 'CTR', 'CPM']].to_dict('records'),
                'anomalies': anomalies if anomalies else [],
                'summary_text': get_campaign_summary(kpis['df'])
            }
            
            return report
            
        except Exception as e:
            return {'error': f"Performance report failed: {str(e)}"}
    
    def generate_insights_report(self, analytics_results: dict, retrieval_context: str = None) -> dict:
        """
        Generate comprehensive insights report combining multiple agents' outputs.
        
        Args:
            analytics_results (dict): Results from Analytics Agent
            retrieval_context (str): Optional context from Retrieval Agent
            
        Returns:
            dict: Consolidated insights report
        """
        try:
            report = {
                'report_type': 'AI-Powered Insights Report',
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'analytics_insights': analytics_results.get('ai_analysis', ''),
                'anomalies': analytics_results.get('anomalies', []),
                'anomaly_count': len(analytics_results.get('anomalies', [])),
                'retrieved_context': retrieval_context,
                'section_kpis': analytics_results.get('kpis', {}),
                'top_performers': {
                    'by_revenue': analytics_results.get('top_revenue_campaigns', {}).to_dict('records') if hasattr(analytics_results.get('top_revenue_campaigns', {}), 'to_dict') else [],
                    'by_ctr': analytics_results.get('top_ctr_campaigns', {}).to_dict('records') if hasattr(analytics_results.get('top_ctr_campaigns', {}), 'to_dict') else []
                }
            }
            
            return report
            
        except Exception as e:
            return {'error': f"Insights report failed: {str(e)}"}
    
    def generate_pdf_report_data(self, df: pd.DataFrame, kpis: dict) -> dict:
        """
        Generate data structure for PDF report export.
        
        Args:
            df (pd.DataFrame): Campaign data
            kpis (dict): Calculated KPIs
            
        Returns:
            dict: Data formatted for PDF generation
        """
        try:
            report_data = {
                'title': 'Campaign Analytics & Performance Report',
                'generation_date': datetime.now().strftime("%B %d, %Y"),
                'kpi_section': {
                    'total_revenue': f"${kpis['total_revenue']:,.2f}",
                    'total_impressions': f"{kpis['total_impressions']:,}",
                    'total_clicks': f"{kpis['total_clicks']:,}",
                    'avg_ctr': f"{kpis['avg_ctr']:.2f}%",
                    'avg_cpm': f"${kpis['avg_cpm']:.2f}"
                },
                'campaign_table': df[['Campaign', 'Impressions', 'Clicks', 'Revenue', 'CTR', 'CPM']].to_dict('records'),
                'charts_to_include': [
                    'Revenue by Campaign',
                    'CTR Comparison',
                    'CPM Analysis',
                    'Impressions vs Clicks'
                ]
            }
            
            return report_data
            
        except Exception as e:
            return {'error': f"PDF report data generation failed: {str(e)}"}
    
    def get_report_history(self, limit: int = 10) -> list:
        """
        Get report generation history.
        
        Args:
            limit (int): Maximum number of recent reports to return
            
        Returns:
            list: Recent reports
        """
        return self.report_history[-limit:]
    
    def get_last_report(self) -> dict:
        """Get the last generated report."""
        if not self.last_report:
            return {'message': 'No reports generated yet'}
        return self.last_report
