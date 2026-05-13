# ================================================
# cleaner.py - Cleans raw job posting data
# ================================================

import pandas as pd
import os
import sys

# This adds the root folder to Python's path
# So we can import config.py from anywhere
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import RAW_DATA_PATH, CLEAN_DATA_PATH

# ================================================
# STEP 1 - LOAD THE RAW DATA
# ================================================
def load_data():
    print("Loading raw data...")
    
    # Read the CSV file we collected
    df = pd.read_csv(RAW_DATA_PATH)
    
    print(f"Loaded {len(df)} job postings")
    print(f"Columns: {list(df.columns)}")
    
    return df

# ================================================
# STEP 2 - REMOVE DUPLICATES
# ================================================
def remove_duplicates(df):
    print("\nRemoving duplicates...")
    
    # Count before
    before = len(df)
    
    # Drop rows where title AND company are exactly the same
    # Keep the first occurrence, remove the rest
    df = df.drop_duplicates(subset=["title", "company"])
    
    # Count after
    after = len(df)
    
    print(f"Removed {before - after} duplicates")
    print(f"Remaining: {after} job postings")
    
    return df

# ================================================
# STEP 3 - CLEAN JOB TITLES
# ================================================
def clean_titles(df):
    print("\nCleaning job titles...")
    
    # strip() removes extra spaces from start and end
    # Example: "  Data Analyst  " becomes "Data Analyst"
    df["title"] = df["title"].str.strip()
    
    # Convert to title case - first letter of each word is capital
    # Example: "data analyst" becomes "Data Analyst"
    df["title"] = df["title"].str.title()
    
    print("Titles cleaned!")
    
    return df

# ================================================
# STEP 4 - HANDLE MISSING SALARIES
# ================================================
def clean_salaries(df):
    print("\nCleaning salary data...")
    
    # Count how many jobs have no salary (0 means not provided)
    missing = len(df[df["salary_min"] == 0])
    print(f"Jobs with no salary info: {missing}")
    
    # Replace 0 with None (which becomes empty in CSV)
    # This is more honest than showing 0
    df["salary_min"] = df["salary_min"].replace(0, None)
    df["salary_max"] = df["salary_max"].replace(0, None)
    
    # Create a new column showing salary range as text
    # This is more readable for our dashboard later
    def salary_range(row):
        if pd.isna(row["salary_min"]):
            return "Not disclosed"
        else:
            return f"{row['salary_min']:,.0f} - {row['salary_max']:,.0f}"
    
    df["salary_range"] = df.apply(salary_range, axis=1)
    
    print("Salary data cleaned!")
    
    return df

# ================================================
# STEP 5 - CLEAN DESCRIPTIONS
# ================================================
def clean_descriptions(df):
    print("\nCleaning descriptions...")
    
    # Remove extra whitespace from descriptions
    df["description"] = df["description"].str.strip()
    
    # Replace multiple spaces with single space
    df["description"] = df["description"].str.replace(r'\s+', ' ', regex=True)
    
    # Limit description to first 500 characters
    # We don't need the full description for analysis
    df["description"] = df["description"].str[:500]
    
    print("Descriptions cleaned!")
    
    return df

# ================================================
# STEP 6 - CLEAN LOCATIONS
# ================================================
def clean_locations(df):
    print("\nCleaning locations...")
    
    # Strip extra spaces
    df["location"] = df["location"].str.strip()
    
    # Count unique locations
    print(f"Unique locations found: {df['location'].nunique()}")
    print("Top 5 locations:")
    print(df["location"].value_counts().head())
    
    return df

# ================================================
# STEP 7 - ADD USEFUL COLUMNS
# ================================================
def add_columns(df):
    print("\nAdding useful columns...")
    
    # Count how many skills each job requires
    # Split the skills_found string by comma and count items
    df["skill_count"] = df["skills_found"].apply(
        lambda x: len(str(x).split(",")) if pd.notna(x) and x != "" else 0
    )
    
    # Flag jobs that have salary info
    df["has_salary"] = df["salary_range"] != "Not disclosed"
    
    print("Columns added!")
    
    return df

# ================================================
# MAIN FUNCTION - RUNS ALL STEPS IN ORDER
# ================================================
def clean_data():
    print("=" * 50)
    print("STARTING DATA CLEANING")
    print("=" * 50)
    
    # Run each step in order
    # Output of each step feeds into the next
    df = load_data()
    df = remove_duplicates(df)
    df = clean_titles(df)
    df = clean_salaries(df)
    df = clean_descriptions(df)
    df = clean_locations(df)
    df = add_columns(df)
    
    # Save the clean data
    df.to_csv(CLEAN_DATA_PATH, index=False)
    
    print("\n" + "=" * 50)
    print(f"CLEANING COMPLETE!")
    print(f"Clean data saved to: {CLEAN_DATA_PATH}")
    print(f"Final dataset: {len(df)} job postings")
    print(f"Columns: {list(df.columns)}")
    print("=" * 50)

# Run it
if __name__ == "__main__":
    clean_data()