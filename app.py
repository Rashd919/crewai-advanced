import streamlit as st
import google.generativeai as genai
import requests
import base64

# --- 1. الأساسيات المحرمة (Core Essentials) ---
st.set_page_config(page_title="الرعد: السيادة المتطورة", layout="wide")

# استدعاء المفاتيح
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    """دالة التطور الذاتي - قلب الرعد النابض"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            clean_code = new_code.strip().replace("```python", "").replace("```", "")
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "تحديث ذاتي آمن", "content": content, "sha": sha}
            requests.put(url, json=data, headers=headers)
            return True
    except: pass
    return False

# --- 2. تشغيل العقل الذكي ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: مبرمج نفسه الذكي")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أصدر أمر التطوير..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            if any(k in user_input for k in ["برمج", "عدل", "تحديث", "غير"]):
                with st.spinner("الرعد يحلل الطلب ويحافظ على ثبات النظام..."):
                    # هنا "الخلطة": بنعطيه الكود الحالي وبنقول له عدل عليه بس حافظ على الدوال
                    current_code = open(__file__).read() if "__file__" in locals() else ""
                    prompt = f"""
                    You are 'Thunder AI'. Your task is to evolve your code based on: '{user_input}'.
                    STRICT RULES FOR EVOLUTION:
                    1. Keep the 'update_self' function EXACTLY as it is.
                    2. Keep the secrets retrieval (api_key, github_token, repo_name) EXACTLY as they are.
                    3. Do not change the 'st.chat_input' logic.
                    4. Only enhance the UI, add features, or improve responses.
                    5. Output the FULL NEW app.py code.
                    """
                    response = model.generate_content(prompt)
                    if update_self(response.text):
                        st.success("⚡ تم التطوير مع الحفاظ على الأساسيات!")
                    else:
                        st.error("⚠️ عائق تقني في الوصول للمستودع.")
            else:
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
