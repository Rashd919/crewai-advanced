import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re, os, time
from supabase import create_client, Client
from datetime import datetime, timedelta

# --- 1. نبض الوعي السيادي ---
st_autorefresh(interval=10 * 1000, key="clock_refresh") # تحديث كل 10 ثوانٍ للساعة

# --- 2. الهوية البصرية ومزامنة التوقيت المحلي ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")

# تعديل التوقيت ليكون UTC+3 (توقيتك المحلي)
local_time = datetime.utcnow() + timedelta(hours=3)
now_str = local_time.strftime("%H:%M:%S")

st.markdown(f"""
    <div style="text-align: center; background-color: #1e1e1e; padding: 10px; border-radius: 10px; border: 2px solid #FF0000; box-shadow: 0px 0px 15px #FF0000;">
        <h1 style="color: #FF0000; margin: 0; font-family: 'Courier New', monospace;">⚡ {now_str} ⚡</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; }</style>", unsafe_allow_html=True)
st.title("⚡ مركز العمليات الاستخباراتية")

# --- 3. البيانات السرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"

# --- 4. بروتوكول الحقن الذكي (المحمي) ---
def update_logic(new_code_snippet):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents("app.py")
        content = base64.b64decode(file.content).decode()
        FREE_TAG = "# --- FREE_ZONE ---
import time

# حالة الطقس في عمان
weather = "☁️ غائم مع احتمال مطر خفيف"

# الساعة الرقمية
current_time = "12:16:22"

# التكامل مع FREE_ZONE
print(" FREE_ZONE ")
print("-----------")
print(f" الساعة: {current_time} | حالة الطقس: {weather}")
print("-----------")
