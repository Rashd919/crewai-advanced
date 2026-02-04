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
    .chat-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); min-height: 400px; color: black; }
    .header-container { text-align: center; color: white; padding: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-container"><h1>🇯🇴 Jo Ai</h1><p>وكيلك الذكي الأردني</p></div>', unsafe_allow_html=True)

# 3. إعداد Gemini
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"خطأ في تشغيل Gemini: {str(e)}")
else:
    st.warning("⚠️ ضيف GOOGLE_API_KEY في الـ Secrets عشان أقدر أشتغل")

# 4. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    role = "👤 أنت" if msg["role"] == "user" else "🤖 Jo Ai"
    st.write(f"**{role}:** {msg['content']}")

# 5. منطقة الإدخال والبحث
user_input = st.chat_input("اسألني أي شيء...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("⏳ خليني أشوفلك..."):
        try:
            # البحث في الإنترنت بطريقة مباشرة وسريعة
            search_results = ""
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(user_input, max_results=3)]
                search_results = str(results)
            
            # صياغة الرد
            prompt = f"أنت Jo Ai، وكيل أردني شهم. المستخدم طلب: {user_input}\nمعلومات البحث: {search_results}\nأجب بلهجة أردنية لطيفة وواضحة."
            response = model.generate_content(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")

# الفوتر
st.markdown(f"<div style='text-align:center; color:white; font-size:12px; margin-top:50px;'>© {datetime.now().year} Jo Ai - أجدع وكيل ذكي</div>", unsafe_allow_html=True)
