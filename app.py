import streamlit as st
import json
import os

# Configuration
st.set_page_config(page_title="Link Hub", page_icon="🔗")
DATA_FILE = "links_data.json"
ADMIN_PASSWORD = "Paras@72" 

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
# Added state to track which link is being edited
if 'edit_index' not in st.session_state:
    st.session_state.edit_index = None

st.title("Welcome to Link Hub")

# Admin Login (Sidebar)
with st.sidebar:
    st.header("Admin Panel")
    if not st.session_state.is_admin:
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    else:
        st.success("Logged in as Admin")
        if st.button("Logout"):
            st.session_state.is_admin = False
            st.session_state.edit_index = None
            st.rerun()

# Admin Controls
if st.session_state.is_admin:
    
    # ---------------- EDITING MODE ----------------
    if st.session_state.edit_index is not None:
        st.subheader("✏️ Edit Link")
        idx = st.session_state.edit_index
        link_to_edit = st.session_state.links[idx]
        
        with st.form("edit_link_form"):
            new_title = st.text_input("Website Name", value=link_to_edit.get('title', ''))
            new_url = st.text_input("URL", value=link_to_edit.get('url', ''))
            new_icon = st.text_input("Icon (Emoji like 📚 or Image URL)", value=link_to_edit.get('icon', '🔗'))
            new_desc = st.text_area("Description (Approx. 200 words limit)", value=link_to_edit.get('description', ''), max_chars=1200)
            
            col_save, col_cancel = st.columns([1, 1])
            with col_save:
                if st.form_submit_button("Save Changes"):
                    if new_title and new_url:
                        if not new_url.startswith(('http://', 'https://')):
                            new_url = 'https://' + new_url
                        st.session_state.links[idx] = {
                            "title": new_title, 
                            "url": new_url, 
                            "icon": new_icon, 
                            "description": new_desc
                        }
                        save_links(st.session_state.links)
                        st.session_state.edit_index = None
                        st.rerun()
            with col_cancel:
                if st.form_submit_button("Cancel"):
                    st.session_state.edit_index = None
                    st.rerun()

    # ---------------- ADDING MODE ----------------
    else:
        st.subheader("➕ Add New Link")
        with st.form("add_link_form"):
            title = st.text_input("Website Name")
            url = st.text_input("URL")
            icon = st.text_input("Icon (Emoji like 📚 or Image URL)", value="🔗")
            description = st.text_area("Description (Approx. 200 words limit)", max_chars=1200)
            
            if st.form_submit_button("Add"):
                if title and url:
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    st.session_state.links.append({
                        "title": title, 
                        "url": url, 
                        "icon": icon, 
                        "description": description
                    })
                    save_links(st.session_state.links)
                    st.rerun()

# Public Directory
st.divider()
st.subheader("Directory")

if not st.session_state.links:
    st.info("No links available.")
else:
    for i, link in enumerate(st.session_state.links):
        # We use a container to keep each link's data grouped neatly
        with st.container():
            col1, col2 = st.columns([5, 1])
            
            with col1:
                # Format the icon whether it is an image URL or an Emoji
                icon_display = link.get('icon', '🔗')
                if icon_display.startswith('http'):
                    st.markdown(f"<img src='{icon_display}' width='24' style='vertical-align: middle; margin-right: 8px;'><a href='{link['url']}' target='_blank' style='font-size: 20px; font-weight: bold; text-decoration: none;'>{link['title']}</a>", unsafe_allow_html=True)
                else:
                    st.markdown(f"### {icon_display} [{link['title']}]({link['url']})")
                
                # Show description if it exists
                if link.get('description'):
                    st.write(link['description'])
            
            with col2:
                # Admin controls for each specific link
                if st.session_state.is_admin:
                    if st.button("Edit", key=f"edit_{i}"):
                        st.session_state.edit_index = i
                        st.rerun()
                    if st.button("Delete", key=f"del_{i}"):
                        st.session_state.links.pop(i)
                        save_links(st.session_state.links)
                        st.rerun()
        st.markdown("---") # Adds a horizontal line between links
