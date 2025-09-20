import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

class CORD19Analyzer:
    def __init__(self, data_path):
        """Initialize the analyzer with data path"""
        self.data_path = data_path
        self.df = None
        self.cleaned_df = None
    
    def load_data(self):
        """Load the metadata.csv file"""
        print("Loading CORD-19 metadata...")
        self.df = pd.read_csv(self.data_path)
        print(f"Data loaded successfully! Shape: {self.df.shape}")
        return self.df
    
    def basic_exploration(self):
        """Perform basic data exploration"""
        print("\n=== BASIC DATA EXPLORATION ===")
        print(f"Dataset dimensions: {self.df.shape}")
        print(f"\nColumn names: {list(self.df.columns)}")
        print(f"\nData types:\n{self.df.dtypes}")
        print(f"\nFirst 5 rows:\n{self.df.head()}")
        print(f"\nMissing values:\n{self.df.isnull().sum()}")
        print(f"\nBasic statistics:\n{self.df.describe()}")
    
    def clean_data(self):
        """Clean and prepare the data"""
        print("\n=== DATA CLEANING ===")
        self.cleaned_df = self.df.copy()
        
        # Handle missing values
        print("Handling missing values...")
        
        # Convert publish_time to datetime
        if 'publish_time' in self.cleaned_df.columns:
            self.cleaned_df['publish_time'] = pd.to_datetime(self.cleaned_df['publish_time'], errors='coerce')
            self.cleaned_df['year'] = self.cleaned_df['publish_time'].dt.year
        
        # Create abstract word count
        if 'abstract' in self.cleaned_df.columns:
            self.cleaned_df['abstract_word_count'] = self.cleaned_df['abstract'].fillna('').str.split().str.len()
        
        # Remove rows with missing titles
        if 'title' in self.cleaned_df.columns:
            self.cleaned_df = self.cleaned_df.dropna(subset=['title'])
        
        print(f"Cleaned data shape: {self.cleaned_df.shape}")
        return self.cleaned_df
    
    def analyze_publications_by_year(self):
        """Analyze publications by year"""
        if 'year' not in self.cleaned_df.columns:
            return None
        
        year_counts = self.cleaned_df['year'].value_counts().sort_index()
        
        plt.figure(figsize=(10, 6))
        plt.bar(year_counts.index, year_counts.values)
        plt.title('COVID-19 Research Publications by Year')
        plt.xlabel('Year')
        plt.ylabel('Number of Publications')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('publications_by_year.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return year_counts
    
    def analyze_top_journals(self, top_n=10):
        """Analyze top journals"""
        if 'journal' not in self.cleaned_df.columns:
            return None
        
        journal_counts = self.cleaned_df['journal'].value_counts().head(top_n)
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(journal_counts)), journal_counts.values)
        plt.yticks(range(len(journal_counts)), journal_counts.index)
        plt.title(f'Top {top_n} Journals Publishing COVID-19 Research')
        plt.xlabel('Number of Publications')
        plt.tight_layout()
        plt.savefig('top_journals.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return journal_counts
    
    def analyze_title_words(self, top_n=20):
        """Analyze most frequent words in titles"""
        if 'title' not in self.cleaned_df.columns:
            return None
        
        # Extract words from titles
        all_titles = ' '.join(self.cleaned_df['title'].fillna('').astype(str))
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_titles.lower())
        
        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'they', 'been', 'have', 'were', 'said', 'each', 'which', 'their', 'time', 'will', 'about', 'can', 'when', 'make', 'like', 'into', 'him', 'has', 'two', 'more', 'her', 'would', 'there', 'could', 'way', 'been', 'who', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part'}
        filtered_words = [word for word in words if word not in stop_words]
        
        word_freq = Counter(filtered_words).most_common(top_n)
        
        # Create bar chart
        words, counts = zip(*word_freq)
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(words)), counts)
        plt.yticks(range(len(words)), words)
        plt.title(f'Top {top_n} Most Frequent Words in Titles')
        plt.xlabel('Frequency')
        plt.tight_layout()
        plt.savefig('title_words.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return word_freq
    
    def create_wordcloud(self):
        """Create word cloud from titles"""
        if 'title' not in self.cleaned_df.columns:
            return None
        
        all_titles = ' '.join(self.cleaned_df['title'].fillna('').astype(str))
        
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Paper Titles')
        plt.tight_layout()
        plt.savefig('wordcloud.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def analyze_sources(self, top_n=10):
        """Analyze distribution by source"""
        if 'source_x' not in self.cleaned_df.columns:
            return None
        
        source_counts = self.cleaned_df['source_x'].value_counts().head(top_n)
        
        plt.figure(figsize=(10, 8))
        plt.pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%')
        plt.title(f'Distribution of Papers by Source (Top {top_n})')
        plt.tight_layout()
        plt.savefig('sources_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return source_counts
    
    def generate_report(self):
        """Generate a summary report"""
        print("\n=== ANALYSIS REPORT ===")
        print(f"Total papers analyzed: {len(self.cleaned_df)}")
        
        if 'year' in self.cleaned_df.columns:
            year_range = f"{self.cleaned_df['year'].min():.0f} - {self.cleaned_df['year'].max():.0f}"
            print(f"Publication years: {year_range}")
        
        if 'journal' in self.cleaned_df.columns:
            unique_journals = self.cleaned_df['journal'].nunique()
            print(f"Unique journals: {unique_journals}")
        
        if 'abstract_word_count' in self.cleaned_df.columns:
            avg_abstract_length = self.cleaned_df['abstract_word_count'].mean()
            print(f"Average abstract length: {avg_abstract_length:.1f} words")

def main():
    # Initialize analyzer
    analyzer = CORD19Analyzer('asset/metadata.csv')
    
    # Load and explore data
    analyzer.load_data()
    analyzer.basic_exploration()
    
    # Clean data
    analyzer.clean_data()
    
    # Perform analysis
    print("\nGenerating visualizations...")
    analyzer.analyze_publications_by_year()
    analyzer.analyze_top_journals()
    analyzer.analyze_title_words()
    analyzer.create_wordcloud()
    analyzer.analyze_sources()
    
    # Generate report
    analyzer.generate_report()
    
    print("\nAnalysis complete! Check the generated PNG files for visualizations.")

if __name__ == "__main__":
    main()