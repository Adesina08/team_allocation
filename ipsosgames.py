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
        "Team Security": [
            {"Name": "UFDMBA, Stella"}, {"Name": "ADIGUN, Olamide"}, 
            {"Name": "OYEKOLA, Ruth"}, {"Name": "ADFYOLANU, Adeyemi"},
            {"Name": "ANUFORO, Sylvester"}, {"Name": "EZENDU, Chiamaka"}
        ],
        "Team Simplicity": [
            {"Name": "OLADEJO, Michael"}, {"Name": "AYOOLA, Victoria"},
            {"Name": "OLAPEJU, Henrietta"}, {"Name": "SALAMI, Ibitayo"},
            {"Name": "OBARO, Micheal"}
        ],
        "Team Speed": [
            {"Name": "OMIWE, Winifred"}, {"Name": "BAKARE, Olasubomi"},
            {"Name": "MOSUGU, Ronke"}, {"Name": "DAIRO, Opeyemi"},
            {"Name": "OKUNLOLA, Fatimoh"}
        ],
        "Team Substance": [
            {"Name": "OWODUNNI, Mayedun"}, {"Name": "MEKULEYI, Oluwapelumi"},
            {"Name": "HYACINTH, Jackson"}, {"Name": "OLAJUBU Olaniyi"},
            {"Name": "OLUFISAYO-MICHAEL, Abimbola"}, {"Name": "OGUNNAIKE, Jane"}
        ]
    }
if "available_staff" not in st.session_state:
    excel_file_path = "staffs.xlsx"
    df = pd.read_excel(excel_file_path)
    
    # Get list of pre-assigned names
    pre_assigned = [
        member["Name"] for team in st.session_state.team_assignments.values() 
        for member in team
    ]
    
    # Filter out pre-assigned staff
    st.session_state.available_staff = df[~df["Name"].isin(pre_assigned)]
    
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

def calculate_best_team(staff, eligible_teams):
    """
    Enhanced fairness algorithm using:
    - Team size balancing
    - Gender diversity protection
    - Level distribution
    - Category diversity
    - Random tie-breaking
    """
    team_scores = []
    team_sizes = {t: len(m) for t, m in st.session_state.team_assignments.items()}
    avg_size = sum(team_sizes.values()) / len(team_sizes)
    
    for team in eligible_teams:
        members = st.session_state.team_assignments[team]
        current_size = team_sizes[team]
        
        # Diversity metrics
        same_level = sum(1 for m in members if m["Level"] == staff["Level"])
        same_category = sum(1 for m in members if m["Category"] == staff["Category"])
        same_gender = sum(1 for m in members if m["Gender"] == staff["Gender"])
        
        # Size penalty (encourage balanced teams)
        size_penalty = abs(current_size - avg_size) ** 1.2
        
        # Diversity penalty weights
        penalty = (
            (same_level * 4) +      # Strong penalty for same level
            (same_category * 3) +   # Medium penalty for same category
            (same_gender * 2) +     # Small penalty for same gender
            size_penalty
        )
        
        # Add randomness for tie-breaking
        team_scores.append((
            penalty,
            random.random(),  # Random factor
            -len(set(m["Level"] for m in members)),  # Prefer level diversity
            current_size,     # Prefer smaller teams
            team
        ))
    
    # Sort by: 1) Penalty 2) Random 3) Level diversity 4) Team size
    team_scores.sort()
    
    return team_scores[0][-1]

def check_constraints(staff_member, team):
    """Enhanced constraints with gender balance"""
    current_team = st.session_state.team_assignments[team]
    current_members = [m["Name"] for m in current_team]
    
    # 1. Hard constraints
    if any(name in current_members for name in st.session_state.incompatible_pairs.get(staff_member["Name"], [])):
        return False
        
    # 2. Gender balance (max 75% same gender)
    if len(current_team) >= 4:
        gender_count = sum(1 for m in current_team if m["Gender"] == staff_member["Gender"])
        if (gender_count + 1) / (len(current_team) + 1) > 0.75:
            return False
            
    # 3. Max team size
    if len(current_team) >= 7:
        return False
        
    return True

