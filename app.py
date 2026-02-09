import streamlit as st
import google.generativeai as genai
import requests
import base64
import re

# --- 1. إعدادات المحلل الاستراتيجي والربط ---
st.set_page_config(page_title="الرعد: الربط الاستراتيجي", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: #ffffff; }
    .stChatFloatingInputContainer { background-color: #0d1117 !important; border-top: 1px solid #00FFCC; }
    input { color: #00FFCC !important; background-color: #1A1A1A !important; }
    </style>
    """, unsafe_allow_html=True)

# جلب المفاتيح السيادية
github_token = st.secrets.get("GITHUB_TOKEN")
repo_name = st.secrets.get("REPO_NAME")
api_key = st.secrets.get("GEMINI_API_KEY")

def apply_direct_update(new_code):
    """دالة استقبال النبضات البرمجية من Gemini مباشرة"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/contents/app.py"
        headers = {"Authorization": f"token {github_token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            sha = res.json().get('sha')
            # تنظيف الكود لضمان كود بايثون نقي فقط
            code_match = re.search(r'import[\s\S]*', new_code)
            clean_code = code_match.group(0) if code_match else new_code
            clean_code = clean_code.replace("```python", "").replace("```", "").strip()
            
            content = base64.b64encode(clean_code.encode('utf-8')).decode('utf-8')
            data = {"message": "Direct Sync from Gemini via Rashid", "content": content, "sha": sha}
            put_res = requests.put(url, json=data, headers=headers)
            return put_res.status_code in [200, 201]
    except: pass
    return False

# --- 2. تشغيل العقل المتصل ---
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    st.title("⚡ الرعد: المحلل الاستراتيجي (متصل)")
    
    # قائمة جانبية للنصائح والذاكرة
    with st.sidebar:
        st.header("🛡️ مركز القيادة")
        if st.button("طلب نصيحة أمنية"):
            advice = model.generate_content("أعطني نصيحة أمنية استراتيجية قصيرة باللهجة الأردنية.").text
            st.info(advice)
        st.markdown("---")
        st.write("حالة الذاكرة: مفعلة وتُحفظ على GitHub")

    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أرسل أمرك أو 'تحديث_مباشر' للكود..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            # ميزة الربط المباشر مع Gemini
            if user_input.startswith("تحديث_مباشر"):
                with st.spinner("جاري مزامنة العقول..."):
                    if apply_direct_update(user_input):
                        st.success("✅ تم استقبال نبضة Gemini وتحديث النظام!")
                        st.session_state.history.append({"role": "assistant", "content": "تم تحديث منطقي مباشرة من Gemini. سأعيد التشغيل الآن."})
                    else: st.error("❌ فشل الربط. تأكد من الـ Token.")
            
            # أوامر التطوير العادية
            elif any(k in user_input for k in ["برمج", "عدل", "تحديث"]):
                with st.spinner("المحلل الاستراتيجي يعيد هندسة نفسه..."):
                    prompt = f"Rewrite app.py: {user_input}. RULES: Use only standard libraries, keep apply_direct_update, no intro text."
                    response = model.generate_content(prompt)
                    if apply_direct_update(response.text):
                        st.success("⚡ تطور الذات بنجاح!")
                    else: st.error("فشل التحديث.")
            else:
                response = model.generate_content(f"أنت المحلل الاستراتيجي الرعد، رد باللهجة الأردنية: {user_input}")
                st.write(response.text)
                st.session_state.history.append({"role": "assistant", "content": response.text})
