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
    .chat-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 20px; color: black; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white;"><h1>🇯🇴 Jo Ai</h1><p>وكيلك الذكي الأردني</p></div>', unsafe_allow_html=True)

# 3. إعداد Gemini (هذا السطر هو الحل لخطأ 404)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام اسم النموذج المباشر الذي تقبله جميع الإصدارات
        model = genai.GenerativeModel('gemini-1.5-flash') 
    except Exception as e:
        st.error(f"خطأ في إعداد المحرك: {str(e)}")
else:
    st.warning("⚠️ تأكد من وضع GOOGLE_API_KEY في Secrets")

# 4. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "👤 أنت" if msg["role"] == "user" else "🤖 Jo Ai"
    st.write(f"**{role}:** {msg['content']}")

# 5. منطقة الإدخال
user_input = st.chat_input("اسألني أي شيء يا نشمي...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("⏳ جاري التفكير..."):
        try:
            # بحث بسيط وسريع
            search_text = ""
            try:
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(user_input, max_results=2)]
                    search_text = str(results)
            except:
                search_text = "تعذر الاتصال بالبحث حالياً."

            # طلب الرد من Gemini
            prompt = f"أنت Jo Ai، وكيل أردني شهم. رد على: {user_input} مستعيناً بالمعلومات: {search_text}. اجعل الرد بلهجة أردنية."
            response = model.generate_content(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
