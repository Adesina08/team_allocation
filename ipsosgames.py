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


def get_image_base64(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None


# Enhanced Custom CSS with team colors and animations
st.markdown(
    """ 
<style>
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
    .team-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    /* Team Colors */
    .team-collaboration {
        background: linear-gradient(135deg, #4CA1AF 0%, #2C3E50 100%);
        color: white;
    }
    .team-integrity {
        background: linear-gradient(135deg, #FF4B2B 0%, #FF416C 100%);
        color: white;
    }
    .team-curiosity {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        color: white;
    }
    .team-client-first {
        background: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%);
        color: white;
    }
    .team-entrepreneurial {
        background: linear-gradient(135deg, #F7971E 0%, #FFD200 100%);
        color: white;
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
        gap: 15px;
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
# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "team_assignments" not in st.session_state:
    st.session_state.team_assignments = {
        "Team Collaboration": [],
        "Team Integrity": [],
        "Team Curiosity": [],
        "Team Client First": [],
        "Team Entrepreneurial Spirit": [],
    }
if "available_staff" not in st.session_state:
    # Load staff data from Excel file
    excel_file_path = (
        r"C:\Users\Adesina.Adeyemo\Documents\staffs.xlsx"  # Update with your file path
    )
    st.session_state.available_staff = pd.read_excel(excel_file_path)


def create_image_grid(images, images_per_row=3):
    """Create a grid of images with consistent spacing and sizing"""
    # Calculate number of rows needed
    num_rows = math.ceil(len(images) / images_per_row)

    # Custom CSS for image grid
    st.markdown(
        """
        <style>
        .image-grid-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .image-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .stImage {
            margin: 0 auto;
        }
        .image-caption {
            text-align: center;
            margin-top: 5px;
            color: #666;
            font-size: 0.9em;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Create rows
    for row in range(num_rows):
        cols = st.columns(images_per_row)
        for col in range(images_per_row):
            idx = row * images_per_row + col
            if idx < len(images):
                with cols[col]:
                    st.image(
                        images[idx],
                        caption=f"Fun Moment {idx + 1}",
                        use_column_width=True,
                    )


def home_page():
    st.title("Welcome to Ipsos Games 2025 🎮")

    # Create two columns for the main sections
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Previous Winners")

        # Winner team details
        st.markdown(
            """
            <div style='padding: 15px; background: #f8f9fa; border-radius: 5px; margin-bottom: 15px; 
                 box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h4 style='margin-top: 0; color: #2C3E50;'>Team Integrity</h4>
                <p style='margin: 5px 0;'>Overall Champions 2024</p>
                <p style='margin: 5px 0;'>Team Captain: Micheal Dukunmsin</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Winner team photo
        st.image(
            "images\moment_1_page-0012.jpg",  # Update with relative path
            use_column_width=True,
            caption="Champion Team Photo",
        )

    with col2:
        st.markdown("### 📸 Fun Moments")

        # List of fun moment images (using relative paths)
        fun_moments_images = [
            "images\moment_1_page-0008.jpg",
            "images\moment_1_page-0017.jpg",
            "images\moment_1_page-0018.jpg",
            "images\moment_1_page-0014.jpg",
            "images\moment_1_page-0012.jpg",
            "images\moment_1_page-0009.jpg",
            "images\moment_1_page-0011.jpg",
            "images\moment_1_page-0001.jpg",
            "images\moment_1_page-0003.jpg",
        ]

        # Create image grid
        create_image_grid(fun_moments_images)

    # New Rules Section
    st.markdown(
        """ 
    <div class='rules-container'>
        <h2 class='rules-header'>📋 Team Allocation Rules</h2>
        <div class='rule-item'>
            <strong>Position Distribution:</strong> Each team can have a maximum of 3 members from the same position level
        </div>
        <div class='rule-item'>
            <strong>Gender Balance:</strong> Teams must maintain a balanced gender representation with no more than 6 members of the same gender
        </div>
        <div class='rule-item'>
            <strong>Previous Team Restriction:</strong> Members cannot be assigned to their previous team
        </div>
        <div class='rule-item'>
            <strong>Random Assignment:</strong> Team allocation is randomized among eligible teams based on the above constraints
        </div>
        <div class='rule-item'>
            <strong>Fairness Policy:</strong> If no team meets all constraints, member will be assigned to the least populated team
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def check_constraints(staff_member, team):
    """Check if staff member can be assigned to team based on constraints"""
    current_team_members = st.session_state.team_assignments[team]

    # Check position distribution
    position_count = sum(
        1
        for member in current_team_members
        if member["Position"] == staff_member["Position"]
    )
    if position_count >= 3:
        return False

    # Check gender balance
    gender_count = sum(
        1
        for member in current_team_members
        if member["Gender"] == staff_member["Gender"]
    )
    if gender_count >= 6:
        return False

    # Check previous team
    if staff_member["Previous Team"] == team:
        return False

    return True


# Function to save team allocations to an Excel file and return the file object
def create_team_allocations_excel():
    # Create a dictionary to hold team members
    team_data = {team: [] for team in st.session_state.team_assignments.keys()}

    # Populate the dictionary with team members
    for team, members in st.session_state.team_assignments.items():
        for member in members:
            team_data[team].append(member["Name"])

    # Create a DataFrame from the dictionary
    max_length = max(len(members) for members in team_data.values())
    for team in team_data:
        # Fill with None for teams with fewer members
        team_data[team] += [None] * (max_length - len(team_data[team]))

    df = pd.DataFrame(team_data)

    # Save the DataFrame to a BytesIO object
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="Team Allocations")
    excel_file.seek(0)  # Move to the beginning of the BytesIO object

    return excel_file


def assign_team_member():
    """Handle team member assignment with enhanced animation"""
    if st.session_state.selected_staff is None:
        return

    staff = st.session_state.selected_staff

    # Centered countdown overlay
    countdown_placeholder = st.empty()
    for i in range(3, 0, -1):
        countdown_placeholder.markdown(
            f"""
        <div class='countdown'>{i}</div>
        """,
            unsafe_allow_html=True,
        )
        time.sleep(1)
    countdown_placeholder.empty()

    # Find suitable team and make assignment
    suitable_teams = []
    for team in st.session_state.team_assignments.keys():
        if check_constraints(staff, team):
            suitable_teams.append(team)

    if suitable_teams:
        assigned_team = random.choice(suitable_teams)
    else:
        # Fallback: assign to least populated team
        team_sizes = {
            team: len(members)
            for team, members in st.session_state.team_assignments.items()
        }
        assigned_team = min(team_sizes, key=team_sizes.get)

    # Update assignments
    st.session_state.team_assignments[assigned_team].append(staff)

    # Remove from available staff
    st.session_state.available_staff = st.session_state.available_staff[
        st.session_state.available_staff["Name"] != staff["Name"]
    ]

    # Display success message with animation
    success_placeholder = st.empty()
    success_placeholder.markdown(
        f"""
    <div class='success-message'>
        <h2>🎉 Success!</h2>
        <p>{staff["Name"]} has been assigned to {assigned_team}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    time.sleep(2.5)
    success_placeholder.empty()

    # Reload page with a query parameter to indicate the target section
    js = """
    <script>
        var url = new URL(window.location.href);
        url.searchParams.set('scrollTo', '279f950c');
        window.location.href = url.toString();
    </script>
    """
    components.html(js, height=0)


def team_assignment_page():
    st.title("Team Assignment Dashboard")

    # Add an ID to the team assignment dashboard container
    st.markdown(
        """
        <div id='279f950c'>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Check for the query parameter
    query_params = st.experimental_get_query_params()
    if query_params.get("scrollTo") == ["team-assignment-dashboard"]:
        js = """
        <script>
            var targetElement = window.parent.document.querySelector("#team-assignment-dashboard");
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        </script>
        """
        st.components.v1.html(js, height=0)

    # Display team sections with enhanced styling
    cols = st.columns(5)
    team_colors = {
        "Team Collaboration": "team-collaboration",
        "Team Integrity": "team-integrity",
        "Team Curiosity": "team-curiosity",
        "Team Client First": "team-client-first",
        "Team Entrepreneurial Spirit": "team-entrepreneurial",
    }

    for idx, (team, members) in enumerate(st.session_state.team_assignments.items()):
        with cols[idx]:
            if members:  # Only display if team has members
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

    # Rest of the function remains unchanged...

    # Staff categories section
    st.markdown("### Available Staff Members")

    # Group staff by category
    categories = [
        "Leadership and Line Managers",
        "Diaspora",
        "Floor 0 & 1",
        "Floor 2",
        "Floor 3",
        "Floor 4",
        "Floor 5",
    ]

    for category in categories:
        # Filter staff by category
        category_staff = st.session_state.available_staff[
            st.session_state.available_staff["Category"] == category
        ]

        if not category_staff.empty:
            st.markdown(
                f"""
            <div class='staff-category'>
                <h3>{category}</h3>
            </div>
            """,
                unsafe_allow_html=True,
            )

            cols = st.columns(6)
            for idx, (_, staff) in enumerate(category_staff.iterrows()):
                with cols[idx % 6]:
                    if st.button(staff["Name"], key=f"staff_{category}_{idx}"):
                        st.session_state.selected_staff = staff.to_dict()
                        assign_team_member()


def ai_champions_page():
    st.title("Meet the AI Champions 🚀")

    # Team members data with images
    team_members = [
        {
            "name": "Alexan Carrilho",
            "email": "Alexan.Carrilho@ipsos.com",
            "image": r"C:\Users\Adesina.Adeyemo\Downloads\alexan.jpeg",
        },
        {
            "name": "Oludare Alatise",
            "email": "Oludare.Alatise@ipsos.com",
            "image": r"C:\Users\Adesina.Adeyemo\Downloads\dare.jpeg",
        },
        {
            "name": "Samuel Jimoh",
            "email": "Samuel.Jimoh@ipsos.com",
            "image": r"C:\Users\Adesina.Adeyemo\Downloads\samuel.jpeg",
        },
        {
            "name": "Paul Oluwadare",
            "email": "Paul.Oluwadare@ipsos.com",
            "image": r"C:\Users\Adesina.Adeyemo\Downloads\paul.jpeg",
        },
        {
            "name": "Adesina Adeyemo",
            "email": "Adesina.Adeyemo@ipsos.com",
            "image": r"C:\Users\Adesina.Adeyemo\Pictures\Adesina_Pic.jpg",
        },
    ]

    # Create columns for displaying champions
    cols = st.columns(3)

    for i, member in enumerate(team_members):
        with cols[i % 3]:
            # Get base64 encoded image
            image_path = os.path.join(
                "images", member["image"]
            )  # Assuming images are in an 'images' folder
            image_base64 = get_image_base64(image_path)

            if image_base64:
                img_html = f'<img src="data:image/jpeg;base64,{image_base64}" style="width: 100%; height: 100%; object-fit: cover;">'
            else:
                img_html = '<div style="background-color: #f0f0f0; width: 100%; height: 100%;"></div>'

            st.markdown(
                f"""
                <div class="team-member-card">
                    <div class="member-photo">
                        {img_html}
                    </div>
                    <div class="member-name">{member["name"]}</div>
                    <div class="member-email">{member["email"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# Navigation
if st.session_state.page == "home":
    home_page()
    if st.button("Go to Team Assignment"):
        st.session_state.page = "assignment"
        st.rerun()
    if st.button("Meet AI Champions"):
        st.session_state.page = "champions"
        st.rerun()

elif st.session_state.page == "assignment":
    team_assignment_page()
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()

elif st.session_state.page == "champions":
    ai_champions_page()
    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
