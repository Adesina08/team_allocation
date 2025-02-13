import streamlit as st
import pandas as pd
import time
import random
import base64
import os
import math
import streamlit.components.v1 as components
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="2025 Ipsos Games",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "team_assignments" not in st.session_state:
    st.session_state.team_assignments = {
        "Security": [],
        "Seamless": [],
        "Social": [],
        "Sassy": [],
    }
if "available_staff" not in st.session_state:
    excel_file_path = "staffs.xlsx"  # Update with your file path
    st.session_state.available_staff = pd.read_excel(excel_file_path)

# Updated CSS with new team colors
st.markdown(
    """
<style>
    /* Updated Team Colors */
    .team-security {
        background: linear-gradient(135deg, #4CA1AF 0%, #2C3E50 100%);
        color: white;
    }
    .team-seamless {
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        color: white;
    }
    .team-social {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        color: white;
    }
    .team-sassy {
        background: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%);
        color: white;
    }
    
    /* Add auto-scroll target style */
    .scroll-target {
        position: absolute;
        top: -100px;
    }
</style>
""",
    unsafe_allow_html=True,
)

def home_page():
    st.title("Welcome to Ipsos Games 2025 🎮")
    # ... (keep existing home page content)

def team_assignment_page():
    st.title("Team Assignment Dashboard")
    
    # Auto-scroll target
    st.markdown('<div class="scroll-target" id="top"></div>', unsafe_allow_html=True)

    # Display team sections
    cols = st.columns(4)
    team_colors = {
        "Security": "team-security",
        "Seamless": "team-seamless",
        "Social": "team-social",
        "Sassy": "team-sassy",
    }

    for idx, (team, members) in enumerate(st.session_state.team_assignments.items()):
        with cols[idx]:
            if members:
                st.markdown(
                    f"""
                    <div class='team-container {team_colors[team]}'>
                        <h3>{team}</h3>
                        <div class='members-list'>
                            {"".join([f"<p>{member['Name']}</p>" for member in members])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Staff selection section
    st.markdown("### Available Staff Members")
    
    # Check if all staff assigned
    if st.session_state.available_staff.empty:
        if st.button("Download Team Allocation Screenshot"):
            st.info("Please use your browser's screenshot function (Ctrl+Shift+S)")

    # Group staff by category
    categories = ["Leadership", "Diaspora", "Floor 0-1", "Floor 2", "Floor 3", "Floor 4", "Floor 5"]
    
    for category in categories:
        category_staff = st.session_state.available_staff[
            st.session_state.available_staff["Category"] == category
        ]
        if not category_staff.empty:
            st.markdown(f"#### {category}")
            cols = st.columns(6)
            for idx, (_, staff) in enumerate(category_staff.iterrows()):
                with cols[idx % 6]:
                    if st.button(staff["Name"], key=f"staff_{category}_{idx}"):
                        st.session_state.selected_staff = staff.to_dict()
                        assign_team_member()

def standings_page():
    st.title("Team Standings")
    
    # Load standings data from CSV
    try:
        standings = pd.read_csv("standings.csv")
        st.table(standings)
    except FileNotFoundError:
        st.error("Standings data not available yet")

    st.markdown("### Upcoming Games")
    st.write("""
    - Monday: Security vs Seamless
    - Tuesday: Social vs Sassy
    - Wednesday: Semi-finals
    - Friday: Grand Finale
    """)

def assign_team_member():
    """Handle team member assignment with auto-scroll"""
    staff = st.session_state.selected_staff

    # Countdown animation
    countdown_placeholder = st.empty()
    for i in range(3, 0, -1):
        countdown_placeholder.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(1)
    countdown_placeholder.empty()

    # Team assignment logic
    suitable_teams = [team for team in st.session_state.team_assignments if check_constraints(staff, team)]
    assigned_team = random.choice(suitable_teams) if suitable_teams else min(
        {team: len(members) for team, members in st.session_state.team_assignments.items()},
        key=lambda x: x[1]
    )

    # Update state
    st.session_state.team_assignments[assigned_team].append(staff)
    st.session_state.available_staff = st.session_state.available_staff[
        st.session_state.available_staff["Name"] != staff["Name"]
    ]

    # Success message
    success_placeholder = st.empty()
    success_placeholder.markdown(
        f"""<div class='success-message'><h2>🎉 Success!</h2><p>{staff["Name"]} assigned to {assigned_team}</p></div>""",
        unsafe_allow_html=True,
    )
    time.sleep(2)
    success_placeholder.empty()

    # Auto-scroll to top
    components.html(
        f"""
        <script>
            window.parent.document.querySelector('.scroll-target').scrollIntoView();
        </script>
        """,
        height=0
    )

# Navigation
pages = {
    "Home": "home",
    "Team Assignment": "assignment",
    "Standings": "standings",
    "AI Champions": "champions"
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

if pages[selection] == "home":
    home_page()
elif pages[selection] == "assignment":
    team_assignment_page()
elif pages[selection] == "standings":
    standings_page()
elif pages[selection] == "champions":
    ai_champions_page()

# Answering your questions:
# 1. Staff updates: Simply update the staffs.xlsx file - the app will load the new data on next refresh
# 2. Standings updates: Update the standings.csv file weekly. The app will automatically show the latest data
