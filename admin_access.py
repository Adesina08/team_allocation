# admin_uploader.py
import streamlit as st
import requests
import base64
import pandas as pd
from io import StringIO
import traceback

# Configuration - Update these with your details
REPO_OWNER = "Adesina08"
REPO_NAME = "team_allocation"
FILE_PATH = "gameweeks.csv"
BRANCH = "main"  # Change if using different branch

# Authentication Setup
def check_password():
    """Password authentication with session state"""
    if 'authenticated' not in st.session_state:
        st.title("Admin Authentication")
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Authenticate"):
            if password == st.secrets.get("ADMIN_PASSWORD", ""):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
                st.stop()
        else:
            st.stop()
    return True

if not check_password():
    st.stop()

# GitHub Configuration
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except KeyError:
    st.error("❌ Missing GitHub token in secrets")
    st.stop()

# Debug Info
st.sidebar.markdown("### 🔍 Connection Info")
st.sidebar.write(f"Repository: {REPO_OWNER}/{REPO_NAME}")
st.sidebar.write(f"Branch: {BRANCH}")
st.sidebar.write(f"File: {FILE_PATH}")

def test_github_connection():
    """Test GitHub API connection"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            st.sidebar.success("✅ Valid GitHub connection")
            return True
        else:
            st.sidebar.error(f"❌ Connection failed: {response.status_code}")
            return False
    except Exception as e:
        st.sidebar.error(f"🚫 Connection error: {str(e)}")
        return False

if not test_github_connection():
    st.stop()

def validate_csv(content):
    """Validate CSV structure and data"""
    try:
        df = pd.read_csv(StringIO(content))
        
        # Check required columns
        required_columns = ['Gameweek', 'Date', 'Team', 'Position', 'PointsEarned']
        if not all(col in df.columns for col in required_columns):
            st.error(f"Missing required columns: {', '.join(required_columns)}")
            return False
            
        # Validate data types
        if not pd.api.types.is_integer_dtype(df['Gameweek']):
            st.error("Gameweek must be integers")
            return False
            
        if not pd.api.types.is_numeric_dtype(df['Position']):
            st.error("Position must be numbers (1-4)")
            return False
            
        # Check position values
        if not df['Position'].between(1, 4).all():
            st.error("Positions must be between 1 and 4")
            return False
            
        return True
        
    except Exception as e:
        st.error(f"📛 CSV validation failed: {str(e)}")
        return False

def update_github_file(content):
    """Update file on GitHub with enhanced error handling"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # Get existing file details
        response = requests.get(url, headers=headers, params={"ref": BRANCH})
        response.raise_for_status()
        file_data = response.json()
        sha = file_data.get("sha")
        
        # Encode new content
        encoded_content = base64.b64encode(content.encode()).decode()
        
        # Prepare update payload
        payload = {
            "message": "Update gameweek data via Admin Portal",
            "content": encoded_content,
            "sha": sha,
            "branch": BRANCH
        }

        # Push changes
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        return True
        
    except requests.exceptions.HTTPError as e:
        error_msg = e.response.json().get("message", "Unknown error")
        st.error(f"🚨 GitHub API Error: {error_msg}")
        st.error(f"Detail: {e.response.text}")
    except Exception as e:
        st.error(f"💥 Unexpected error: {str(e)}")
        st.code(traceback.format_exc())
    return False

# Main App Interface
st.title("🎮 Gameweek Data Admin Portal")
st.write("Securely update gameweek standings in GitHub repository")

uploaded_file = st.file_uploader("Upload CSV file", type="csv", 
                               help="Must contain Gameweek, Date, Team, Position, PointsEarned columns")

if uploaded_file:
    content = uploaded_file.getvalue().decode()
    
    if validate_csv(content):
        st.success("✅ CSV validation passed!")
        
        st.subheader("Data Preview")
        df = pd.read_csv(StringIO(content))
        st.dataframe(df)
        
        st.subheader("Publish Changes")
        commit_message = st.text_input("Commit message", 
                                     value="Update gameweek standings via Admin Portal")
        
        if st.button("🚀 Publish to GitHub"):
            with st.spinner("🔄 Updating repository..."):
                if update_github_file(content):
                    st.balloons()
                    st.success("🎉 Successfully updated gameweek data!")
                    st.markdown(f"""
                        **Next Steps:**
                        1. Changes will propagate within 1-2 minutes
                        2. [View on GitHub](https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/{BRANCH}/{FILE_PATH})
                    """)

# Setup Instructions
with st.expander("🔧 Configuration Guide", expanded=False):
    st.markdown("""
    **1. GitHub Token Setup:**
    1. Go to [GitHub Token Settings](https://github.com/settings/tokens)
    2. Generate new token with `repo` scope
    3. Copy token into `.streamlit/secrets.toml`:
        ```toml
        GITHUB_TOKEN = "your_token_here"
        ADMIN_PASSWORD = "your_secure_password"
        ```

    **2. CSV Requirements:**
    - Required columns: `Gameweek, Date, Team, Position, PointsEarned`
    - Gameweek: Integer
    - Position: 1-4
    - Teams must match existing names
    """)

st.caption("⚠️ All changes are permanent. Double-check data before publishing.")
