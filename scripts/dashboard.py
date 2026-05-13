# ================================================
# dashboard.py - Interactive web dashboard
# ================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import CLEAN_DATA_PATH

# ================================================
# PAGE CONFIGURATION
# This must be the first streamlit command
# ================================================
st.set_page_config(
    page_title="Job Market Pulse",
    page_icon="📊",
    layout="wide"
)

# ================================================
# LOAD DATA
# ================================================
@st.cache_data
def load_data():
    conn = sqlite3.connect("data/jobs.db")
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df

@st.cache_data
def load_briefing():
    briefing_path = "output/market_briefing.txt"
    if os.path.exists(briefing_path):
        with open(briefing_path, "r", encoding="utf-8") as f:
            return f.read()
    return "No briefing generated yet. Run ai_insights.py first."

# ================================================
# SKILL COUNTER HELPER
# ================================================
def count_skills(df):
    all_skills = []
    for skills in df["skills_found"]:
        if pd.notna(skills) and str(skills).strip() != "":
            for skill in str(skills).split(","):
                all_skills.append(skill.strip())
    return pd.Series(all_skills).value_counts().reset_index()

# ================================================
# MAIN DASHBOARD
# ================================================
def main():
    # --- HEADER ---
    st.title("📊 Job Market Pulse")
    st.subheader("AI-Powered Indian Job Market Analytics Dashboard")
    st.markdown("*Real-time insights from 185+ job postings across India*")
    st.divider()

    # Load data
    df = load_data()

    # --- METRIC CARDS ---
    # These are the 4 big numbers at the top
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Jobs Analyzed",
            value=len(df),
            delta="Live data"
        )

    with col2:
        # Find top skill
        skill_counts = count_skills(df)
        top_skill = skill_counts.iloc[0]["index"] if len(skill_counts) > 0 else "N/A"
        st.metric(
            label="Most In-Demand Skill",
            value=top_skill.upper(),
            delta="Across all roles"
        )

    with col3:
        # Find top city
        top_city = df[df["location"] != "India"]["location"].value_counts().index[0]
        top_city_short = top_city.split(",")[0]
        st.metric(
            label="Top Hiring City",
            value=top_city_short,
            delta="Most job postings"
        )

    with col4:
        salary_rate = round(df["has_salary"].mean() * 100, 1)
        st.metric(
            label="Salary Disclosed",
            value=f"{salary_rate}%",
            delta="Of all postings"
        )

    st.divider()

    # --- TWO COLUMN LAYOUT FOR CHARTS ---
    left, right = st.columns(2)

    with left:
        # SKILLS BAR CHART
        st.subheader("🔧 Top 10 In-Demand Skills")
        skill_df = count_skills(df).head(10)
        skill_df.columns = ["skill", "count"]

        fig_skills = px.bar(
            skill_df,
            x="count",
            y="skill",
            orientation="h",
            color="count",
            color_continuous_scale="blues",
            labels={"count": "Job Postings", "skill": "Skill"}
        )
        fig_skills.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"}
        )
        st.plotly_chart(fig_skills, use_container_width=True)

    with right:
        # CITIES BAR CHART
        st.subheader("🏙️ Top 10 Hiring Cities")
        city_df = df[df["location"] != "India"]["location"].value_counts().head(10).reset_index()
        city_df.columns = ["city", "count"]
        city_df["city"] = city_df["city"].str.split(",").str[0]

        fig_cities = px.bar(
            city_df,
            x="count",
            y="city",
            orientation="h",
            color="count",
            color_continuous_scale="greens",
            labels={"count": "Job Postings", "city": "City"}
        )
        fig_cities.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"}
        )
        st.plotly_chart(fig_cities, use_container_width=True)

    st.divider()

    # --- SECOND ROW ---
    left2, right2 = st.columns(2)

    with left2:
        # ROLE DISTRIBUTION PIE CHART
        st.subheader("🎯 Job Distribution by Role")
        role_df = df["search_title"].value_counts().reset_index()
        role_df.columns = ["role", "count"]

        fig_roles = px.pie(
            role_df,
            values="count",
            names="role",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_roles.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_roles, use_container_width=True)

    with right2:
        # TOP COMPANIES TABLE
        st.subheader("🏢 Top Hiring Companies")
        company_df = df.groupby("company").size().reset_index(name="jobs_posted")
        company_df = company_df.sort_values("jobs_posted", ascending=False).head(10)
        company_df = company_df.reset_index(drop=True)
        company_df.index = company_df.index + 1
        st.dataframe(
            company_df,
            use_container_width=True,
            height=350
        )

    st.divider()

    # --- AI BRIEFING PANEL ---
    st.subheader("🤖 AI Generated Market Briefing")
    st.markdown("*Automatically generated by Groq LLaMA 3 based on live data*")

    briefing = load_briefing()
    st.info(briefing)

    st.divider()

    # --- RAW DATA EXPLORER ---
    st.subheader("🔍 Explore Raw Data")
    st.markdown("Filter and explore all job postings")

    # Filter by role
    roles = ["All"] + list(df["search_title"].unique())
    selected_role = st.selectbox("Filter by Role", roles)

    if selected_role != "All":
        filtered_df = df[df["search_title"] == selected_role]
    else:
        filtered_df = df

    # Show filtered data
    st.dataframe(
        filtered_df[["title", "company", "location", "skills_found", "salary_range", "search_title"]],
        use_container_width=True,
        height=300
    )

    st.caption(f"Showing {len(filtered_df)} job postings | Job Market Pulse v1.0 | Data from Adzuna API")

if __name__ == "__main__":
    main()