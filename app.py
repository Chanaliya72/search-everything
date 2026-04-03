import streamlit as st
import json
import os

# Configuration
st.set_page_config(page_title="Link Hub", page_icon="🔗")
DATA_FILE = "links_data.json"

# --- UPDATED PASSWORD ---
ADMIN_PASSWORD = "Paras@72" 
# ------------------------

# Data Management
def load_links():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_links(links):
    with open(DATA_FILE, "w") as f:
        json.dump(links, f)

# State Initialization
if 'links' not in st.session_state:
    st.session_state.links = load_links()
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

st.title("Welcome to Link Hub")

# Admin Login (Sidebar)
with st.sidebar:
    st.header("Admin Panel")
    if not st.session_state.is_admin:
        # The text_input type="password" hides the characters as they are typed
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            # This line strictly confirms the password matches 'Paras@72' exactly
            if pwd == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    else:
        st.success("Logged in as Admin")
        if st.button("Logout"):
            st.session_state.is_admin = False
            st.rerun()

# Admin Controls (Only visible if password was correct)
if st.session_state.is_admin:
    st.subheader("Add New Link")
    with st.form("add_link"):
        title = st.text_input("Website Name")
        url = st.text_input("URL")
        if st.form_submit_button("Add"):
            if title and url:
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                st.session_state.links.append({"title": title, "url": url})
                save_links(st.session_state.links)
                st.rerun()

# Public Directory (Visible to everyone)
st.divider()
st.subheader("Directory")

if not st.session_state.links:
    st.info("No links available.")
else:
    for i, link in enumerate(st.session_state.links):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"🔗 **[{link['title']}]({link['url']})**")
        with col2:
            # Only the admin sees the delete buttons
            if st.session_state.is_admin:
                if st.button("Delete", key=f"del_{i}"):
                    st.session_state.links.pop(i)
                    save_links(st.session_state.links)
                    st.rerun()
