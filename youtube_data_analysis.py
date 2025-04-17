import streamlit as st
import pandas as pd
import plotly.express as px  # New library for interactive visualizations
import seaborn as sns
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="YouTube Data Analysis", layout="wide")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_youtube_data_with_eda.csv')
    df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')
    df['trending_date'] = pd.to_datetime(df['trending_date'], errors='coerce')
    return df

df = load_data()

# Sidebar - Filters
st.sidebar.header("Filter Options")
categories = st.sidebar.multiselect(
    "Select Categories",
    options=df['category_name'].unique(),
    default=df['category_name'].unique()
)

date_range = st.sidebar.date_input(
    "Select Publish Date Range",
    [df['publish_date'].min(), df['publish_date'].max()]
)

metric = st.sidebar.selectbox(
    "Select Metric to Analyze",
    options=['views', 'likes', 'comments', 'likes_per_view', 'comments_per_view'],
    index=0
)

# Apply Filters
filtered_df = df[
    (df['category_name'].isin(categories)) &
    (df['publish_date'] >= pd.Timestamp(date_range[0]).tz_localize('UTC')) &
    (df['publish_date'] <= pd.Timestamp(date_range[1]).tz_localize('UTC'))
]

# Tabs for Visualization
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Time-Series Analysis", "Category Insights", "Custom Metrics"])

# Tab 1: Overview
with tab1:
    st.header("Dataset Overview")
    st.write("Explore key statistics and dataset details.")
    with st.expander("View Dataset"):
        st.dataframe(filtered_df)
    st.write("### Summary Statistics")
    st.write(filtered_df.describe())

# Tab 2: Time-Series Analysis
with tab2:
    st.header("Time-Series Analysis")
    st.write("Analyze trends over time for the selected metric.")
    st.write(f"Currently selected metric: {metric.capitalize()}")
    
    daily_metric = filtered_df.groupby(filtered_df['publish_date'].dt.date)[metric].mean().reset_index()
    
    # Interactive Plotly Chart
    fig = px.line(
        daily_metric,
        x='publish_date',
        y=metric,
        title=f"{metric.capitalize()} Over Time",
        labels={'publish_date': 'Publish Date', metric: metric.capitalize()}
    )
    fig.update_traces(mode="lines+markers")  # Add markers for hover interactivity
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Category Insights
with tab3:
    st.header("Category-Based Insights")
    st.write("Compare engagement metrics across different categories.")
    st.write(f"Currently selected metric: {metric.capitalize()}")
    
    # Interactive Plotly Boxplot
    fig = px.box(
        filtered_df,
        x='category_name',
        y=metric,
        title=f"{metric.capitalize()} by Category",
        labels={'category_name': 'Category', metric: metric.capitalize()}
    )
    fig.update_layout(xaxis_title="Category", yaxis_title=metric.capitalize(), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Custom Metrics
with tab4:
    st.header("Custom Metrics Exploration")
    st.write("Explore engagement metrics like 'Likes per View' or 'Comments per View'.")
    selected_metric = st.radio(
        "Select a Metric",
        ['likes_per_view', 'comments_per_view'],
        index=0
    )
    
    fig = px.histogram(
        filtered_df,
        x=selected_metric,
        nbins=30,
        title=f"Distribution of {selected_metric.replace('_', ' ').capitalize()}",
        labels={selected_metric: selected_metric.replace('_', ' ').capitalize()}
    )
    fig.update_layout(xaxis_title=selected_metric.replace('_', ' ').capitalize(), yaxis_title="Frequency")
    st.plotly_chart(fig, use_container_width=True)

# Sidebar Info Section
with st.sidebar.expander("About the App"):
    st.info("""
    This interactive app enables users to:
    - Filter data by categories and publish date
    - Explore trends in engagement metrics like views, likes, and comments
    - Analyze metrics across categories and over time
    - Visualize custom engagement metrics
    """)

st.success("Enjoy exploring insights from YouTube's trending video data!")
