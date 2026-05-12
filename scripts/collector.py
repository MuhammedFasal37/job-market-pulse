# ================================================
# collector.py - Fetches real job postings from Adzuna API
# ================================================

# --- IMPORTS ---
# os lets us read environment variables (our secret keys)
import os

# requests lets Python talk to the internet
import requests

# pandas for organizing data into tables
import pandas as pd

# time lets us pause between API calls so we don't overwhelm the server
import time

# dotenv reads our .env file and loads the secret keys
from dotenv import load_dotenv

# This line actually loads the .env file
# Without this, Python can't see your API keys
load_dotenv()

# --- LOAD OUR OWN CONFIG ---
# We import our settings from config.py
# This is why we made config.py - one place for all settings
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import JOB_TITLES, RESULTS_PER_TITLE, COUNTRY, RAW_DATA_PATH, SKILLS_TO_TRACK

# --- READ SECRET KEYS ---
# os.getenv reads the value from .env file
# It's like opening a safe and taking out the key
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# --- THE SKILL EXTRACTOR FUNCTION ---
# This function reads a job description and finds which skills are mentioned
# Remember functions from yesterday? This is a real one now
def extract_skills(description):
    # Convert description to lowercase so "Python" and "python" both match
    description = description.lower()
    
    # Empty list to store found skills
    found_skills = []
    
    # Loop through every skill we defined in config.py
    for skill in SKILLS_TO_TRACK:
        # Check if this skill appears in the description
        if skill.lower() in description:
            found_skills.append(skill)
    
    # Join the list into a single string separated by commas
    # Example: ["python", "sql"] becomes "python, sql"
    return ", ".join(found_skills)

# --- THE MAIN COLLECTOR FUNCTION ---
def collect_jobs():
    # This list will hold all job postings we collect
    all_jobs = []
    
    print(f"Starting job collection for {len(JOB_TITLES)} job titles...")
    print("=" * 50)
    
    # Loop through each job title in our config
    for job_title in JOB_TITLES:
        print(f"Fetching jobs for: {job_title}")
        
        # Build the API URL
        # This is the address we send our request to
        # Like typing a very specific address into your browser
        url = (
            f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
            f"?app_id={APP_ID}"
            f"&app_key={APP_KEY}"
            f"&results_per_page={RESULTS_PER_TITLE}"
            f"&what={job_title.replace(' ', '%20')}"
            f"&content-type=application/json"
        )
        
        # Send the request to Adzuna
        # This is like making the phone call
        response = requests.get(url)
        
        # Check if the call was successful
        # 200 means success in internet language
        if response.status_code == 200:
            # Convert the response into Python data
            data = response.json()
            
            # The actual jobs are inside data["results"]
            jobs = data.get("results", [])
            
            print(f"  Found {len(jobs)} jobs")
            
            # Loop through each job and extract what we need
            for job in jobs:
                job_record = {
                    "title": job.get("title", "N/A"),
                    "company": job.get("company", {}).get("display_name", "N/A"),
                    "location": job.get("location", {}).get("display_name", "N/A"),
                    "salary_min": job.get("salary_min", 0),
                    "salary_max": job.get("salary_max", 0),
                    "description": job.get("description", ""),
                    "created": job.get("created", "N/A"),
                    "search_title": job_title,
                    "skills_found": extract_skills(job.get("description", ""))
                }
                all_jobs.append(job_record)
        
        else:
            print(f"  Error fetching {job_title}: Status {response.status_code}")
        
        # Wait 1 second between requests
        # This is polite - don't hammer the server with requests
        time.sleep(1)
    
    # --- SAVE TO CSV ---
    if all_jobs:
        df = pd.DataFrame(all_jobs)
        df.to_csv(RAW_DATA_PATH, index=False)
        print("=" * 50)
        print(f"Done! Collected {len(all_jobs)} job postings")
        print(f"Saved to: {RAW_DATA_PATH}")
        print(df.head())
    else:
        print("No jobs collected. Check your API keys.")

# --- RUN THE COLLECTOR ---
# This line means: only run collect_jobs() if we run THIS file directly
# If another file imports this file, it won't auto-run
if __name__ == "__main__":
    collect_jobs()