# Add this in your team_assignment_page function where the download button appears:
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
    
    if st.session_state.available_staff.empty:
        # Export team assignments
        assignments_json = json.dumps(st.session_state.team_assignments, indent=2)
        st.download_button(
            label="📥 Download Team Assignments (JSON)",
            data=assignments_json,
            file_name="team_assignments.json",
            mime="application/json"
        )
        
        # Export remaining staff list (empty in this case)
        st.warning("All staff have been assigned!")
    else:
        # Add continuous export capability
        csv = st.session_state.available_staff.to_csv(index=False)
        st.download_button(
            label="📥 Export Remaining Staff (CSV)",
            data=csv,
            file_name="remaining_staff.csv",
            mime="text/csv"
        )

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
    """Enhanced Standings Page with Correct Podium Ordering"""
    st.title("🏆 Team Standings & Historical Performance")
    
    try:
        # Load historical gameweek data
        gameweeks = pd.read_csv("gameweeks.csv")
        latest_gw = gameweeks['Gameweek'].max()

                # --- Current Gameweek Podium ---
        st.markdown("---")
        st.header(f"🎮 Gameweek {latest_gw} Podium")
        current_gw_data = gameweeks[gameweeks['Gameweek'] == latest_gw]
        
        # Proper ordering: 1st, 2nd, 3rd, 4th
        cols = st.columns(4)
        positions = {
            1: (cols[0], "🥇", "#FFD700"),
            2: (cols[1], "🥈", "#C0C0C0"),
            3: (cols[2], "🥉", "#CD7F32"),
            4: (cols[3], "🔹", "#808080")
        }

        for pos in sorted(current_gw_data['Position'].unique()):
            team = current_gw_data[current_gw_data['Position'] == pos]['Team'].values[0]
            points = current_gw_data[current_gw_data['Position'] == pos]['PointsEarned'].values[0]
            col, medal, color = positions[pos]
            with col:
                st.markdown(f"""
                    <div style='text-align: center; 
                                border: 2px solid {color};
                                padding: 15px; 
                                border-radius: 10px;
                                margin: 10px;
                                background: rgba(255,255,255,0.1);'>
                        <h3>{medal} {team}</h3>
                        <p>⭐ {points} Points</p>
                    </div>
                """, unsafe_allow_html=True)

        # --- Current Standings Section ---
        st.header(f"📊 Current Overall Standings (After {latest_gw} Gameweeks)")
        
        # Calculate cumulative standings
        current_standings = calculate_standings(gameweeks)
        show_standings_table(current_standings)

        # --- Historical Gameweeks Section ---
        st.markdown("---")
        st.header("📅 Previous Gameweeks")
        historical_gws = sorted(gameweeks['Gameweek'].unique()[:-1], reverse=True)
        
        for gw in historical_gws:
            gw_data = gameweeks[gameweeks['Gameweek'] == gw]
            cumulative_data = gameweeks[gameweeks['Gameweek'] <= gw]
            gw_date = gw_data['Date'].iloc[0]
            
            with st.expander(f"Gameweek {gw} - {gw_date}", expanded=False):
                # Historical Podium
                st.subheader(f"Week {gw} Podium 🏅")
                gw_cols = st.columns(4)
                gw_positions = {
                    1: (gw_cols[0], "🥇", "#FFD700"),
                    2: (gw_cols[1], "🥈", "#C0C0C0"),
                    3: (gw_cols[2], "🥉", "#CD7F32"),
                    4: (gw_cols[3], "🔹", "#808080")
                }

                for pos in sorted(gw_data['Position'].unique()):
                    team = gw_data[gw_data['Position'] == pos]['Team'].values[0]
                    points = gw_data[gw_data['Position'] == pos]['PointsEarned'].values[0]
                    col, medal, color = gw_positions[pos]
                    with col:
                        st.markdown(f"""
                            <div style='text-align: center; 
                                        border: 2px solid {color};
                                        padding: 15px; 
                                        border-radius: 10px;
                                        margin: 10px;
                                        background: rgba(255,255,255,0.1);'>
                                <h4>{medal} {team}</h4>
                                <p>⭐ {points} Points</p>
                            </div>
                        """, unsafe_allow_html=True)

                # Cumulative Standings Table
                st.markdown("### Cumulative Standings After This Week")
                historical_standings = calculate_standings(cumulative_data)
                show_standings_table(historical_standings)

    except FileNotFoundError:
        st.error("No gameweek data available yet! Check back after the first matches.")
        st.image("images/coming_soon.jpg", use_container_width=True)
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")

# Keep calculate_standings() and show_standings_table() functions unchanged from previous version

def calculate_standings(data):
    """Calculate standings from gameweek data"""
    agg_stats = data.groupby('Team').agg(
        GamesPlayed=('Gameweek', 'count'),
        TotalPoints=('PointsEarned', 'sum')
    ).reset_index()

    position_counts = pd.crosstab(
        index=data['Team'], 
        columns=data['Position'], 
        colnames=[None]
    ).reset_index()
    position_counts.columns = ['Team', '1ST', '2ND', '3RD', '4TH']

    standings = pd.merge(agg_stats, position_counts, on='Team', how='outer')
    return standings.fillna(0).astype({
        '1ST': int, '2ND': int, '3RD': int, '4TH': int
    })[['Team', 'GamesPlayed', '1ST', '2ND', '3RD', '4TH', 'TotalPoints']]

def show_standings_table(standings):
    """Display styled standings table with all columns"""
    st.dataframe(
        standings.sort_values('TotalPoints', ascending=False)
        .style
        .format({'TotalPoints': '{:.0f}'})
        .set_properties(**{'text-align': 'center'})  # Center alignment added here
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
