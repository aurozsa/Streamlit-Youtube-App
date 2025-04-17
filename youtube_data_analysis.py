import streamlit as st
import pandas as pd
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
    (df['publish_date'] >= pd.Timestamp(date_range[0])) &
    (df['publish_date'] <= pd.Timestamp(date_range[1]))
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
    daily_metric = filtered_df.groupby(filtered_df['publish_date'].dt.date)[metric].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(daily_metric['publish_date'], daily_metric[metric], marker='o', linestyle='-', label=metric)
    ax.set_title(f"{metric.capitalize()} Over Time")
    ax.set_xlabel("Publish Date")
    ax.set_ylabel(metric.capitalize())
    ax.legend()
    st.pyplot(fig)

# Tab 3: Category Insights
with tab3:
    st.header("Category-Based Insights")
    st.write("Compare engagement metrics across different categories.")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.boxplot(x='category_name', y=metric, data=filtered_df, ax=ax)
    ax.set_title(f"{metric.capitalize()} by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel(metric.capitalize())
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Tab 4: Custom Metrics
with tab4:
    st.header("Custom Metrics Exploration")
    st.write("Explore engagement metrics like 'Likes per View' or 'Comments per View'.")
    selected_metric = st.radio(
        "Select a Metric",
        ['likes_per_view', 'comments_per_view']
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_df[selected_metric], bins=30, kde=True, ax=ax)
    ax.set_title(f"Distribution of {selected_metric.replace('_', ' ').capitalize()}")
    ax.set_xlabel(selected_metric.replace('_', ' ').capitalize())
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

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
