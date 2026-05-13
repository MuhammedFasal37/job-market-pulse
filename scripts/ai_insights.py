# ================================================
# ai_insights.py - Generates AI market briefing
# using Groq API (free)
# ================================================

import pandas as pd
import sqlite3
import os
import sys
from groq import Groq
from dotenv import load_dotenv

# Load our secret keys from .env file
load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import CLEAN_DATA_PATH

# ================================================
# STEP 1 - GATHER DATA SUMMARY FROM DATABASE
# ================================================
def get_data_summary():
    print("Gathering data summary from database...")

    conn = sqlite3.connect("data/jobs.db")

    # Get top skills
    df_skills = pd.read_sql(
        "SELECT skills_found FROM jobs WHERE skills_found != ''", conn
    )
    all_skills = []
    for skills in df_skills["skills_found"]:
        if pd.notna(skills) and skills.strip() != "":
            for skill in skills.split(","):
                all_skills.append(skill.strip())
    top_skills = pd.Series(all_skills).value_counts().head(5)

    # Get top cities
    top_cities = pd.read_sql("""
        SELECT location, COUNT(*) as count
        FROM jobs
        WHERE location != 'India'
        GROUP BY location
        ORDER BY count DESC
        LIMIT 5
    """, conn)

    # Get top companies
    top_companies = pd.read_sql("""
        SELECT company, COUNT(*) as count
        FROM jobs
        GROUP BY company
        ORDER BY count DESC
        LIMIT 5
    """, conn)

    # Get role distribution
    roles = pd.read_sql("""
        SELECT search_title, COUNT(*) as count
        FROM jobs
        GROUP BY search_title
        ORDER BY count DESC
    """, conn)

    # Get salary disclosure rate
    salary = pd.read_sql("""
        SELECT 
            ROUND(COUNT(CASE WHEN has_salary = 1 THEN 1 END) * 100.0 / COUNT(*), 1) 
            as disclosure_rate
        FROM jobs
    """, conn)

    conn.close()

    # Build summary string to send to AI
    summary = f"""
JOB MARKET DATA SUMMARY - INDIA (May 2026)
Total job postings analyzed: 185

TOP 5 IN-DEMAND SKILLS:
{top_skills.to_string()}

TOP 5 HIRING CITIES:
{top_cities.to_string(index=False)}

TOP 5 HIRING COMPANIES:
{top_companies.to_string(index=False)}

ROLE DISTRIBUTION:
{roles.to_string(index=False)}

SALARY DISCLOSURE RATE: {salary['disclosure_rate'].values[0]}%
    """

    print("Data summary ready!")
    return summary

# ================================================
# STEP 2 - SEND TO GROQ AND GET INSIGHTS
# ================================================
def generate_ai_insights(data_summary):
    print("\nSending data to Groq AI...")
    print("Generating market briefing...")

    # Initialize Groq client
    # It automatically reads GROQ_API_KEY from .env
    client = Groq()

    # The prompt we send to the AI
    prompt = f"""
You are a senior data analyst specializing in the Indian job market.
Below is real job market data collected from Indian job postings in May 2026.

{data_summary}

Please write a professional and insightful market briefing based on this data.
Structure it as follows:

1. MARKET OVERVIEW (2-3 sentences summarizing the overall picture)
2. SKILLS IN DEMAND (what skills employers want most and why this matters)
3. HIRING HOTSPOTS (which cities are leading and what this means)
4. TOP RECRUITERS (notable companies and their hiring patterns)
5. SALARY TRANSPARENCY (insights about salary disclosure and what candidates should know)
6. RECOMMENDATIONS (3 specific actionable tips for job seekers based on this data)

Write in a professional but easy to understand tone.
Be specific with numbers from the data.
This briefing will be displayed on a live analytics dashboard.
    """

    # Call Groq API
    # chat.completions.create sends our prompt and gets a response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1000
    )

    # Extract the text from the response
    briefing = response.choices[0].message.content
    return briefing

# ================================================
# STEP 3 - SAVE THE BRIEFING
# ================================================
def save_briefing(briefing):
    with open("output/market_briefing.txt", "w", encoding="utf-8") as f:
        f.write("JOB MARKET PULSE - AI GENERATED BRIEFING\n")
        f.write("=" * 50 + "\n\n")
        f.write(briefing)

    print("\nBriefing saved to: output/market_briefing.txt")

# ================================================
# MAIN FUNCTION
# ================================================
def main():
    print("=" * 50)
    print("JOB MARKET PULSE - AI INSIGHT GENERATOR")
    print("=" * 50)

    # Get data summary
    data_summary = get_data_summary()

    # Generate AI insights
    briefing = generate_ai_insights(data_summary)

    if briefing:
        print("\n" + "=" * 50)
        print("AI GENERATED MARKET BRIEFING")
        print("=" * 50)
        print(briefing)
        save_briefing(briefing)
        print("\n" + "=" * 50)
        print("AI INSIGHTS COMPLETE!")
        print("=" * 50)
    else:
        print("Failed to generate briefing. Check your API key.")

if __name__ == "__main__":
    main()