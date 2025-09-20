import pandas as pd

# Test data loading
print("Testing CORD-19 metadata loading...")
try:
    df = pd.read_csv('asset/metadata.csv')
    print(f"✅ Data loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head(2))
    print(f"\nMissing values:")
    print(df.isnull().sum().head(10))
except Exception as e:
    print(f"❌ Error loading data: {e}")