# CORD-19 Data Analysis Project

## Overview
This project analyzes the CORD-19 dataset containing metadata about COVID-19 research papers. It includes data exploration, visualization, and an interactive Streamlit web application.

## Dataset
- **Source**: CORD-19 Research Challenge Dataset
- **File**: `asset/metadata.csv`
- **Content**: Metadata for COVID-19 research papers including titles, abstracts, publication dates, authors, and journals

## Project Structure
```
Python_Project/
├── asset/
│   └── metadata.csv          # Dataset file
├── cord19_analysis.py        # Main analysis script
├── streamlit_app.py          # Interactive web application
├── cord19_exploration.ipynb  # Jupyter notebook for exploration
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Installation

1. **Clone or download the project**
2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Run the Main Analysis Script
```bash
python cord19_analysis.py
```
This will:
- Load and explore the dataset
- Clean and prepare the data
- Generate visualizations (saved as PNG files)
- Print analysis summary

### 2. Launch the Streamlit Web Application
```bash
streamlit run streamlit_app.py
```
This will open an interactive web interface where you can:
- Filter data by year range
- Explore publications by year
- View top journals
- Analyze title word frequency
- Generate word clouds
- Download filtered data

### 3. Use the Jupyter Notebook
```bash
jupyter notebook cord19_exploration.ipynb
```
For step-by-step interactive analysis and exploration.

## Features

### Data Analysis
- **Basic Exploration**: Dataset dimensions, data types, missing values
- **Data Cleaning**: Handle missing values, date conversion, feature engineering
- **Temporal Analysis**: Publications by year
- **Journal Analysis**: Top publishing journals
- **Text Analysis**: Most frequent words in titles
- **Source Distribution**: Papers by data source

### Visualizations
- Bar charts for publications by year
- Horizontal bar charts for top journals
- Word frequency analysis
- Word clouds from paper titles
- Pie charts for source distribution

### Interactive Features (Streamlit App)
- Year range filtering
- Dynamic chart updates
- Multiple analysis tabs
- Data download functionality
- Responsive design

## Key Insights

The analysis reveals:
1. **Temporal Patterns**: Clear publication trends related to pandemic timeline
2. **Journal Distribution**: Research spread across multiple high-impact journals
3. **Research Themes**: Key topics identified through title analysis
4. **Data Quality**: Comprehensive metadata with varying completeness

## Technical Implementation

### Libraries Used
- **pandas**: Data manipulation and analysis
- **matplotlib/seaborn**: Static visualizations
- **plotly**: Interactive visualizations
- **streamlit**: Web application framework
- **wordcloud**: Text visualization
- **collections**: Data structure utilities

### Code Quality Features
- Modular design with class-based architecture
- Error handling and data validation
- Caching for performance optimization
- Comprehensive documentation
- Clean, readable code structure

## Assignment Requirements Fulfilled

✅ **Part 1**: Data Loading and Basic Exploration  
✅ **Part 2**: Data Cleaning and Preparation  
✅ **Part 3**: Data Analysis and Visualization  
✅ **Part 4**: Streamlit Application  
✅ **Part 5**: Documentation and Reflection  

## Learning Outcomes Achieved

- ✅ Practice loading and exploring real-world datasets
- ✅ Learn basic data cleaning techniques
- ✅ Create meaningful visualizations
- ✅ Build interactive web applications
- ✅ Present data insights effectively

## Future Enhancements

Potential improvements could include:
- Advanced text analysis (sentiment analysis, topic modeling)
- Author network analysis
- Citation analysis
- Machine learning models for paper classification
- Enhanced interactive features

## Challenges and Solutions

### Challenge 1: Large Dataset Size
**Solution**: Implemented data sampling and efficient loading strategies

### Challenge 2: Missing Data
**Solution**: Comprehensive missing value analysis and appropriate handling strategies

### Challenge 3: Text Processing
**Solution**: Used regex and counter utilities for efficient text analysis

### Challenge 4: Interactive Visualization
**Solution**: Combined matplotlib for static plots and plotly for interactive charts

## Reflection

This project provided hands-on experience with:
- Real-world data analysis workflows
- Data cleaning and preparation techniques
- Multiple visualization approaches
- Web application development with Streamlit
- Documentation and project organization

The CORD-19 dataset offered rich opportunities to explore temporal patterns, text analysis, and interactive data presentation, making it an excellent choice for learning fundamental data science skills.

## Contact

For questions or suggestions about this project, please refer to the course materials or reach out to the instructor.