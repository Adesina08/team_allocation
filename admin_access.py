# admin_uploader.py
import streamlit as st
import requests
import base64
import pandas as pd
from io import StringIO
import traceback

# Configuration - Update these values
REPO_OWNER = "Adesina08"
REPO_NAME = "team_allocation"
FILE_PATH = "gameweeks.csv"
BRANCH = "main"

# Authentication System
def check_password():
    """Password authentication with session management"""
    if 'authenticated' not in st.session_state:
        st.title("🔐 Admin Authentication")
        col1, col2 = st.columns([2, 1])
        with col1:
            password = st.text_input("Enter Admin Password", 
                                   type="password",
                                   help="Contact system administrator for credentials")
        with col2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            if st.button("Authenticate"):
                if password == st.secrets.get("ADMIN_PASSWORD", ""):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password")
                    st.stop()
        st.stop()
    return True

if not check_password():
    st.stop()

# GitHub Configuration
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except KeyError:
    st.error("❌ Missing GitHub token in secrets.toml")
    st.stop()

# Debug Panel
st.sidebar.title("🔧 Debug Panel")
st.sidebar.markdown(f"**Repository:** [{REPO_OWNER}/{REPO_NAME}](https://github.com/{REPO_OWNER}/{REPO_NAME})")
st.sidebar.markdown(f"**Branch:** `{BRANCH}`")
st.sidebar.markdown(f"**Target File:** `{FILE_PATH}`")
st.sidebar.markdown(f"**Token:** `{GITHUB_TOKEN[:4]}...`")

def test_github_connection():
    """Test GitHub API connection with detailed diagnostics"""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    tests = {
        "User Access": "https://api.github.com/user",
        "Repository Access": f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}",
        "File Access": f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    }
    
    results = {}
    for name, url in tests.items():
        try:
            response = requests.get(url, headers=headers)
            results[name] = {
                "status": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.content else {}
            }
        except Exception as e:
            results[name] = {"error": str(e)}
    
    return results

# Connection Test Button
if st.sidebar.button("🔌 Test GitHub Connection"):
    st.sidebar.subheader("Connection Test Results")
    test_results = test_github_connection()
    
    for test_name, result in test_results.items():
        if "error" in result:
            st.sidebar.error(f"**{test_name}:** {result['error']}")
        else:
            if result["success"]:
                st.sidebar.success(f"**{test_name}:** Success (HTTP {result['status']})")
            else:
                st.sidebar.error(f"**{test_name}:** Failed (HTTP {result['status']})")
                st.sidebar.json(result["response"])

# Main Application
st.title("📤 Gameweek Data Upload Portal")
st.markdown("Securely update gameweek standings in the GitHub repository")

def validate_csv(content):
    """Comprehensive CSV validation"""
    try:
        df = pd.read_csv(StringIO(content))
        
        # Column check
        required_columns = ['Gameweek', 'Date', 'Team', 'Position', 'PointsEarned']
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"Missing columns: {', '.join(missing)}")
            return False
            
        # Data type checks
        if not pd.api.types.is_integer_dtype(df['Gameweek']):
            st.error("Gameweek must contain integers")
            return False
            
        if not df['Position'].between(1, 4).all():
            st.error("Positions must be between 1-4")
            return False
            
        # Team validation
        valid_teams = ['Team Security', 'Team Speed', 'Team Substance', 'Team Simplicity']
        invalid_teams = df[~df['Team'].isin(valid_teams)]['Team'].unique()
        if len(invalid_teams) > 0:
            st.error(f"Invalid team names: {', '.join(invalid_teams)}")
            return False
            
        return True
        
    except Exception as e:
        st.error(f"CSV validation failed: {str(e)}")
        return False

def update_github_file(content):
    """GitHub file update with enhanced error handling"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # Get existing file SHA
        response = requests.get(url, headers=headers, params={"ref": BRANCH})
        response.raise_for_status()
        sha = response.json()["sha"]
        
        # Prepare update
        encoded_content = base64.b64encode(content.encode()).decode()
        payload = {
            "message": "Gameweek update via Admin Portal",
            "content": encoded_content,
            "sha": sha,
            "branch": BRANCH
        }

        # Execute update
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        return True
        
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        st.error(f"""
        **GitHub API Error ({e.response.status_code})**
        ```
        {error_data.get('message', 'No error message')}
        Documentation URL: {error_data.get('documentation_url', '')}
        ```
        """)
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.code(traceback.format_exc())
    
    return False

# File Upload Section
uploaded_file = st.file_uploader("Upload CSV file", type="csv",
                               help="Required format: Gameweek, Date, Team, Position, PointsEarned")

if uploaded_file:
    content = uploaded_file.getvalue().decode()
    
    if validate_csv(content):
        st.success("✅ Valid CSV Format")
        
        st.subheader("Data Preview")
        df = pd.read_csv(StringIO(content))
        st.dataframe(df.style.highlight_max(subset=['PointsEarned'], color='#90EE90'))
        
        st.subheader("Publish Changes")
        commit_message = st.text_input("Commit message", 
                                     value="Update gameweek standings via Admin Portal")
        
        if st.button("🚀 Publish to GitHub"):
            with st.spinner("Updating repository..."):
                if update_github_file(content):
                    st.balloons()
                    st.success("🎉 Successfully updated gameweek data!")
                    st.markdown(f"""
                    **Next Steps:**
                    1. Changes will be live within 1-2 minutes
                    2. [View commit on GitHub](https://github.com/{REPO_OWNER}/{REPO_NAME}/commits/{BRANCH})
                    """)

# Setup Instructions
with st.expander("⚙️ Configuration Guide", expanded=False):
    st.markdown("""
    **1. GitHub Token Setup:**
    1. Go to [GitHub Token Settings](https://github.com/settings/tokens)
    2. Generate new token with these scopes:
       - `repo` (Full control of private repositories)
    3. Add to `.streamlit/secrets.toml`:
       ```toml
       GITHUB_TOKEN = "ghp_your_token_here"
       ADMIN_PASSWORD = "your_secure_password"
       ```

    **2. CSV Requirements:**
    ```csv
    Gameweek,Date,Team,Position,PointsEarned
    1,2024-01-01,Team Security,1,30
    1,2024-01-01,Team Speed,2,25
    ```

    **3. Repository Requirements:**
    - Must contain `gameweeks.csv` in root directory
    - Token owner must have write access
    """)

st.caption("⚠️ All changes are permanent. Verify data before publishing.")
