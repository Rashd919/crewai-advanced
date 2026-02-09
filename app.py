import streamlit as st
import google.generativeai as genai
import requests
import base64

# إعداد الرعد: النسخة المستقرة للتحكم الذاتي
st.set_page_config(page_title="الرعد: التحكم الذاتي", layout="wide")

# استدعاء المفاتيح
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    """دالة التعديل الذاتي عبر GitHub API"""
    url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
    headers = {"Authorization": f"token {github_token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        sha = res.json().get('sha')
        # تنظيف الكود لضمان عدم وجود أخطاء تنسيق
        clean_code = new_code.strip().replace("```python", "").replace("```", "")
        content = base64.b64encode(clean_code.encode()).decode()
        data = {"message": "تحديث سيادي من الرعد", "content": content, "sha": sha}
        put_res = requests.put(url, json=data, headers=headers)
        return put_res.status_code in [200, 201]
    return False

if api_key:
    genai.configure(api_key=api_key)
    # استخدام الموديل الخارق اللي اكتشفناه في الفحص
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: مبرمج نفسه")
    st.info("أهلاً بك يا راشد. أنا جاهز لتطوير منطقي بناءً على أوامرك.")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_command := st.chat_input("أصدر أمر البرمجة للرعد..."):
        st.session_state.history.append({"role": "user", "content": user_command})
        with st.chat_message("user"):
            st.write(user_command)
        
        # إذا كان الأمر يتضمن تعديل برمجي
        if any(word in user_command for word in ["عدل", "برمج", "تحديث", "غير"]):
            with st.chat_message("assistant"):
                with st.spinner("الرعد يعيد صياغة كوده المصدري..."):
                    prompt = f"أنت الرعد. بناءً على هذا الطلب: '{user_command}'، اكتب كود Python كامل لملف app.py يعمل فقط بـ streamlit و google-generativeai. لا تستخدم Flask أو أي مكتبة غير موجودة. اعطني الكود الصافي فقط."
                    response = model.generate_content(prompt)
                    if update_self(response.text):
                        st.success("⚡ نجح التعديل! انتظر إعادة التشغيل التلقائي.")
                    else:
                        st.error("⚠️ فشل التحديث. تأكد من إعدادات الـ Token و Repo Name.")
        else:
            with st.chat_message("assistant"):
                response = model.generate_content(user_command)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
