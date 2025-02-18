import streamlit as st
import pandas as pd
import time
import random
from PIL import Image
import plotly.graph_objects as go
import numpy as np
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_card import card
import json
import io
from PIL import Image
import base64
import os
import math
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="2025 Ipsos Games",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state with minimum team size
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
    excel_file_path = "staffs.xlsx"
    df = pd.read_excel(excel_file_path)
    st.session_state.available_staff = df
    
    # Load incompatible pairs
    incompatible_pairs = {}
    for _, row in df.iterrows():
        name = row["Name"]
        incompatible = row.get("Incompatible With", "")
        if pd.isna(incompatible):
            incompatible = ""
        incompatible_list = [x.strip() for x in str(incompatible).split(",")] if incompatible else []
        incompatible_pairs[name] = incompatible_list
    st.session_state.incompatible_pairs = incompatible_pairs

# Enhanced CSS with new team colors
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
    
    .scroll-target {
        position: absolute;
        top: -100px;
    }
    /* Button Styles */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
        /* Team Container Styles */
    .team-container {
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
        /* Member Card Styles */
    .member-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 15px;
        margin: 8px 0;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        color: #333;
    }
    .member-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Countdown Animation */
    .countdown {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 100px;
        font-weight: bold;
        color: #1f77b4;
        z-index: 9999;
        animation: pulse 0.5s ease-in-out;
    }
    @keyframes pulse {
        0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
        50% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
    }
    
    /* Rules Section */
    .rules-container {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .rules-header {
        color: #2C3E50;
        font-size: 1.8em;
        margin-bottom: 20px;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
    }
    .rule-item {
        padding: 10px;
        margin: 5px 0;
        border-left: 3px solid #1f77b4;
        background-color: white;
        border-radius: 0 8px 8px 0;
    }
    
    /* Success Message */
    .success-message {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: rgba(40, 167, 69, 0.9);
        color: white;
        padding: 20px 40px;
        border-radius: 10px;
        z-index: 9999;
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translate(-50%, -60%); }
        to { opacity: 1; transform: translate(-50%, -50%); }
    }
    /* Gallery Section Styles */
    .gallery-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        padding: 20px;
    }
    
    .gallery-item {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .fun-moments-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 75px;
    }
    
    /* Staff Categories Section */
    .staff-category {
        background: linear-gradient(to right, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .staff-category h3 {
        color: #2C3E50;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 5px;
        margin-bottom: 10px;
    }
    
    .staff-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 10px;
        padding: 10px;
    }
       /* Team member styles */
    .team-member-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
        
    .member-photo {
        width: 150px;
        height: 150px;
        border-radius: 75px;
        margin: 0 auto 15px auto;
        overflow: hidden;
    }
        
    .member-photo img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
        
        .member-name {
            font-size: 1.2em;
            color: #2C3E50;
            margin-bottom: 5px;
        }
        
    .member-email {
        color: #666;
        font-size: 0.9em;
    }
</style>
""",
    unsafe_allow_html=True,
)

def get_image_base64(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None

def create_image_grid(images, images_per_row=3):
    """Create image grid (original implementation preserved)"""
    num_rows = math.ceil(len(images) / images_per_row)
    for row in range(num_rows):
        cols = st.columns(images_per_row)
        for col in range(images_per_row):
            idx = row * images_per_row + col
            if idx < len(images):
                with cols[col]:
                    st.image(images[idx], use_container_width=True)

def home_page():
    """Original home page with modifications for new teams"""
    st.title("Welcome to Ipsos Games 2025 🎮")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Previous Winners")
        st.markdown("""
            <div style='padding:15px; background:#f8f9fa; border-radius:5px; margin-bottom:15px;'>
                <h4 style='margin-top:0; color:#2C3E50;'>Overall Champions 2024: Team Integrity</h4>
                <p style='margin:5px 0;'>Team Captain: Micheal Dukumnsin</p>
            </div>
        """, unsafe_allow_html=True)
        st.image("images/moment_1_page-0012.jpg", use_container_width=True)

    with col2:
        st.markdown("### 📸 Fun Moments")
        fun_moments_images = [
            "images/moment_1_page-0008.jpg",
            "images/moment_1_page-0017.jpg",
            "images/moment_1_page-0018.jpg",
            "images/moment_1_page-0014.jpg",
            "images/moment_1_page-0012.jpg",
            "images/moment_1_page-0009.jpg",
            "images/moment_1_page-0011.jpg",
            "images/moment_1_page-0001.jpg",
            "images/moment_1_page-0003.jpg",
        ]
        create_image_grid(fun_moments_images)

    st.markdown("""
    <div class='rules-container'>
        <h2 class='rules-header'>📋 Team Allocation Rules</h2>
        </div>
        <div class='rule-item'>
            <strong>Random Assignment:</strong> Team allocation is randomized among eligible teams
        </div>
    </div>
    """, unsafe_allow_html=True)

def check_constraints(staff_member, team):
    """Check only incompatible pairs and team balance"""
    current_team = st.session_state.team_assignments[team]
    
    # 1. Incompatibility check
    incompatible_staff = st.session_state.incompatible_pairs.get(staff_member["Name"], [])
    current_members = [m["Name"] for m in current_team]
    if any(name in current_members for name in incompatible_staff):
        return False
    
    # 2. Minimum team size protection
    team_sizes = {t: len(m) for t, m in st.session_state.team_assignments.items()}
    min_size = min(team_sizes.values())
    if len(current_team) - min_size >= 2:
        return False
    
    return True

def team_assignment_page():
    """Modified team assignment page with immediate updates"""
    st.title("Team Assignment Dashboard")
    st.markdown('<div class="scroll-target" id="top"></div>', unsafe_allow_html=True)

    # Display teams
    cols = st.columns(4)
    team_colors = {
        "Security": "team-security",
        "Seamless": "team-seamless",
        "Social": "team-social",
        "Sassy": "team-sassy",
    }

    for idx, (team, members) in enumerate(st.session_state.team_assignments.items()):
        with cols[idx]:
            count = len(members)
            st.markdown(f"""
                <div class='team-container {team_colors[team]}'>
                    <h3>{team} ({count})</h3>
                    <div class='members-list'>
                        {"".join([f"<p>{m['Name']}</p>" for m in members])}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("### Available Staff Members")
    
    if st.session_state.available_staff.empty:
        st.button("Download Screenshot")

    # Fixed category display for Floor 0-1
    categories = ["Leadership", "Diaspora", "Floor 0-1", "Floor 2", 
                "Floor 3", "Floor 4", "Floor 5"]
    
    for category in categories:
        staff_df = st.session_state.available_staff[
            st.session_state.available_staff["Category"] == category
        ]
        if not staff_df.empty:
            st.markdown(f"#### {category.replace('0-1', '0 - 1')}")  # Better formatting
            cols = st.columns(6)
            for idx, (_, staff) in enumerate(staff_df.iterrows()):
                with cols[idx % 6]:
                    if st.button(staff["Name"], key=f"staff_{category}_{idx}"):
                        # Immediate removal and UI update
                        st.session_state.available_staff = st.session_state.available_staff[
                            st.session_state.available_staff["Name"] != staff["Name"]]
                        st.session_state.selected_staff = staff.to_dict()
                        st.rerun()  # Force immediate UI update
                        assign_team_member()

def standings_page():
    """New standings page"""
    st.title("Team Standings")
    
    try:
        standings = pd.read_csv("standings.csv")
        st.markdown("### Current Rankings")
        st.dataframe(standings.style.highlight_max(subset="POINTS", color='#d4edda'), 
                    use_container_width=True)
        
        st.markdown("### Upcoming Games")
        st.write("""
        - Monday: Security vs Seamless
        - Tuesday: Social vs Sassy
        - Wednesday: Semi-finals
        - Friday: Grand Finale
        """)
    except FileNotFoundError:
        st.error("Standings data will be updated weekly")

def assign_team_member():
    """Improved assignment logic with better randomization"""
    staff = st.session_state.selected_staff
    
    # Faster countdown with progress
    countdown = st.empty()
    for i in range(3, 0, -1):
        countdown.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(0.5)  # Reduced from 1s to 0.5s
    countdown.empty()
    
    # Get suitable teams with intelligent sorting
    suitable_teams = [t for t in st.session_state.team_assignments 
                     if check_constraints(staff, t)]
    
    # Prioritize teams with fewer members
    suitable_teams.sort(key=lambda t: len(st.session_state.team_assignments[t]))
    
    if suitable_teams:
        # Weighted random choice favoring smaller teams
        weights = [1/(len(st.session_state.team_assignments[t])+1) for t in suitable_teams]
        assigned_team = random.choices(suitable_teams, weights=weights, k=1)[0]
    else:
        # Fallback to smallest team if no suitable teams
        assigned_team = min(st.session_state.team_assignments,
                          key=lambda t: len(st.session_state.team_assignments[t]))
    
    # Update team assignments
    st.session_state.team_assignments[assigned_team].append(staff)
    
    # Visible success message
    success = st.markdown(
        f"""<div class='success-message'>
            <h2>🎉 Success!</h2>
            <p>{staff["Name"]} → {assigned_team}</p>
        </div>""", 
        unsafe_allow_html=True
    )
    time.sleep(1.5)
    success.empty()
    
    # Force UI update
    st.rerun()

def ai_champions_page():
    """Original AI Champions page preserved"""
    st.title("Meet the AI Champions 🚀")
    
    team_members = [
        {"name": "Alexan Carrilho", "email": "Alexan.Carrilho@ipsos.com", 
         "image": "images/alexan.jpeg",},
        {"name": "Oludare Alatise", "email": "Oludare.Alatise@ipsos.com",
         "image": "images/dare.jpeg",},
        {"name": "Samuel Jimoh","email": "Samuel.Jimoh@ipsos.com",
         "image": "images/samuel.jpeg",},
        {"name": "Paul Oluwadare","email": "Paul.Oluwadare@ipsos.com",
         "image": "images/paul.jpeg",},
        {"name": "Adesina Adeyemo","email": "Adesina.Adeyemo@ipsos.com",
         "image": "images/Adesina_Pic.jpg",},
    ]
    
    cols = st.columns(3)
    
    for i, member in enumerate(team_members):
        with cols[i % 3]:
            img_base64 = get_image_base64(member["image"])
            
            # Create the card HTML with proper structure and styling
            card_html = f"""
                <div class="team-member-card">
                    <div class="member-photo">
                        <img src="data:image/jpeg;base64,{img_base64}" alt="{member['name']}" />
                    </div>
                    <div class="member-name">{member["name"]}</div>
                    <div class="member-email">{member["email"]}</div>
                </div>

            st.markdown(card_html, unsafe_allow_html=True)

# Navigation system
pages = {
    "🏠 Home": "home",
    "📋 Team Assignment": "assignment",
    "📊 Standings": "standings",
    "🤖 AI Champions": "champions"
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
