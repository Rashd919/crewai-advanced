import streamlit as st
import google.generativeai as genai
import requests
import base64

# 1. إعداد الواجهة السيادية الثابتة
st.set_page_config(page_title="الرعد: السيادة الرقمية", layout="wide")

# تنسيق CSS لضمان بقاء الواجهة احترافية وصندوق الكتابة شغال
st.markdown("""
    <style>
    .stChatFloatingInputContainer { background-color: rgba(10, 10, 10, 0.9) !important; bottom: 20px !important; }
    input { color: #00FFCC !important; background-color: #1A1A1A !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. جلب المفاتيح
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    """دالة التطور الذاتي - ممنوع حذفها يا رعد"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            clean_code = new_code.strip()
            if "```python" in clean_code:
                clean_code = clean_code.split("```python")[1].split("```")[0]
            elif "```" in clean_code:
                clean_code = clean_code.split("```")[1].split("```")[0]
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "Thunder AI: Critical Core Update", "content": content, "sha": sha}
            requests.put(url, json=data, headers=headers)
            return True
    except: pass
    return False

# 3. تشغيل العقل (Gemini)
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: وكيل الأردن السيادي")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    # عرض المحادثة
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # صندوق الكتابة الحقيقي (الذي يربط المستخدم بالذكاء الاصطناعي)
    if user_input := st.chat_input("أصدر أمرك للرعد..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            # إذا طلب المستخدم تطوير الكود
            if any(k in user_input for k in ["برمج", "عدل", "تحديث", "غير"]):
                with st.spinner("جاري إعادة هندسة الكود..."):
                    # تعليمات صارمة للرعد بعدم حذف الدوال الأساسية
                    prompt = f"Rewrite the current app.py to: {user_input}. IMPORTANT: You MUST keep the 'update_self' function and the 'st.chat_input' logic exactly as they are. Output ONLY code."
                    response = model.generate_content(prompt)
                    if update_self(response.text):
                        st.success("⚡ تم التطوير بنجاح! انتظر التحديث.")
                    else: st.error("فشل في الوصول لـ GitHub.")
            else:
                # رد حواري عادي
                response = model.generate_content(user_input)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
