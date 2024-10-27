# modules/chart_generator.py

import pandas as pd
import plotly.express as px
import streamlit as st

def create_premium_chart(chart_data):
    """
    Creates a bar chart for Monthly Premiums.
    
    Args:
        chart_data (dict or list): Data for charting.
    
    Returns:
        Plotly Figure: The generated chart.
    """
    # Convert JSON data to DataFrame
    if isinstance(chart_data, dict) and "policies" in chart_data:
        df = pd.DataFrame(chart_data['policies'])
    elif isinstance(chart_data, list):
        df = pd.DataFrame(chart_data)
    else:
        st.error("Unsupported chart data format.")
        return None
    
    # Check for required columns
    required_columns = ["Provider", "Monthly Premium", "Coverage Limit", "Deductibles"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"Chart data is missing required fields: {required_columns}")
        return None
    
    # Debugging: Display the DataFrame
    st.write("Chart Data DataFrame for Monthly Premium:", df)
    
    # Create the bar chart
    fig = px.bar(
        df,
        x='Provider',
        y='Monthly Premium',
        labels={'Provider': 'Provider', 'Monthly Premium': 'Monthly Premium ($)'},
        title='Comparison of Monthly Premiums Across Providers',
        color='Provider',
        text='Monthly Premium',
        height=500
    )
    
    # Format the text on bars
    fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
    
    # Adjust layout for better appearance
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    return fig

def create_coverage_limit_chart(chart_data):
    """
    Creates a bar chart for Coverage Limits.
    
    Args:
        chart_data (dict or list): Data for charting.
    
    Returns:
        Plotly Figure: The generated chart.
    """
    # Convert JSON data to DataFrame
    if isinstance(chart_data, dict) and "policies" in chart_data:
        df = pd.DataFrame(chart_data['policies'])
    elif isinstance(chart_data, list):
        df = pd.DataFrame(chart_data)
    else:
        st.error("Unsupported chart data format.")
        return None
    
    # Check for required columns
    required_columns = ["Provider", "Coverage Limit"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"Chart data is missing required fields: {required_columns}")
        return None
    
    # Debugging: Display the DataFrame
    st.write("Chart Data DataFrame for Coverage Limit:", df)
    
    # Create the bar chart
    fig = px.bar(
        df,
        x='Provider',
        y='Coverage Limit',
        labels={'Provider': 'Provider', 'Coverage Limit': 'Coverage Limit ($)'},
        title='Comparison of Coverage Limits Across Providers',
        color='Provider',
        text='Coverage Limit',
        height=500
    )
    
    # Format the text on bars
    fig.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
    
    # Adjust layout for better appearance
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    return fig

def create_deductibles_chart(chart_data):
    """
    Creates a bar chart for Deductibles.
    
    Args:
        chart_data (dict or list): Data for charting.
    
    Returns:
        Plotly Figure: The generated chart.
    """
    # Convert JSON data to DataFrame
    if isinstance(chart_data, dict) and "policies" in chart_data:
        df = pd.DataFrame(chart_data['policies'])
    elif isinstance(chart_data, list):
        df = pd.DataFrame(chart_data)
    else:
        st.error("Unsupported chart data format.")
        return None
    
    # Check for required columns
    required_columns = ["Provider", "Deductibles"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"Chart data is missing required fields: {required_columns}")
        return None
    
    # Debugging: Display the DataFrame
    st.write("Chart Data DataFrame for Deductibles:", df)
    
    # Create the bar chart
    fig = px.bar(
        df,
        x='Provider',
        y='Deductibles',
        labels={'Provider': 'Provider', 'Deductibles': 'Deductibles ($)'},
        title='Comparison of Deductibles Across Providers',
        color='Provider',
        text='Deductibles',
        height=500
    )
    
    # Format the text on bars
    fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
    
    # Adjust layout for better appearance
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    return fig
