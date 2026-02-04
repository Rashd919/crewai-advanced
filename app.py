import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Jo Ai - الوكيل الأردني", page_icon="🇯🇴", layout="centered")

# 2. تصميم الواجهة (CSS)
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; }
    .chat-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 20px; margin-bottom: 20px; color: black; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white;"><h1>🇯🇴 Jo Ai</h1><p>وكيلك الذكي الأردني</p></div>', unsafe_allow_html=True)

# 3. إعداد Gemini (التعديل هنا)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام المسار الكامل للنموذج لضمان التعرف عليه
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    except Exception as e:
        st.error(f"خطأ في إعداد المحرك: {str(e)}")
else:
    st.warning("⚠️ ضيف المفتاح في Secrets")

# 4. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.write(f"**{'👤 أنت' if msg['role'] == 'user' else '🤖 Jo Ai'}:** {msg['content']}")

# 5. الإدخال
user_input = st.chat_input("اسألني أي شيء...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("⏳ جاري الرد..."):
        try:
            search_data = ""
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(user_input, max_results=2)]
                search_data = str(results)
            
            prompt = f"أنت Jo Ai، وكيل أردني. المستخدم سأل: {user_input}\nمعلومات: {search_data}\nرد بلهجة أردنية."
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
