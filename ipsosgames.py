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
    excel_file_path = "staffs.xlsx"
    st.session_state.available_staff = pd.read_excel(excel_file_path)

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
    /* Keep all original styles below */
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
    .team-container {
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    /* ... (keep all other original CSS styles) ... */
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
                <h4 style='margin-top:0; color:#2C3E50;'>Team Integrity</h4>
                <p style='margin:5px 0;'>Overall Champions 2024</p>
                <p style='margin:5px 0;'>Team Captain: Micheal Dukunmsin</p>
            </div>
        """, unsafe_allow_html=True)
        st.image("images/moment_1_page-0012.jpg", use_container_width=True)

    with col2:
        st.markdown("### 📸 Fun Moments")
        fun_moments_images = [
            "images/moment_1_page-0008.jpg",
            "images/moment_1_page-0017.jpg",
            "images/moment_1_page-0014.jpg",
            "images/moment_1_page-0009.jpg",
            "images/moment_1_page-0011.jpg",
            "images/moment_1_page-0001.jpg",
        ]
        create_image_grid(fun_moments_images)

    st.markdown("""
    <div class='rules-container'>
        <h2 class='rules-header'>📋 Team Allocation Rules</h2>
        <!-- Keep original rule items -->
    </div>
    """, unsafe_allow_html=True)

def check_constraints(staff_member, team):
    """Updated for new teams"""
    current_team = st.session_state.team_assignments[team]
    
    position_count = sum(1 for m in current_team 
                      if m["Position"] == staff_member["Position"])
    if position_count >= 3: return False
    
    gender_count = sum(1 for m in current_team 
                     if m["Gender"] == staff_member["Gender"])
    if gender_count >= 6: return False
    
    if staff_member["Previous Team"] == team: return False
    
    return True

def team_assignment_page():
    """Modified for 4 teams and auto-scroll"""
    st.title("Team Assignment Dashboard")
    st.markdown('<div class="scroll-target" id="top"></div>', unsafe_allow_html=True)

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
                st.markdown(f"""
                    <div class='team-container {team_colors[team]}'>
                        <h3>{team}</h3>
                        <div class='members-list'>
                            {"".join([f"<p>{m['Name']}</p>" for m in members])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("### Available Staff Members")
    
    if st.session_state.available_staff.empty:
        st.button("Download Screenshot", 
                 help="Use browser screenshot tool (Ctrl+Shift+S/Cmd+Shift+S)")

    categories = ["Leadership", "Diaspora", "Floor 0-1", "Floor 2", 
                "Floor 3", "Floor 4", "Floor 5"]
    
    for category in categories:
        staff_df = st.session_state.available_staff[
            st.session_state.available_staff["Category"] == category
        ]
        if not staff_df.empty:
            st.markdown(f"#### {category}")
            cols = st.columns(6)
            for idx, (_, staff) in enumerate(staff_df.iterrows()):
                with cols[idx % 6]:
                    if st.button(staff["Name"], key=f"staff_{category}_{idx}"):
                        st.session_state.selected_staff = staff.to_dict()
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

def ai_champions_page():
    """Original AI Champions page preserved"""
    st.title("Meet the AI Champions 🚀")
    
    team_members = [
        {"name": "Alexan Carrilho", "email": "Alexan.Carrilho@ipsos.com", 
         "image": "images/alexan.jpeg"},
        {"name": "Oludare Alatise", "email": "Oludare.Alatise@ipsos.com",
         "image": "images/dare.jpeg"},
        # ... (keep original team member data)
    ]
    
    cols = st.columns(3)
    for i, member in enumerate(team_members):
        with cols[i % 3]:
            img_base64 = get_image_base64(member["image"])
            img_html = f'<img src="data:image/jpeg;base64,{img_base64}"' if img_base64 else ''
            st.markdown(f"""
                <div class="team-member-card">
                    <div class="member-photo">{img_html}</div>
                    <div class="member-name">{member["name"]}</div>
                    <div class="member-email">{member["email"]}</div>
                </div>
            """, unsafe_allow_html=True)

def assign_team_member():
    """Updated assignment function with auto-scroll"""
    staff = st.session_state.selected_staff
    
    # Countdown animation
    countdown = st.empty()
    for i in range(3, 0, -1):
        countdown.markdown(f"<div class='countdown'>{i}</div>", unsafe_allow_html=True)
        time.sleep(1)
    countdown.empty()
    
    # Team selection logic
    suitable_teams = [t for t in st.session_state.team_assignments 
                     if check_constraints(staff, t)]
    assigned_team = (random.choice(suitable_teams) if suitable_teams 
                    else min(st.session_state.team_assignments, 
                           key=lambda t: len(st.session_state.team_assignments[t])))
    
    # Update state
    st.session_state.team_assignments[assigned_team].append(staff)
    st.session_state.available_staff = st.session_state.available_staff[
        st.session_state.available_staff["Name"] != staff["Name"]
    ]
    
    # Success message
    success = st.empty()
    success.markdown(
        f"""<div class='success-message'>
            <h2>🎉 Success!</h2>
            <p>{staff["Name"]} → {assigned_team}</p>
        </div>""", 
        unsafe_allow_html=True
    )
    time.sleep(2)
    success.empty()
    
    # Auto-scroll
    components.html("""
    <script>
        window.parent.document.querySelector('.scroll-target').scrollIntoView();
    </script>
    """, height=0)

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

# Staff update explanation
st.sidebar.markdown("---")
st.sidebar.info("""
**Staff Updates:**  
1. Update `staffs.xlsx` file  
2. App will auto-load new data on refresh  

**Standings Updates:**  
1. Modify `standings.csv` weekly  
2. Changes reflect immediately
""")
