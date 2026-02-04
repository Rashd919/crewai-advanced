import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
from datetime import datetime

# 1. إعدادات الصفحة الفائقة
st.set_page_config(page_title="Jo Ai 2.0 - Thinking", page_icon="🧠", layout="centered")

# تصميم واجهة احترافية داكنة (Dark Mode)
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stApp { background: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center;"><h1>🧠 جو آي 2.0 - Thinking</h1><p>أذكى نسخة ذكاء اصطناعي في العالم حالياً</p></div>', unsafe_allow_html=True)

# 2. إعداد الاتصال بـ Gemini 2.0
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام نسخة التفكير المتطور gemini-2.0-flash-thinking-exp
        model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')
    except Exception as e:
        st.error("فشل الاتصال الأولي، جاري المحاولة مرة أخرى...")
else:
    st.warning("⚠️ تأكد من وجود GOOGLE_API_KEY في Secrets")

# 3. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. التفاعل
user_input = st.chat_input("اسأل أذكى نسخة موجودة...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("⏳ النسخة 2.0 عم بتفكر بعمق..."):
        try:
            # البحث لدعم "التفكير"
            search_context = ""
            try:
                with DDGS() as ddgs:
                    search_context = str([r for r in ddgs.text(user_input, max_results=1)])
            except: pass

            prompt = f"أنت Jo Ai 2.0، تستخدم تقنية Thinking. أجب بلهجة أردنية ذكية جداً. السؤال: {user_input}\nمعلومات: {search_context}"
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # حل ذكي: إذا فشل 2.0، يحول تلقائياً لـ 1.5 لضمان الرد
            try:
                fallback_model = genai.GenerativeModel('gemini-1.5-flash')
                response = fallback_model.generate_content(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except:
                st.error("الضغط عالي جداً على سيرفرات قوقل، جرب مرة ثانية بعد 5 ثواني.")
