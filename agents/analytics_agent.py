"""
Analytics Agent: Responsible for KPI analysis and anomaly detection.

Part of the agentic AI workflow:
CSV Upload → Analytics Agent → Retrieval Agent → Recommendation Agent → Reporting Agent

This agent specifically handles:
- KPI calculations
- Performance analysis
- Anomaly detection
- Statistical insights
"""

import pandas as pd
from utils.analytics import calculate_kpis, detect_anomalies, get_top_campaigns
from utils.prompts import format_campaign_analysis, format_anomaly_detection
from utils.groq_helper import generate_response


class AnalyticsAgent:
    """
    Analytics Agent for campaign data analysis.
    
    Responsibilities:
    - Calculate KPIs (CTR, CPM, Revenue)
    - Detect anomalies
    - Provide statistical summaries
    - Generate analysis insights
    """
    
    def __init__(self):
        self.last_analysis = None
        self.kpis = None
        self.anomalies = None
    
    def analyze_campaign_data(self, df: pd.DataFrame) -> dict:
        """
        Perform comprehensive analysis on campaign data.
        
        AI AUTOMATION: Uses LLM to generate insights from calculated KPIs.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            dict: Analysis results including KPIs, anomalies, and AI insights
        """
        try:
            # Step 1: Calculate KPIs
            self.kpis = calculate_kpis(df)
            
            # Step 2: Detect anomalies
            self.anomalies = detect_anomalies(self.kpis['df'], self.kpis)
            
            # Step 3: Get top performers
            top_revenue = get_top_campaigns(self.kpis['df'], 'Revenue', 3)
            top_ctr = get_top_campaigns(self.kpis['df'], 'CTR', 3)
            
            # Step 4: Generate AI-powered insights
            # AI AUTOMATION: LLM analyzes the data
            analysis_prompt = format_campaign_analysis(
                self.kpis['df'],
                self.kpis
            )
            ai_analysis = generate_response(analysis_prompt)
            
            # Store results
            self.last_analysis = {
                'kpis': self.kpis,
                'anomalies': self.anomalies,
                'top_revenue_campaigns': top_revenue,
                'top_ctr_campaigns': top_ctr,
                'ai_analysis': ai_analysis
            }
            
            return self.last_analysis
            
        except Exception as e:
            return {'error': f"Analytics analysis failed: {str(e)}"}
    
    def detect_campaign_anomalies(self, df: pd.DataFrame) -> dict:
        """
        Detect and analyze anomalies in campaign performance.
        
        AI AUTOMATION: Uses LLM to explain anomalies.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            dict: Anomaly detection results with AI explanations
        """
        try:
            if not self.kpis:
                self.kpis = calculate_kpis(df)
            
            # Detect anomalies
            anomalies = detect_anomalies(self.kpis['df'], self.kpis)
            
            # Generate AI explanation for anomalies
            # AI AUTOMATION: LLM provides context and recommendations
            anomaly_prompt = format_anomaly_detection(self.kpis['df'])
            ai_explanation = generate_response(anomaly_prompt)
            
            return {
                'detected_anomalies': anomalies,
                'anomaly_count': len(anomalies),
                'ai_explanation': ai_explanation
            }
            
        except Exception as e:
            return {'error': f"Anomaly detection failed: {str(e)}"}
    
    def get_performance_summary(self) -> dict:
        """
        Get performance summary from last analysis.
        
        Returns:
            dict: Summary of campaign performance
        """
        if not self.last_analysis:
            return {'message': 'No analysis performed yet'}
        
        return {
            'total_revenue': self.last_analysis['kpis']['total_revenue'],
            'total_impressions': self.last_analysis['kpis']['total_impressions'],
            'total_clicks': self.last_analysis['kpis']['total_clicks'],
            'avg_ctr': self.last_analysis['kpis']['avg_ctr'],
            'avg_cpm': self.last_analysis['kpis']['avg_cpm'],
            'campaign_count': self.last_analysis['kpis']['campaign_count'],
            'anomaly_count': len(self.last_analysis['anomalies'])
        }
    
    def get_alert_metrics(self) -> list:
        """
        Get alerts for campaigns with poor performance.
        
        Returns:
            list: List of alerts with severity levels
        """
        if not self.last_analysis:
            return []
        
        alerts = []
        
        # Alert for low average CTR
        if self.last_analysis['kpis']['avg_ctr'] < 2:
            alerts.append({
                'type': 'warning',
                'message': f"⚠️ Low Average CTR: {self.last_analysis['kpis']['avg_ctr']:.2f}%"
            })
        
        # Alert for revenue concerns
        total_campaigns = self.last_analysis['kpis']['campaign_count']
        low_revenue_campaigns = sum(1 for a in self.last_analysis['anomalies'] 
                                   if a['type'] == 'Low Revenue')
        if low_revenue_campaigns > total_campaigns * 0.3:
            alerts.append({
                'type': 'error',
                'message': f"🚨 {low_revenue_campaigns} campaigns with low revenue"
            })
        
        # Alert for high CPM
        high_cpm_anomalies = sum(1 for a in self.last_analysis['anomalies'] 
                                if a['type'] == 'High CPM')
        if high_cpm_anomalies > 0:
            alerts.append({
                'type': 'warning',
                'message': f"⚠️ {high_cpm_anomalies} campaigns with high CPM"
            })
        
        return alerts
