import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Jo Ai - النسخة 2.0 الأحدث", page_icon="🚀", layout="centered")

# تصميم الواجهة الأنيق
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); min-height: 100vh; }
    .stChatMessage { border-radius: 15px; margin-bottom: 15px; background: rgba(255, 255, 255, 0.1); color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white;"><h1>🚀 جو آي - Gemini 2.0</h1><p>أنت الآن تستخدم أسرع وأحدث ذكاء اصطناعي من قوقل</p></div>', unsafe_allow_html=True)

# 2. إعداد محرك Gemini 2.0 Flash
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استدعاء النسخة 2.0 التجريبية الأحدث
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
    except Exception as e:
        st.error(f"خطأ في تشغيل المحرك الجديد: {str(e)}")
else:
    st.warning("⚠️ ضيف المفتاح في Secrets")

# 3. السجل والدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("سولف مع Gemini 2.0 يا نشمي...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("⏳ النسخة 2.0 عم بتفكر بذكاء..."):
        try:
            # بحث سريع لدعم الرد
            search_context = ""
            try:
                with DDGS() as ddgs:
                    search_context = str([r for r in ddgs.text(user_input, max_results=2)])
            except:
                pass

            prompt = f"أنت Jo Ai الإصدار 2.0. رد بلهجة أردنية ذكية جداً ومختصرة على: {user_input}. معلومات: {search_context}"
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error("⚠️ النسخة 2.0 جديدة جداً، إذا ما ردت انتظر ثواني وجرب مرة ثانية.")
