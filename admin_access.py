import streamlit as st
import requests
import base64

# Configuration: Replace these with your actual repository details
REPO_OWNER = "your_username"    # GitHub username or organization owning the repository
REPO_NAME = "your_repo_name"    # Name of the repository with project files
FILE_PATH = "gameweek.csv"      # File path in the repository to update

# Password protection for the admin
password = st.text_input("Enter Password", type="password")
if password != st.secrets["ADMIN_PASSWORD"]:
    st.error("Incorrect password. Please try again.")
    st.stop()

# Retrieve the GitHub token from Streamlit secrets
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

# Function to upload or update the file in the GitHub repository
def update_file_on_github(content):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Check if the file already exists to get its SHA (for updating)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]  # File exists, get its SHA
    elif response.status_code == 404:
        sha = None  # File doesn't exist, will create it
    else:
        st.error(f"Error checking file: {response.status_code}")
        return
    
    # Encode the file content to base64 as required by GitHub API
    content_encoded = base64.b64encode(content.encode()).decode()
    
    # Prepare the API payload
    payload = {
        "message": "Updated gameweek.csv via Streamlit app",
        "content": content_encoded,
    }
    if sha:
        payload["sha"] = sha  # Include SHA for updating existing file
    
    # Send the request to update or create the file
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code in (200, 201):
        st.success("Gameweek.csv has been successfully updated in the repository!")
    else:
        st.error(f"Failed to update file: {response.json().get('message', 'Unknown error')}")

# Streamlit app interface
st.title("Gameweek CSV Uploader")
st.write("Upload your gameweeks CSV file to update it in the GitHub repository.")

# File uploader for the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded file content
    content = uploaded_file.read().decode("utf-8")
    
    # Button to trigger the upload
    if st.button("Upload to GitHub"):
        update_file_on_github(content)
