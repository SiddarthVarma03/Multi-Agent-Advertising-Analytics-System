"""
Plotly chart generation for analytics dashboard.
Creates interactive visualizations for campaign data.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def create_revenue_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create interactive revenue comparison chart.
    
    Args:
        df (pd.DataFrame): Campaign data with Revenue and Campaign columns
        
    Returns:
        go.Figure: Plotly figure
    """
    fig = px.bar(
        df.sort_values('Revenue', ascending=False),
        x='Campaign',
        y='Revenue',
        title='Revenue by Campaign',
        labels={'Revenue': 'Revenue ($)', 'Campaign': 'Campaign Name'},
        color='Revenue',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    return fig


def create_ctr_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create CTR (Click-Through Rate) comparison chart.
    
    Args:
        df (pd.DataFrame): Campaign data with CTR column
        
    Returns:
        go.Figure: Plotly figure
    """
    fig = px.bar(
        df.sort_values('CTR', ascending=False),
        x='Campaign',
        y='CTR',
        title='Click-Through Rate (CTR) by Campaign',
        labels={'CTR': 'CTR (%)', 'Campaign': 'Campaign Name'},
        color='CTR',
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    return fig


def create_cpm_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create CPM (Cost Per Mille) comparison chart.
    
    Args:
        df (pd.DataFrame): Campaign data with CPM column
        
    Returns:
        go.Figure: Plotly figure
    """
    fig = px.bar(
        df.sort_values('CPM', ascending=True),
        x='Campaign',
        y='CPM',
        title='Cost Per Thousand Impressions (CPM)',
        labels={'CPM': 'CPM ($)', 'Campaign': 'Campaign Name'},
        color='CPM',
        color_continuous_scale='Reds_r'
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    return fig


def create_impressions_vs_clicks(df: pd.DataFrame) -> go.Figure:
    """
    Create scatter plot of Impressions vs Clicks.
    
    Args:
        df (pd.DataFrame): Campaign data
        
    Returns:
        go.Figure: Plotly figure
    """
    fig = px.scatter(
        df,
        x='Impressions',
        y='Clicks',
        size='Revenue',
        color='CTR',
        hover_data=['Campaign'],
        title='Impressions vs Clicks (size = Revenue)',
        labels={'Impressions': 'Impressions', 'Clicks': 'Clicks'},
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=400, hovermode='closest')
    return fig


def create_metric_distribution(df: pd.DataFrame, metric: str = 'CTR') -> go.Figure:
    """
    Create distribution histogram for specified metric.
    
    Args:
        df (pd.DataFrame): Campaign data
        metric (str): Metric to visualize (CTR, CPM, Revenue)
        
    Returns:
        go.Figure: Plotly figure
    """
    fig = go.Figure(data=[
        go.Histogram(x=df[metric], nbinsx=15, name=metric)
    ])
    fig.update_layout(
        title=f'{metric} Distribution',
        xaxis_title=metric,
        yaxis_title='Frequency',
        height=400,
        showlegend=False
    )
    return fig


def create_performance_gauge(value: float, title: str, max_value: float = 100) -> go.Figure:
    """
    Create gauge chart for KPI visualization.
    
    Args:
        value (float): Current metric value
        title (str): Title of the gauge
        max_value (float): Maximum value for gauge scale
        
    Returns:
        go.Figure: Plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value * 0.5], 'color': "lightgray"},
                {'range': [max_value * 0.5, max_value], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    fig.update_layout(height=350)
    return fig


def create_campaign_comparison_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create formatted campaign comparison table.
    
    Args:
        df (pd.DataFrame): Campaign data
        
    Returns:
        pd.DataFrame: Formatted dataframe for display
    """
    display_df = df[['Campaign', 'Impressions', 'Clicks', 'Revenue', 'CTR', 'CPM']].copy()
    
    # Format numeric columns
    display_df['Impressions'] = display_df['Impressions'].apply(lambda x: f"{int(x):,}")
    display_df['Clicks'] = display_df['Clicks'].apply(lambda x: f"{int(x):,}")
    display_df['Revenue'] = display_df['Revenue'].apply(lambda x: f"${x:,.2f}")
    display_df['CTR'] = display_df['CTR'].apply(lambda x: f"{x:.2f}%")
    display_df['CPM'] = display_df['CPM'].apply(lambda x: f"${x:.2f}")
    
    return display_df
