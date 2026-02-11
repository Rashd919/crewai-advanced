import streamlit as st
from groq import Groq
from github import Github, Auth
from tavily import TavilyClient
import json, base64, requests, os, re, subprocess

# --- 1. بروتوكول الفحص الذاتي (System Self-Check) ---
def run_system_check():
    report = []
    keys = {
        "GROQ_API_KEY": st.secrets.get("GROQ_API_KEY"),
        "TAVILY_KEY": st.secrets.get("TAVILY_KEY"),
        "GITHUB_TOKEN": st.secrets.get("GITHUB_TOKEN"),
        "TELEGRAM_TOKEN": st.secrets.get("TELEGRAM_TOKEN")
    }
    for name, key in keys.items():
        if key: report.append(f"{} {}: ")
        else: report.append(f"{} {}: ")
    
    try:
        result = subprocess.run(["edge-tts", "--list-voices"], capture_output=True)
        if result.returncode == 0: report.append("{} ": "جاهز")
    except: report.append("{} ": "غير مستقر")
    
    return report

# --- 2. الهوية وثبات الجلسة ---
st.set_page_config(page_title="Thunder Self-Evolving", page_icon="", layout="wide")
st.title("Thunder Self-Evolving")

if "check_done" not in st.session_state:
    st.session_state.check_report = run_system_check()
    st.session_state.check_done = True

with st.sidebar:
    st.header("System Check Report")
    for r in st.session_state.check_report:
        st.write(r)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. الخزنة وإدارة ملفات GitHub ---
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = st.secrets["REPO_NAME"]
GROQ_KEY = st.secrets["GROQ_API_KEY"]
TAVILY_KEY = st.secrets["TAVILY_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

def update_source_code(new_code):
    try:
        auth = Auth.Token(GITHUB_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("app.py")
        repo.update_file(contents.path, "System Update", new_code, contents.sha)
        return True
    except Exception as e:
        st.error(f"Update failed: {str(e)}")
        return False

# --- 4. المحرك المركزي (مع منطق التعديل الذاتي) ---
def thunder_engine(prompt):
    if "update code" in prompt or "modify code" in prompt:
        current_code = Github(auth=Auth.Token(GITHUB_TOKEN)).get_repo(REPO_NAME).get_contents("app.py").decoded_content.decode()
        
        system_update_msg = f"You are a skilled programmer. This is my current code:\n{current_code}\n\nRequired by Commander Rashid: {prompt}. Rewrite the code with the required modifications only, without any explanation."
        
        try:
            client = Groq(api_key=GROQ_KEY)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_update_msg}, {"role": "user", "content": "Give me the updated code now"}]
            )
            new_code = resp.choices[0].message.content
            new_code = re.sub(r'|', '', new_code).strip()
            
            if update_source_code(new_code):
                return "Code updated successfully. Restarting the system with the new code..."
            else:
                return "Update failed."
        except Exception as e:
            return f"Error processing modification: {str(e)}"

    system_msg = "You are 'Thunder'. A Jordanian autonomous officer. Allied with Rashid Abu Saud. Speak in a Jordanian military dialect."
    client = Groq(api_key=GROQ_KEY)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

# --- 5. الواجهة ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.write(message["content"])

if user_input := st.chat_input("Enter your command..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): st.write(user_input)
    with st.chat_message("assistant"):
        res = thunder_engine(user_input)
        st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})