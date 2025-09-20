import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🦠",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load and cache the data"""
    try:
        df = pd.read_csv('asset/metadata.csv')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def clean_data(df):
    """Clean and prepare the data"""
    cleaned_df = df.copy()
    
    # Convert publish_time to datetime
    if 'publish_time' in cleaned_df.columns:
        cleaned_df['publish_time'] = pd.to_datetime(cleaned_df['publish_time'], errors='coerce')
        cleaned_df['year'] = cleaned_df['publish_time'].dt.year
    
    # Create abstract word count
    if 'abstract' in cleaned_df.columns:
        cleaned_df['abstract_word_count'] = cleaned_df['abstract'].fillna('').str.split().str.len()
    
    # Remove rows with missing titles
    if 'title' in cleaned_df.columns:
        cleaned_df = cleaned_df.dropna(subset=['title'])
    
    return cleaned_df

def main():
    st.title("🦠 CORD-19 Data Explorer")
    st.write("Interactive exploration of COVID-19 research papers")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    if df is None:
        st.stop()
    
    # Clean data
    cleaned_df = clean_data(df)
    
    # Sidebar
    st.sidebar.header("Filters")
    
    # Year filter
    if 'year' in cleaned_df.columns:
        min_year = int(cleaned_df['year'].min())
        max_year = int(cleaned_df['year'].max())
        year_range = st.sidebar.slider(
            "Select year range",
            min_year, max_year,
            (min_year, max_year)
        )
        
        # Filter data by year
        filtered_df = cleaned_df[
            (cleaned_df['year'] >= year_range[0]) & 
            (cleaned_df['year'] <= year_range[1])
        ]
    else:
        filtered_df = cleaned_df
    
    # Main content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Papers", len(filtered_df))
    
    with col2:
        if 'journal' in filtered_df.columns:
            st.metric("Unique Journals", filtered_df['journal'].nunique())
    
    with col3:
        if 'abstract_word_count' in filtered_df.columns:
            avg_length = filtered_df['abstract_word_count'].mean()
            st.metric("Avg Abstract Length", f"{avg_length:.0f} words")
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Publications by Year", 
        "📰 Top Journals", 
        "🔤 Title Analysis", 
        "☁️ Word Cloud", 
        "📋 Data Sample"
    ])
    
    with tab1:
        st.subheader("Publications by Year")
        if 'year' in filtered_df.columns:
            year_counts = filtered_df['year'].value_counts().sort_index()
            
            fig = px.bar(
                x=year_counts.index, 
                y=year_counts.values,
                labels={'x': 'Year', 'y': 'Number of Publications'},
                title='COVID-19 Research Publications Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show statistics
            st.write(f"**Peak year:** {year_counts.idxmax()} ({year_counts.max()} papers)")
            st.write(f"**Total papers in selected range:** {year_counts.sum()}")
    
    with tab2:
        st.subheader("Top Journals")
        if 'journal' in filtered_df.columns:
            top_n = st.selectbox("Number of top journals to show", [5, 10, 15, 20], index=1)
            
            journal_counts = filtered_df['journal'].value_counts().head(top_n)
            
            fig = px.bar(
                x=journal_counts.values,
                y=journal_counts.index,
                orientation='h',
                labels={'x': 'Number of Publications', 'y': 'Journal'},
                title=f'Top {top_n} Journals Publishing COVID-19 Research'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Title Word Analysis")
        if 'title' in filtered_df.columns:
            top_n_words = st.selectbox("Number of top words to show", [10, 15, 20, 25], index=1)
            
            # Extract words from titles
            all_titles = ' '.join(filtered_df['title'].fillna('').astype(str))
            words = re.findall(r'\b[a-zA-Z]{3,}\b', all_titles.lower())
            
            # Remove common stop words
            stop_words = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'they', 'been', 'have', 'were', 'said', 'each', 'which', 'their', 'time', 'will', 'about', 'can', 'when', 'make', 'like', 'into', 'him', 'has', 'two', 'more', 'her', 'would', 'there', 'could', 'way', 'been', 'who', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part'}
            filtered_words = [word for word in words if word not in stop_words]
            
            word_freq = Counter(filtered_words).most_common(top_n_words)
            
            if word_freq:
                words_list, counts_list = zip(*word_freq)
                
                fig = px.bar(
                    x=counts_list,
                    y=words_list,
                    orientation='h',
                    labels={'x': 'Frequency', 'y': 'Words'},
                    title=f'Top {top_n_words} Most Frequent Words in Titles'
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Word Cloud")
        if 'title' in filtered_df.columns:
            all_titles = ' '.join(filtered_df['title'].fillna('').astype(str))
            
            if all_titles.strip():
                wordcloud = WordCloud(
                    width=800, 
                    height=400, 
                    background_color='white'
                ).generate(all_titles)
                
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.write("No title data available for word cloud generation.")
    
    with tab5:
        st.subheader("Data Sample")
        st.write("Sample of the filtered dataset:")
        
        # Show column selection
        if not filtered_df.empty:
            available_cols = filtered_df.columns.tolist()
            selected_cols = st.multiselect(
                "Select columns to display",
                available_cols,
                default=available_cols[:5] if len(available_cols) >= 5 else available_cols
            )
            
            if selected_cols:
                sample_size = st.slider("Number of rows to display", 5, 50, 10)
                st.dataframe(filtered_df[selected_cols].head(sample_size))
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download filtered data as CSV",
                data=csv,
                file_name=f"cord19_filtered_{year_range[0]}_{year_range[1]}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()