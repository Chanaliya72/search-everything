import streamlit as st

# Page setup
st.set_page_config(page_title="Link Hub", page_icon="🔗")
st.title("Welcome to Link Hub")
st.write("Share and discover interesting websites")

# Setup a temporary place to store links while the app runs
if 'saved_links' not in st.session_state:
    st.session_state.saved_links = []

# The input form
with st.form("add_link_form", clear_on_submit=True):
    title = st.text_input("Website Name (e.g., Python Docs)")
    url = st.text_input("URL (e.g., python.org)")
    submitted = st.form_submit_button("Add to Directory")
    
    if submitted and url:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        st.session_state.saved_links.append({'title': title or url, 'url': url})
        st.success(f"Added {title or url}!")

# Display the links
st.divider()
st.subheader("Directory")

if st.session_state.saved_links:
    for link in st.session_state.saved_links:
        st.markdown(f"### 🔗 [{link['title']}]({link['url']})")
else:
    st.info("No links have been added yet.")
