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
    initial_sidebar_state="expanded",
)

# Initialize session state with minimum team size
if "page" not in st.session_state:
    st.session_state.page = "home"
if "team_assignments" not in st.session_state:
    st.session_state.team_assignments = {
        "Team Security": [],
        "Team Simplicity": [],
        "Team Speed": [],
        "Team Substance": [],
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
        background: linear-gradient(135deg, #0000FF 0%, #00008B 100%); /* Blue */
        color: white;
    }
    .team-speed {
        background: linear-gradient(135deg, #FF0000 0%, #8B0000 100%); /* Red */
        color: white;
    }
    .team-substance {
        background: linear-gradient(135deg, #FFFFFF 0%, #D3D3D3 100%); /* White */
        color: black;
    }
    .team-simplicity {
        background: linear-gradient(135deg, #FFFF00 0%, #FFD700 100%); /* Yellow */
        color: black;
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
                <p style='margin:5px 0;'>Team Captain: Michael DUMKWUSON 🥇</p>
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

    # st.markdown("""
    # <div class='rules-container'>
    #     <h2 class='rules-header'>📋 Team Allocation Rules</h2>
    #     <div class='rule-item'>
    #         <strong>Deterministic Assignment:</strong> Teams are allocated using a penalty‐score algorithm to minimize similarities.
    #     </div>
    # </div>
    # """, unsafe_allow_html=True)

def check_constraints(staff_member, team):
    """Check only incompatible pairs and team balance"""
    current_team = st.session_state.team_assignments[team]
    
    # 1. Incompatibility check
    incompatible_staff = st.session_state.incompatible_pairs.get(staff_member["Name"], [])
    current_members = [m["Name"] for m in current_team]
    if any(name in current_members for name in incompatible_staff):
        return False
    
    # # 2. Minimum team size protection
    # team_sizes = {t: len(m) for t, m in st.session_state.team_assignments.items()}
    # min_size = min(team_sizes.values())
    # if len(current_team) - min_size >= 2:
    #     return False
    
    return True

def calculate_best_team(staff, eligible_teams):
    """
    Calculate a penalty score for each eligible team based on matching attributes:
      - "Group in previous game" (×5)
      - "Level" (×3)
      - "Office floor" (×2)
      - "Gender" (×2)
    Returns the team (from eligible_teams) with the lowest penalty.
    """
    team_scores = []
    for team in eligible_teams:
        members = st.session_state.team_assignments[team]
        prev_group_count = sum(1 for m in members if m.get("Group in previous game") == staff.get("Group in previous game"))
        level_count = sum(1 for m in members if m.get("Level") == staff.get("Level"))
        office_floor_count = sum(1 for m in members if m.get("Category") == staff.get("Category"))
        gender_count = sum(1 for m in members if m.get("Gender") == staff.get("Gender"))
        penalty = (prev_group_count * 5) + (level_count * 3) + (office_floor_count * 2) + (gender_count * 2)
        team_scores.append((penalty, len(members), team))
    team_scores.sort(key=lambda x: (x[0], x[1], x[2]))
    return team_scores[0][2]

def team_assignment_page():
    """Modified team assignment page with immediate updates"""
    st.title("Team Assignment Dashboard")
    # Ensure that there is an element to scroll to:
    st.markdown("<div class='scroll-target'></div>", unsafe_allow_html=True)
    
    # Display teams
    cols = st.columns(4)
    team_colors = {
        "Team Security": "team-security",
        "Team Speed": "team-speed",
        "Team Substance": "team-substance",
        "Team Simplicity": "team-simplicity",
    }

    for idx, (team, members) in enumerate(st.session_state.team_assignments.items()):
        with cols[idx]:
            count = len(members)
            # Only create the members list container if there are assigned members
            if members:
                member_cards = "".join([f"<p>{m['Name']}</p>" for m in members])
                members_html = f"<div class='members-list'>{member_cards}</div>"
            else:
                members_html = ""
            st.markdown(f"""
                <div class='team-container {team_colors[team]}'>
                    <h3>{team} ({count})</h3>
                    {members_html}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("### Available Staff Members")
    
    # When all staff have been assigned, show a download button to save assignments
    if st.session_state.available_staff.empty:
        # Convert team assignments to a JSON string for download
        assignments_json = json.dumps(st.session_state.team_assignments, indent=2)
        st.download_button(
            label="Download Team Assignments",
            data=assignments_json,
            file_name="team_assignments.json",
            mime="application/json"
        )
    else:
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
                            assign_team_member()

def assign_team_member():
    """Assignment logic with the deterministic penalty algorithm."""
    staff = st.session_state.selected_staff

    # Countdown for dramatic effect
    countdown = st.empty()
    for i in range(3, 0, -1):
        countdown.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(1.5)
    countdown.empty()

    # Determine eligible teams based on constraints
    eligible_teams = [team for team in st.session_state.team_assignments if check_constraints(staff, team)]
    
    if eligible_teams:
        # Use the penalty algorithm to choose the best team
        assigned_team = calculate_best_team(staff, eligible_teams)
    else:
        # Fallback: assign to the team with the smallest number of members
        assigned_team = min(st.session_state.team_assignments, key=lambda t: len(st.session_state.team_assignments[t]))
    
    # Update team assignments
    st.session_state.team_assignments[assigned_team].append(st.session_state.selected_staff)
    
    # Auto-scroll back to the top
    components.html("""
    <script>
        window.parent.document.querySelector('.scroll-target').scrollIntoView();
    </script>
    """, height=0)
    
    # Show a success message
    success = st.markdown(
        f"""<div class='success-message'>
            <h2>🎉 Success!</h2>
            <p>{staff["Name"]} has been assigned to Team {assigned_team}!👍</p>
        </div>""", 
        unsafe_allow_html=True
    )
    time.sleep(1.5)
    success.empty()
    
    # Force UI update
    st.rerun()

def standings_page():
    """Enhanced Standings Page with Dynamic Calculations"""
    st.title("🏆 Team Standings & Historical Performance")
    
    try:
        # Load historical gameweek data
        gameweeks = pd.read_csv("gameweeks.csv")
        
        # --- Calculate Current Standings ---
        # Aggregate basic stats
        agg_stats = gameweeks.groupby('Team').agg(
            GamesPlayed=('Gameweek', 'count'),
            TotalPoints=('PointsEarned', 'sum')
        ).reset_index()

        # Calculate position counts
        position_counts = pd.crosstab(
            index=gameweeks['Team'], 
            columns=gameweeks['Position'], 
            colnames=[None]
        ).reset_index()
        position_counts.columns = ['Team', '1ST', '2ND', '3RD', '4TH']

        # Merge and clean data
        current_standings = pd.merge(agg_stats, position_counts, on='Team', how='outer')
        current_standings = current_standings.fillna(0).astype({
            '1ST': int, '2ND': int, '3RD': int, '4TH': int
        })[['Team', 'GamesPlayed', '1ST', '2ND', '3RD', '4TH', 'TotalPoints']]

        # --- Display Current Standings ---
        st.header("📊 Current Season Standings")
        st.dataframe(
            current_standings.style
                .format({'TotalPoints': '{:.0f}'})
                .apply(lambda x: ['background: #0000FF20' if x.Team == 'Team Security' else 
                                'background: #FF000020' if x.Team == 'Team Speed' else
                                'background: #FFFFFF20' if x.Team == 'Team Substance' else
                                'background: #FFFF0020' for i in x], axis=1),
            column_config={
                "Team": st.column_config.TextColumn("Team", width="medium"),
                "GamesPlayed": st.column_config.NumberColumn("🎮 Played", format="%d"),
                "1ST": st.column_config.NumberColumn("🏆 1st", format="%d"),
                "2ND": st.column_config.NumberColumn("🥈 2nd", format="%d"),
                "3RD": st.column_config.NumberColumn("🥉 3rd", format="%d"),
                "4TH": st.column_config.NumberColumn("🔹 4th", format="%d"),
                "TotalPoints": st.column_config.NumberColumn("⭐ Points", format="%d")
            },
            use_container_width=True,
            hide_index=True
        )

        # --- Historical Gameweeks Section ---
        st.markdown("---")
        st.header("📅 Previous Gameweeks")
        unique_gws = sorted(gameweeks['Gameweek'].unique(), reverse=True)
        
        for gw in unique_gws:
            gw_data = gameweeks[gameweeks['Gameweek'] == gw]
            gw_date = gw_data['Date'].iloc[0]
            
            with st.expander(f"Gameweek {gw} - {gw_date}", expanded=False):
                # Podium Display
                cols = st.columns([1, 2, 1])
                podium_positions = {1: cols[1], 2: cols[0], 3: cols[2]}
                
                for pos in [1, 2, 3]:
                    team = gw_data[gw_data['Position'] == pos]['Team'].values[0]
                    points = gw_data[gw_data['Position'] == pos]['PointsEarned'].values[0]
                    with podium_positions[pos]:
                        st.subheader(f"{['🥈', '🥇', '🥉'][pos-1]} {team}")
                        st.caption(f"{points} points")

                # Detailed Table
                gw_table = gw_data[['Team', 'Position', 'PointsEarned']].sort_values('Position')
                st.dataframe(
                    gw_table.style.applymap(lambda x: 'color: #FFD700' if x == 1 else 
                                          'color: #C0C0C0' if x == 2 else 
                                          'color: #CD7F32' if x == 3 else ''),
                    column_config={
                        "Position": st.column_config.NumberColumn("🏅 Position", format="%d"),
                        "PointsEarned": st.column_config.NumberColumn("⭐ Points", format="%d")
                    },
                    use_container_width=True,
                    hide_index=True
                )

    except FileNotFoundError:
        st.error("No gameweek data available yet! Check back after the first matches.")
        st.image("images/coming_soon.jpg", use_container_width=True)
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")

def ai_champions_page():
    """Original AI Champions page preserved"""
    st.title("Meet the AI Champions 🚀")
    
    team_members = [
        {
            "name": "Alexan Carrilho",
            "email": "Alexan.Carrilho@ipsos.com",
            "image": "images/alexan.jpeg",
        },
        {
            "name": "Oludare Alatise",
            "email": "Oludare.Alatise@ipsos.com",
            "image": "images/dare.jpeg",
        },
        {
            "name": "Samuel Jimoh",
            "email": "Samuel.Jimoh@ipsos.com",
            "image": "images/samuel.jpeg",
        },
        {
            "name": "Paul Oluwadare",
            "email": "Paul.Oluwadare@ipsos.com",
            "image": "images/paul.jpeg",
        },
        {
            "name": "Adesina Adeyemo",
            "email": "Adesina.Adeyemo@ipsos.com",
            "image": "images/Adesina_Pic.jpg",
        },
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
            """
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
