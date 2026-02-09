import streamlit as st
import google.generativeai as genai
import requests
import base64

st.set_page_config(page_title="الرعد: التحكم الذاتي", layout="wide")

# استدعاء المفاتيح من الـ Secrets
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def update_self(new_code):
    """دالة تمكن الرعد من الوصول لـ GitHub وتحديث نفسه برمجياً"""
    url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
    headers = {"Authorization": f"token {github_token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        sha = res.json().get('sha')
        # تنظيف الكود الجديد من أي علامات Markdown قد يضيفها الـ AI
        clean_code = new_code.strip().replace("```python", "").replace("```", "")
        content = base64.b64encode(clean_code.encode()).decode()
        data = {"message": "تحديث سيادي ذاتي بواسطة الرعد", "content": content, "sha": sha}
        put_res = requests.put(url, json=data, headers=headers)
        return put_res.status_code in [200, 201]
    return False

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: مبرمج نفسه")
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_command := st.chat_input("أصدر أمر البرمجة للرعد..."):
        st.session_state.history.append({"role": "user", "content": user_command})
        with st.chat_message("user"):
            st.write(user_command)
        
        # تفعيل خاصية التعديل الذاتي إذا وجد كلمات مفتاحية
        if any(word in user_command for word in ["عدل نفسك", "برمج", "تحديث"]):
            with st.chat_message("assistant"):
                with st.spinner("الرعد يتصل بـ GitHub لإعادة برمجة منطقه..."):
                    prompt = f"أنت الرعد. بناءً على هذا الطلب: '{user_command}'، اكتب كود Python كامل لملف app.py. لا تشرح، فقط اعطني الكود الصافي."
                    response = model.generate_content(prompt)
                    if update_self(response.text):
                        st.success("⚡ نجحت العملية! الرعد أعاد بناء نفسه. انتظر ثواني ليتم التحديث تلقائياً.")
                    else:
                        st.error("⚠️ فشل التعديل الذاتي. تأكد من صلاحيات الـ Token.")
        else:
            # رد حواري عادي
            with st.chat_message("assistant"):
                response = model.generate_content(user_command)
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
