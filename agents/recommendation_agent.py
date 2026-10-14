"""
Recommendation Agent: Responsible for generating optimization suggestions.

Part of the agentic AI workflow:
CSV Upload → Analytics Agent → Retrieval Agent → Recommendation Agent → Reporting Agent

This agent specifically handles:
- Performance optimization suggestions
- Campaign improvement recommendations
- Best practice advice
- Actionable insights for campaign managers
"""

import pandas as pd
from utils.analytics import calculate_kpis
from utils.prompts import format_optimization_prompt
from utils.groq_helper import generate_response


class RecommendationAgent:
    """
    Recommendation Agent for campaign optimization.
    
    Responsibilities:
    - Generate optimization suggestions based on KPIs
    - Provide best practice recommendations
    - Suggest targeting improvements
    - Recommend budget adjustments
    
    AI AUTOMATION: Uses Groq LLM to generate intelligent recommendations
    based on campaign performance data.
    """
    
    def __init__(self):
        self.last_recommendations = None
        self.optimization_history = []
    
    def generate_optimization_recommendations(self, df: pd.DataFrame) -> dict:
        """
        Generate AI-powered optimization recommendations for campaigns.
        
        AI AUTOMATION: LLM analyzes KPIs and generates specific recommendations.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            dict: Recommendations with specific action items
        """
        try:
            # Calculate KPIs
            kpis = calculate_kpis(df)
            
            # Generate optimization prompt with data
            optimization_prompt = format_optimization_prompt(df, kpis)
            
            # Use Groq to generate recommendations
            # AI AUTOMATION: LLM-powered recommendation engine
            ai_recommendations = generate_response(optimization_prompt)
            
            # Extract specific recommendations based on metrics
            specific_recommendations = self._extract_specific_recommendations(df, kpis)
            
            result = {
                'ai_generated_recommendations': ai_recommendations,
                'specific_recommendations': specific_recommendations,
                'kpi_summary': {
                    'avg_ctr': kpis['avg_ctr'],
                    'avg_cpm': kpis['avg_cpm'],
                    'total_revenue': kpis['total_revenue']
                }
            }
            
            self.last_recommendations = result
            self.optimization_history.append(result)
            
            return result
            
        except Exception as e:
            return {'error': f"Recommendation generation failed: {str(e)}"}
    
    def _extract_specific_recommendations(self, df: pd.DataFrame, kpis: dict) -> list:
        """
        Extract specific actionable recommendations based on metrics.
        
        Args:
            df (pd.DataFrame): Campaign data
            kpis (dict): Calculated KPIs
            
        Returns:
            list: List of specific recommendations
        """
        recommendations = []
        
        # CTR Improvement
        if kpis['avg_ctr'] < 2.5:
            recommendations.append({
                'area': 'CTR Optimization',
                'current_value': f"{kpis['avg_ctr']:.2f}%",
                'recommendation': 'CTR is below industry average. Consider: A/B testing ad creative, improving targeting, optimizing landing pages.',
                'priority': 'High'
            })
        
        # CPM Reduction
        if kpis['avg_cpm'] > 5:
            recommendations.append({
                'area': 'Cost Optimization',
                'current_value': f"${kpis['avg_cpm']:.2f}",
                'recommendation': 'CPM is higher than typical. Consider: Expanding audience reach, adjusting bid strategy, testing different placements.',
                'priority': 'High'
            })
        
        # Low performing campaigns
        low_revenue = df[df['Revenue'] < df['Revenue'].mean()]
        if len(low_revenue) > 0:
            recommendations.append({
                'area': 'Campaign Performance',
                'current_value': f"{len(low_revenue)} underperforming campaigns",
                'recommendation': f"Pause or optimize {len(low_revenue)} campaigns underperforming against benchmarks. Reallocate budget to top performers.",
                'priority': 'Medium'
            })
        
        # Top performer scaling
        top_performers = df[df['Revenue'] > df['Revenue'].quantile(0.75)]
        if len(top_performers) > 0:
            recommendations.append({
                'area': 'Budget Allocation',
                'current_value': f"{len(top_performers)} high-performing campaigns",
                'recommendation': f"Increase budget for {len(top_performers)} top-performing campaigns to maximize ROI.",
                'priority': 'Medium'
            })
        
        return recommendations
    
    def get_budget_optimization_suggestions(self, df: pd.DataFrame) -> dict:
        """
        Generate budget reallocation suggestions based on performance.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            dict: Budget optimization strategy
        """
        try:
            kpis = calculate_kpis(df)
            
            # Calculate revenue per campaign
            df_copy = kpis['df'].copy()
            total_budget = df_copy['Revenue'].sum()
            
            # Identify high performers
            high_performers = df_copy[df_copy['Revenue'] > df_copy['Revenue'].quantile(0.75)]
            low_performers = df_copy[df_copy['Revenue'] < df_copy['Revenue'].quantile(0.25)]
            
            budget_strategy = {
                'total_budget': total_budget,
                'reallocation_suggestions': []
            }
            
            # Suggest cutting low performers
            if len(low_performers) > 0:
                cutting_budget = low_performers['Revenue'].sum()
                budget_strategy['reallocation_suggestions'].append({
                    'action': 'Cut underperformers',
                    'campaigns': low_performers['Campaign'].tolist(),
                    'budget_freed': cutting_budget,
                    'budget_percentage': (cutting_budget / total_budget * 100) if total_budget > 0 else 0
                })
            
            # Suggest boosting high performers
            if len(high_performers) > 0:
                boost_budget = high_performers['Revenue'].sum() * 0.2  # Suggest 20% increase
                budget_strategy['reallocation_suggestions'].append({
                    'action': 'Boost top performers',
                    'campaigns': high_performers['Campaign'].tolist(),
                    'suggested_increase': boost_budget,
                    'expected_impact': 'Higher ROI, increased conversions'
                })
            
            return budget_strategy
            
        except Exception as e:
            return {'error': f"Budget optimization failed: {str(e)}"}
    
    def get_targeting_suggestions(self, df: pd.DataFrame) -> list:
        """
        Generate audience targeting suggestions.
        
        Args:
            df (pd.DataFrame): Campaign data
            
        Returns:
            list: Targeting recommendations
        """
        try:
            kpis = calculate_kpis(df)
            suggestions = []
            
            # High CTR campaigns - suggest broader reach
            high_ctr = kpis['df'][kpis['df']['CTR'] > kpis['avg_ctr'] * 1.5]
            if len(high_ctr) > 0:
                suggestions.append({
                    'type': 'Audience Expansion',
                    'campaigns': high_ctr['Campaign'].tolist(),
                    'action': 'These campaigns have high CTR. Consider expanding to similar audiences.'
                })
            
            # Low CTR campaigns - suggest refinement
            low_ctr = kpis['df'][kpis['df']['CTR'] < kpis['avg_ctr'] * 0.5]
            if len(low_ctr) > 0:
                suggestions.append({
                    'type': 'Audience Refinement',
                    'campaigns': low_ctr['Campaign'].tolist(),
                    'action': 'These campaigns have low CTR. Refine targeting to more specific audiences.'
                })
            
            return suggestions
            
        except Exception as e:
            return []
    
    def get_last_recommendations(self) -> dict:
        """Get last generated recommendations."""
        if not self.last_recommendations:
            return {'message': 'No recommendations generated yet'}
        return self.last_recommendations
