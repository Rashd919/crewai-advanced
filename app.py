import streamlit as st
import os

# --- Secret Management (as per rule 3) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.warning("OPENAI_API_KEY not found in environment variables. Functionality requiring it will be limited.")

# --- Self-Update Logic (as per rule 3) ---
def update_self(new_code):
    try:
        with open(__file__, "w") as f:
            f.write(new_code)
        st.success("Code updated successfully! Please refresh the app.")
    except Exception as e:
        st.error(f"Error updating code: {e}")

# --- Streamlit UI ---
st.set_page_config(page_title="Thunder AI Chat", layout="centered")

# Custom CSS for ChatGPT-like appearance
st.markdown("""
<style>
    /* General styling for the chat container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 700px; /* Limits width of chat content for a focused experience */
    }

    /* Hide Streamlit's default header and footer */
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* Override Streamlit's default background colors for chat messages */
    /* Target the actual message bubble div within stChatMessage */
    div.stChatMessage[data-testid="stChatMessage"]:has(> div:nth-child(1) > div > div > img[alt="⚡"]) > div:nth-child(2) > div {
        background-color: #f0f0f0; /* Light grey for Thunder AI's messages */
        border-radius: 12px 2px 12px 12px; /* Smoothed corners, slightly different near avatar */
    }
    div.stChatMessage[data-testid="stChatMessage"]:has(> div:nth-child(1) > div > div > img[alt="👤"]) > div:nth-child(2) > div {
        background-color: #e0f7fa; /* Light blue for user's messages */
        border-radius: 2px 12px 12px 12px; /* Smoothed corners, slightly different near avatar */
    }

    /* Style for the chat input container */
    .stChatInputContainer {
        border-top: 1px solid #eee;
        padding-top: 10px;
        background-color: white; /* Ensures clean background for the input area */
        position: sticky; /* Keeps the input at the bottom */
        bottom: 0;
        z-index: 1000;
    }
    .stChatInputContainer input {
        border-radius: 20px;
        padding: 10px 15px;
        border: 1px solid #ccc;
    }
</style>
""", unsafe_allow_html=True)


st.title("⚡ Thunder AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! I am Thunder AI. How can I assist you today?"})

# Display chat messages from history
for message in st.session_state.messages:
    # Use st.chat_message for ChatGPT-like bubbles with distinct avatars
    avatar = "⚡" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# User input at the bottom of the chat interface
if prompt := st.chat_input("Ask Thunder AI..."):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Simulate Thunder AI's response
    with st.chat_message("assistant", avatar="⚡"):
        # Placeholder for actual LLM call (e.g., using OPENAI_API_KEY)
        response = f"I received your message: \"{prompt}\". I'm still evolving, but I'm ready to learn!"
        st.markdown(response)
    # Add Thunder AI's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # The update_self function is defined as per rules, but not called here
    # as this code itself is the result of the requested evolution.