import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
from datetime import datetime

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="Jo Ai - الوكيل الأردني", page_icon="🇯🇴", layout="centered")

# تصميم الثيم الأردني (CSS)
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; }
    .stChatMessage { background: rgba(255, 255, 255, 0.9); border-radius: 15px; margin-bottom: 10px; color: black; }
    .stChatInput { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white;"><h1>🇯🇴 جو آي</h1><p>أهلاً بيك يا نشمي، أنا وكيلك الذكي</p></div>', unsafe_allow_html=True)

# 2. إعداد الاتصال بالـ API (استخدام النسخة المضمونة 8b)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # تم التعديل هنا لضمان الاستقرار وسرعة الرد
        model = genai.GenerativeModel('gemini-1.5-flash-8b')
    except Exception as e:
        st.error(f"⚠️ خطأ في إعداد الاتصال: {str(e)}")
else:
    st.warning("⚠️ يرجى إضافة GOOGLE_API_KEY في Secrets")

# 3. إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. منطقة الإدخال
user_input = st.chat_input("تفضل اسألني أي شيء يا نشمي...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("⏳ خليني أشوفلك..."):
        try:
            # محاولة البحث السريع
            search_context = ""
            try:
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(user_input, max_results=2)]
                    search_context = str(results)
            except:
                search_context = "سأجيب من معلوماتي الخاصة."

            # طلب الرد
            prompt = f"أنت Jo Ai، وكيل أردني شهم. رد على: {user_input} بلهجة أردنية أصيلة. معلومات مساعدة: {search_context}"
            response = model.generate_content(prompt)
            
            # عرض الرد
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error("⚠️ يبدو أن هناك ضغطاً على النظام، حاول مرة أخرى خلال ثوانٍ.")
            # تسجيل الخطأ في اللوحات الخلفية للمبرمج
            print(f"Error: {str(e)}")

# الفوتر
st.markdown(f"<div style='text-align:center; color:white; font-size:10px; margin-top:30px;'>© {datetime.now().year} Jo Ai - صنع للأردن</div>", unsafe_allow_html=True)
