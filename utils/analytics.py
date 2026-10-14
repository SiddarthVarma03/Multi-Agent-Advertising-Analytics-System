"""
Analytics and KPI calculations for campaign data.
Processes campaign CSV data and computes key metrics.
"""

import pandas as pd
import numpy as np


def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate key performance indicators from campaign data.
    
    Args:
        df (pd.DataFrame): Campaign data with columns: Campaign, Impressions, Clicks, Revenue
        
    Returns:
        dict: Dictionary containing all calculated KPIs
    """
    
    # Validate required columns
    required_columns = ['Campaign', 'Impressions', 'Clicks', 'Revenue']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"DataFrame must contain columns: {required_columns}")
    
    # Convert to numeric (handle errors)
    df['Impressions'] = pd.to_numeric(df['Impressions'], errors='coerce')
    df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce')
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
    
    # Remove rows with NaN values
    df = df.dropna()
    
    # Calculate metrics
    total_impressions = df['Impressions'].sum()
    total_clicks = df['Clicks'].sum()
    total_revenue = df['Revenue'].sum()
    
    # Avoid division by zero
    if total_impressions == 0:
        avg_ctr = 0
        avg_cpm = 0
    else:
        # CTR = (Clicks / Impressions) * 100
        avg_ctr = (total_clicks / total_impressions) * 100
        # CPM = (Revenue / Impressions) * 1000
        avg_cpm = (total_revenue / total_impressions) * 1000
    
    # Calculate per-campaign metrics
    df_calc = df.copy()
    df_calc['CTR'] = (df_calc['Clicks'] / df_calc['Impressions'] * 100).round(2)
    df_calc['CPM'] = (df_calc['Revenue'] / df_calc['Impressions'] * 1000).round(2)
    
    kpis = {
        'total_impressions': int(total_impressions),
        'total_clicks': int(total_clicks),
        'total_revenue': round(total_revenue, 2),
        'avg_ctr': round(avg_ctr, 2),
        'avg_cpm': round(avg_cpm, 2),
        'campaign_count': len(df),
        'df': df_calc  # Return processed dataframe
    }
    
    return kpis


def detect_anomalies(df: pd.DataFrame, kpis: dict) -> list:
    """
    Detect anomalies in campaign performance.
    
    Args:
        df (pd.DataFrame): Campaign data with metrics
        kpis (dict): Calculated KPIs
        
    Returns:
        list: List of anomalies detected
    """
    anomalies = []
    
    avg_ctr = kpis['avg_ctr']
    avg_cpm = kpis['avg_cpm']
    
    for idx, row in df.iterrows():
        ctr = row['CTR']
        cpm = row['CPM']
        campaign = row['Campaign']
        
        # Low CTR anomaly (< 50% of average)
        if ctr < avg_ctr * 0.5 and avg_ctr > 0:
            anomalies.append({
                'type': 'Low CTR',
                'campaign': campaign,
                'value': f"{ctr:.2f}%",
                'severity': 'Medium',
                'description': f"CTR is {ctr:.2f}%, significantly below average {avg_ctr:.2f}%"
            })
        
        # High CPM anomaly (> 150% of average)
        if cpm > avg_cpm * 1.5 and avg_cpm > 0:
            anomalies.append({
                'type': 'High CPM',
                'campaign': campaign,
                'value': f"${cpm:.2f}",
                'severity': 'High',
                'description': f"CPM is ${cpm:.2f}, significantly above average ${avg_cpm:.2f}"
            })
        
        # Very low revenue
        if row['Revenue'] == 0 or row['Revenue'] < kpis['total_revenue'] * 0.01:
            anomalies.append({
                'type': 'Low Revenue',
                'campaign': campaign,
                'value': f"${row['Revenue']:.2f}",
                'severity': 'Medium',
                'description': f"Campaign generated minimal revenue"
            })
    
    return anomalies


def get_top_campaigns(df: pd.DataFrame, metric: str = 'Revenue', n: int = 3) -> pd.DataFrame:
    """
    Get top performing campaigns by specified metric.
    
    Args:
        df (pd.DataFrame): Campaign data
        metric (str): Metric to sort by (Revenue, Clicks, CTR, CPM)
        n (int): Number of top campaigns to return
        
    Returns:
        pd.DataFrame: Top n campaigns
    """
    if metric == 'Revenue':
        return df.nlargest(n, 'Revenue')[['Campaign', 'Revenue', 'Clicks', 'Impressions', 'CTR', 'CPM']]
    elif metric == 'Clicks':
        return df.nlargest(n, 'Clicks')[['Campaign', 'Clicks', 'Revenue', 'Impressions', 'CTR', 'CPM']]
    elif metric == 'CTR':
        return df.nlargest(n, 'CTR')[['Campaign', 'CTR', 'Revenue', 'Clicks', 'CPM']]
    elif metric == 'CPM':
        return df.nsmallest(n, 'CPM')[['Campaign', 'CPM', 'Revenue', 'Clicks', 'CTR']]
    else:
        return df.head(n)


def get_campaign_summary(df: pd.DataFrame) -> str:
    """
    Generate a text summary of campaign data.
    
    Args:
        df (pd.DataFrame): Campaign data
        
    Returns:
        str: Text summary
    """
    summary = f"""
    Campaign Performance Summary:
    - Number of Campaigns: {len(df)}
    - Total Impressions: {df['Impressions'].sum():,}
    - Total Clicks: {df['Clicks'].sum():,}
    - Total Revenue: ${df['Revenue'].sum():,.2f}
    - Average CTR: {df['CTR'].mean():.2f}%
    - Average CPM: ${df['CPM'].mean():.2f}
    - Best Performing Campaign: {df.loc[df['Revenue'].idxmax(), 'Campaign']}
    """
    return summary
