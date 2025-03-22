# admin_uploader.py
import streamlit as st
import requests
import base64
import pandas as pd
from io import StringIO

# Configuration - Update these with your actual details
REPO_OWNER = "your-github-username"  # Replace with your GitHub username
REPO_NAME = "your-repo-name"         # Replace with your repository name
FILE_PATH = "gameweeks.csv"          # Path to your CSV file in the repo

# Authentication
def check_password():
    if 'authenticated' not in st.session_state:
        password = st.text_input("Admin Password", type="password")
        if password:
            if password == st.secrets["ADMIN_PASSWORD"]:
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

# Retrieve GitHub token from secrets
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
except KeyError:
    st.error("Missing GitHub token in secrets")
    st.stop()

def validate_csv(content):
    """Validate CSV structure"""
    try:
        df = pd.read_csv(StringIO(content))
        required_columns = ['Gameweek', 'Date', 'Team', 'Position', 'PointsEarned']
        if not all(col in df.columns for col in required_columns):
            st.error(f"Missing required columns: {', '.join(required_columns)}")
            return False
        return True
    except Exception as e:
        st.error(f"Invalid CSV format: {str(e)}")
        return False

def update_github_file(content):
    """Update file on GitHub with proper error handling"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # Get existing file SHA
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        sha = response.json().get("sha")
        
        # Prepare update
        encoded_content = base64.b64encode(content.encode()).decode()
        payload = {
            "message": "Update gameweek data via Admin Portal",
            "content": encoded_content,
            "sha": sha
        }

        # Push changes
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"GitHub API Error: {e.response.json().get('message', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error updating file: {str(e)}")
    return False

# Main app interface
st.title("Gameweek Data Admin Portal")
st.write("### Secure CSV Upload to GitHub Repository")

uploaded_file = st.file_uploader("Upload new gameweek data (CSV)", type="csv")

if uploaded_file:
    content = uploaded_file.getvalue().decode()
    
    if validate_csv(content):
        st.success("CSV validation passed!")
        st.write("Preview of new data:")
        st.dataframe(pd.read_csv(StringIO(content)))
        
        if st.button("🚀 Publish to GitHub"):
            with st.spinner("Updating repository..."):
                if update_github_file(content):
                    st.balloons()
                    st.success("Successfully updated gameweek data!")
                    st.markdown(f"""
                        **Next Steps:**
                        1. Changes will be visible in the main app shortly
                        2. [View on GitHub](https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/{FILE_PATH})
                    """)

# Add setup instructions
with st.expander("ℹ️ Configuration Guide"):
    st.markdown("""
    **1. Repository Setup:**
    - Ensure your repository contains the `gameweeks.csv` file
    - File format must include these columns:
        - Gameweek (integer)
        - Date (YYYY-MM-DD)
        - Team (exact team names)
        - Position (1-4)
        - PointsEarned (integer)

    **2. Required Permissions:**
    - GitHub token must have `repo` scope
    - [Create token](https://github.com/settings/tokens/new?scopes=repo)
    """)

st.caption("Note: All changes are audited and permanent. Double-check before publishing.")
