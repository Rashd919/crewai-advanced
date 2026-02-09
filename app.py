import streamlit as st
import google.generativeai as genai
import requests
import base64
import re
from datetime import datetime

# --- 1. إعدادات المحلل الاستراتيجي ---
st.set_page_config(page_title="الرعد: المحلل الاستراتيجي", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: #ffffff; }
    .stChatFloatingInputContainer { background-color: #0d1117 !important; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #00FFCC; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# جلب المفاتيح
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_file_on_github(file_path, content, message):
    """دالة عامة لتحديث أي ملف على GitHub (للكود أو للذاكرة)"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        sha = res.json().get('sha') if res.status_code == 200 else None
        
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        data = {"message": message, "content": encoded_content}
        if sha: data["sha"] = sha
        
        requests.put(url, json=data, headers=headers)
        return True
    except: return False

# --- 2. تفعيل الذاكرة الطويلة ---
def save_chat_to_github(history):
    chat_text = ""
    for msg in history:
        chat_text += f"{msg['role']}: {msg['content']}\n"
    update_file_on_github("chat_history.txt", chat_text, "Update Chat Memory")

# --- 3. تشغيل العقل ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: المحلل الاستراتيجي السيادي")
    
    # زر النصيحة الأمنية اليومية
    if st.sidebar.button("🛡️ نصيحة أمنية سيادية"):
        advice_prompt = "أعطني نصيحة أمن سيبراني قصيرة واحترافية باللهجة الأردنية."
        advice = model.generate_content(advice_prompt).text
        st.sidebar.info(advice)

    if "history" not in st.session_state:
        # محاولة تحميل الذاكرة لو أردت (تحتاج دالة get)
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أصدر أمرك للمحلل الاستراتيجي..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            if any(k in user_input for k in ["عدل", "برمج", "تحديث"]):
                with st.spinner("جاري التطوير الاستراتيجي..."):
                    prompt = f"عدل كود app.py بناءً على: {user_input}. حافظ على update_file_on_github وGemini."
                    response = model.generate_content(prompt)
                    # تنظيف الكود قبل الرفع
                    code_match = re.search(r'import[\s\S]*', response.text)
                    clean_code = code_match.group(0) if code_match else response.text
                    clean_code = clean_code.replace("```python", "").replace("```", "").strip()
                    
                    if update_file_on_github("app.py", clean_code, "Self-Evolve"):
                        st.success("⚡ تم التطور استراتيجياً!")
                    else: st.error("فشل التحديث.")
            else:
                response = model.generate_content(f"أنت محلل استراتيجي أردني خبير، رد على: {user_input}")
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
                # حفظ الذاكرة بعد كل رد
                save_chat_to_github(st.session_state.history)
