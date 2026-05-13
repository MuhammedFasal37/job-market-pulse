

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Click%20Here-brightgreen)](https://job-market-pulse-htedv5mwgmk6pbhp8mtz4m.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)](https://streamlit.io)
[![Auto Updated](https://img.shields.io/badge/Data-Auto%20Updated%20Daily-orange)]()

> *"I spent 6 months job hunting without success — so I built a system to analyze exactly what Indian employers want."*

---

## 🔗 [Click here to view the live dashboard](https://job-market-pulse-htedv5mwgmk6pbhp8mtz4m.streamlit.app)

---

## 📌 What is this project?

Job Market Pulse is an end-to-end automated data analytics pipeline that:

- **Collects** 185+ real Indian job postings daily from the Adzuna API
- **Cleans** the data automatically — removing duplicates, extracting skills, normalizing salaries
- **Analyzes** the data using advanced SQL queries to surface real market insights
- **Generates** an AI-powered market briefing using Groq LLaMA 3
- **Displays** everything on a live interactive dashboard built with Streamlit and Plotly
- **Updates automatically** every day at 7:30 AM IST via GitHub Actions — zero manual work

---

## 🔍 Key Insights Discovered

From analyzing 185+ real Indian job postings (May 2026):

| Insight | Finding |
|--------|---------|
| 🥇 Most in-demand skill | **SQL** (34 job postings) |
| 🥈 Second most demanded | **Power BI** (24 job postings) |
| 🥉 Third most demanded | **Python** (23 job postings) |
| 🏙️ Top hiring city | **Bangalore** (42 openings) |
| 🏢 Top recruiter | **TCS** (9 postings) |
| 💰 Salary transparency | Only **2.2%** of companies disclose salary |

---

## 🏗️ Project Architecture
Adzuna API → collector.py → raw_jobs.csv
↓
cleaner.py → clean_jobs.csv
↓
analyzer.py → jobs.db (SQLite)
↓
ai_insights.py → market_briefing.txt (Groq LLaMA 3)
↓
dashboard.py → Live Streamlit Dashboard
↓
GitHub Actions → Auto-updates every day at 7:30 AM IST

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core programming language |
| **pandas** | Data cleaning and manipulation |
| **SQLite + SQL** | Database and analytics queries |
| **Adzuna API** | Real job postings data source |
| **Groq LLaMA 3** | AI-generated market briefings |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Interactive data visualizations |
| **GitHub Actions** | Automated daily data pipeline |
| **Git & GitHub** | Version control and deployment |

---

## 📁 Project Structure
job-market-pulse/
├── scripts/
│   ├── config.py          # Project settings and configuration
│   ├── collector.py       # Fetches job data from Adzuna API
│   ├── cleaner.py         # Cleans and processes raw data
│   ├── analyzer.py        # SQL analysis and insights
│   ├── ai_insights.py     # AI briefing generation (Groq)
│   └── dashboard.py       # Streamlit interactive dashboard
├── data/
│   ├── raw_jobs.csv       # Raw collected job postings
│   ├── clean_jobs.csv     # Cleaned and processed data
│   └── jobs.db            # SQLite database
├── output/
│   └── market_briefing.txt # AI generated market briefing
├── .github/
│   └── workflows/
│       └── update_data.yml # GitHub Actions automation
├── requirements.txt        # Python dependencies
└── README.md              # You are here

---

## 🚀 How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/MuhammedFasal37/job-market-pulse.git
cd job-market-pulse
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
GROQ_API_KEY=your_groq_key

4. Run the pipeline
```bash
python scripts/collector.py
python scripts/cleaner.py
python scripts/analyzer.py
python scripts/ai_insights.py
```

5. Launch the dashboard
```bash
python -m streamlit run scripts/dashboard.py
```

---

## 👨‍💻 About the Developer

Built by **Muhammed Fasal** as a portfolio project to demonstrate end-to-end data analytics skills.

- 🔗 [Live Dashboard](https://job-market-pulse-htedv5mwgmk6pbhp8mtz4m.streamlit.app)
- 💼 [GitHub Profile](https://github.com/MuhammedFasal37)

---

*Data updates automatically every day via GitHub Actions. Last pipeline run visible in the Actions tab.*
