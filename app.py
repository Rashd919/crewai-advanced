
import streamlit as st
from openai import OpenAI

# --- Configuration for self-update ---
MODEL_FOR_UPDATES = "gpt-4o"

UPDATE_SELF_PROMPT = """You are a self-updating Streamlit application named 'Thunder AI'.
Your task is to rewrite your entire 'app.py' code based on user requests.
You must output ONLY the complete, valid Python code for 'app.py'.
DO NOT include any conversational text or explanations outside of valid Python comments or string literals.
Ensure the generated code is fully functional and follows best practices for Streamlit applications.
Preserve existing functionality, especially:
1. Streamlit imports and basic structure.
2. The logic for handling 'st.secrets["OPENAI_API_KEY"]'.
3. The `update_self` function itself (its signature and core purpose, though its internal prompt might evolve).
4. Streamlit's chat input (`st.chat_input`) and message display (`st.chat_message`) pattern.
5. Any custom CSS added by previous updates should be maintained or intelligently modified.
6. Remember to include the `apply_custom_css` function call at the beginning of the app.

When updating, consider the following:
- Maintain readability and proper Python syntax.
- If the user asks for a background change, use `st.markdown` with `<style>` tags to inject CSS into the `body`.
- If changing the background, ensure all text (especially chat messages and input fields) remains clearly visible and readable against the new background. This usually means adjusting text colors and potentially adding semi-transparent backgrounds to components like chat messages.
- If the request is for "يا رعد، غير الخلفية بس حافظ على ظهور صندوق الكتابة بوضوح" (Oh Thunder, change the background but keep the text input box clearly visible), translate this into concrete CSS changes for the background and text/input clarity.
- Do not add extraneous features unless explicitly requested.
- Ensure the output is a complete and runnable `app.py` file.
- The `client` object should be instantiated with `st.secrets["OPENAI_API_KEY"]`.
- The `MODEL_FOR_UPDATES` should be set to a capable model like "gpt-4o".
"""

# --- Secrets and API Key Handling ---
if "openai_api_key" not in st.session_state:
    if "OPENAI_API_KEY" in st.secrets:
        st.session_state.openai_api_key = st.secrets["OPENAI_API_KEY"]
    else:
        st.error("OPENAI_API_KEY not found in st.secrets. Please add it to your Streamlit secrets.")
        st.stop() # Stop the app if no API key

client = OpenAI(api_key=st.session_state.openai_api_key)

# --- update_self function ---
def update_self(user_prompt: str, current_code: str) -> str:
    """
    Function to enable the AI to modify its own source code.

    Args:
        user_prompt (str): The specific request from the user for the update.
        current_code (str): The full current source code of the app.

    Returns:
        str: The new, modified source code.
    """
    st.info("Thunder AI is analyzing the update request and its current code...")
    messages = [
        {"role": "system", "content": UPDATE_SELF_PROMPT},
        {"role": "user", "content": f"Here is the current code:\n