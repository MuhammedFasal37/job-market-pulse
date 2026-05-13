# ================================================
# Job Market Pulse - Project Configuration
# ================================================
# This file is the control panel for our project.
# Change settings here and they apply everywhere.

# --- SEARCH SETTINGS ---
# What job titles do we want to analyze?
JOB_TITLES = [
    "Data Analyst",
    "Business Analyst", 
    "Data Scientist",
    "BI Analyst"
]

# How many job postings to collect per title
RESULTS_PER_TITLE = 50

# Which country to search in
# Options: "us" for USA, "gb" for UK, "in" for India
COUNTRY = "in"

# --- FILE PATHS ---
# Where we save the raw collected data
RAW_DATA_PATH = "data/raw_jobs.csv"

# Where we save the cleaned data
CLEAN_DATA_PATH = "data/clean_jobs.csv"

# --- SKILLS TO TRACK ---
# These are the skills we'll look for inside job descriptions
SKILLS_TO_TRACK = [
    "python", "sql", "excel", "tableau", "power bi",
    "r programming", "machine learning", "statistics", "pandas",
    "numpy", "matplotlib", "spark", "aws", "azure",
    "communication", "problem solving", "data visualization"
]

# --- PROJECT INFO ---
PROJECT_NAME = "Job Market Pulse"
VERSION = "1.0"