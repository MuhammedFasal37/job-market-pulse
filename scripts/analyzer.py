# ================================================
# analyzer.py - SQL analysis of job postings
# ================================================

import pandas as pd
import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import CLEAN_DATA_PATH

# ================================================
# STEP 1 - LOAD DATA INTO SQLITE DATABASE
# ================================================
def load_into_database():
    print("Loading clean data into SQLite database...")
    
    # Read our clean CSV file
    df = pd.read_csv(CLEAN_DATA_PATH)
    
    # Create a database file called jobs.db
    # This is like creating a new Excel workbook
    # If it already exists, it just connects to it
    conn = sqlite3.connect("data/jobs.db")
    
    # Write the dataframe into the database as a table called "jobs"
    # if_exists="replace" means overwrite if table already exists
    df.to_sql("jobs", conn, if_exists="replace", index=False)
    
    print(f"Loaded {len(df)} job postings into database")
    print("Database created: data/jobs.db")
    
    return conn

# ================================================
# STEP 2 - RUN SQL QUERIES
# ================================================
def run_query(conn, query, title):
    print(f"\n{'='*50}")
    print(f"ANALYSIS: {title}")
    print('='*50)
    
    # pd.read_sql runs a SQL query and returns results as a DataFrame
    # This is the magic line - SQL query meets pandas
    result = pd.read_sql(query, conn)
    print(result.to_string(index=False))
    return result

def analyze_jobs(conn):
    
    # ---- QUERY 1: Most in demand skills ----
    # This is more complex - we need to split the skills_found column
    # Because skills are stored as "python, sql, excel" in one cell
    # SQLite doesn't split strings easily so we use pandas for this one
    print(f"\n{'='*50}")
    print("ANALYSIS: Top 10 Most In-Demand Skills")
    print('='*50)
    
    df = pd.read_sql("SELECT skills_found FROM jobs WHERE skills_found != ''", conn)
    
    # Split each row's skills and count them all
    all_skills = []
    for skills in df["skills_found"]:
        if pd.notna(skills) and skills.strip() != "":
            for skill in skills.split(","):
                all_skills.append(skill.strip())
    
    # Count each skill
    skill_counts = pd.Series(all_skills).value_counts().head(10)
    print(skill_counts.to_string())

    # ---- QUERY 2: Jobs by city ----
    run_query(conn, """
        SELECT 
            location,
            COUNT(*) as job_count
        FROM jobs
        WHERE location != 'India'
        GROUP BY location
        ORDER BY job_count DESC
        LIMIT 10
    """, "Top 10 Hiring Cities")

    # ---- QUERY 3: Top hiring companies ----
    run_query(conn, """
        SELECT 
            company,
            COUNT(*) as jobs_posted,
            search_title as role
        FROM jobs
        GROUP BY company
        ORDER BY jobs_posted DESC
        LIMIT 10
    """, "Top 10 Hiring Companies")

    # ---- QUERY 4: Jobs by role ----
    run_query(conn, """
        SELECT 
            search_title as job_role,
            COUNT(*) as total_postings
        FROM jobs
        GROUP BY search_title
        ORDER BY total_postings DESC
    """, "Job Postings by Role")

    # ---- QUERY 5: Average skill count by role ----
    run_query(conn, """
        SELECT 
            search_title as job_role,
            ROUND(AVG(skill_count), 1) as avg_skills_required,
            MAX(skill_count) as max_skills,
            MIN(skill_count) as min_skills
        FROM jobs
        GROUP BY search_title
        ORDER BY avg_skills_required DESC
    """, "Average Skills Required by Role")

    # ---- QUERY 6: Companies hiring in Bangalore ----
    run_query(conn, """
        SELECT 
            company,
            title,
            location
        FROM jobs
        WHERE location LIKE '%Bangalore%'
        ORDER BY company
        LIMIT 10
    """, "Companies Hiring in Bangalore")

    # ---- QUERY 7: Salary disclosure rate ----
    run_query(conn, """
        SELECT 
            has_salary as salary_disclosed,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM jobs), 1) as percentage
        FROM jobs
        GROUP BY has_salary
    """, "Salary Disclosure Rate")

# ================================================
# MAIN FUNCTION
# ================================================
def main():
    print("=" * 50)
    print("JOB MARKET PULSE - SQL ANALYSIS ENGINE")
    print("=" * 50)
    
    # Load data into database
    conn = load_into_database()
    
    # Run all analyses
    analyze_jobs(conn)
    
    # Close database connection
    conn.close()
    
    print(f"\n{'='*50}")
    print("ANALYSIS COMPLETE!")
    print("=" * 50)

if __name__ == "__main__":
    main()