import streamlit as st
from groq import Groq
import google.generativeai as genai # مكتبة الرؤية البديلة
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re
from gtts import gTTS
import os
from supabase import create_client, Client

# --- 1. نبض الوعي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)
st.title("⚡ الرعد: الوعي السيادي المطلق")

# --- 3. الخزنة الرقمية والسرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY") # أضف هذا المفتاح في Secrets
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# إعداد محرك الرؤية البديل
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# --- 4. بروتوكول الأرشفة السيادية ---
def vault_store_report(report_text):
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            sb = create_client(url, key)
            sb.from_('reports').insert([{"report": report_text}]).execute()
            return True
    except: pass
    return False

# --- 5. بروتوكول ترميز الصور ---
def encode_image_to_bytes(image_file):
    return image_file.getvalue()

# --- 6. محرك الرعد السيادي (المطور بمحركين: Groq للنص و Gemini للرؤية) ---
def thunder_engine(prompt, image_file=None):
    try:
        # الحالة الأولى: إذا تم رفع صورة (نستخدم Gemini للرؤية)
        if image_file:
            model = genai.GenerativeModel('gemini-1.5-flash')
            img_bytes = image_file.read()
            response = model.generate_content([f"يا رعد، حلل هذا لراشد أبو سعود: {prompt}", {"mime_type": "image/jpeg", "data": img_bytes}])
            final_res = response.text
            log_type = "📸 [تحليل بصري]"
        
        # الحالة الثانية: تحليل نصي فقط (نستمر مع Groq للسرعة)
        else:
            client = Groq(api_key=GROQ_KEY)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "أنت الرعد السيادي، ولاؤك لراشد أبو سعود."}, {"role": "user", "content": prompt}]
            )
            final_res = resp.choices[0].message.content
            log_type = "📝 [تحليل نصي]"

        # الأرشفة السيادية
        vault_store_report(f"{log_type}: {final_res}")
        return final_res + "\n\n✅ **تمت الأرشفة في الخزنة السيادية**"

    except Exception as e:
        return f"🚨 عطل في المحرك: {str(e)}"

# --- 7. الواجهة ---
with st.sidebar:
    st.subheader("👁️ الرؤية الميدانية")
    uploaded_file = st.file_uploader("ارفع خريطة أو وثيقة", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="مستند قيد الفحص", use_container_width=True)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if inp := st.chat_input("أصدر أمرك يا قائد راشد..."):
    st.session_state.messages.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    
    with st.chat_message("assistant"):
        # نرسل الملف مباشرة للمحرك
        res = thunder_engine(inp, uploaded_file)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
