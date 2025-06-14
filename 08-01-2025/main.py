import streamlit as st
from utils.final_agent import get_app


graph = get_app()

st.set_page_config(page_title="Fitness Agent", layout="centered")
st.title("Fitness Chat Assistant")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.chat_input("Ask your  question...")

# When the user submits a query
if user_input:
    # Show user message
    state = {"messages":[user_input],"validation_flag":False, "attempts":0,"urls":[],"final_message":""}

    st.session_state.chat_history.append(("user", user_input))
    
    # Run graph
    result = graph.invoke(state)

  
    # Extract URLs
    # Assuming result['urls'] is a list of URL strings
    urls = result.get('urls', []) # Use .get() with a default to avoid KeyError if 'urls' is missing

    # Limit to first 3 URLs
    display_urls = urls[:3] if len(urls) > 3 else urls


    hyperlink_strings = []
    for i, url_link in enumerate(display_urls):
        # Basic check to ensure it's a valid URL format for display
        if url_link.startswith("http://") or url_link.startswith("https://"):
            hyperlink_strings.append(f"[Source {i+1}]({url_link})")
        else:
            # If it's not a proper URL, just display as text or skip
            hyperlink_strings.append(url_link) # Or: f"Invalid URL: {url_link}"


    # Combine final message with formatted links
    response_text = result.get('final_message', '') # Use .get() to avoid KeyError

    if hyperlink_strings:
        response = response_text + "\n\nSources: " + ", ".join(hyperlink_strings)
    else:
        response = response_text # No URLs to append


    # Save assistant message

    # Save assistant message
    st.session_state.chat_history.append(("assistant", response))

# Display full chat history
for sender, msg in st.session_state.chat_history:
    with st.chat_message(sender):
        st.markdown(msg)
