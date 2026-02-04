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
    .chat-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); color: black; }
    .header-container { text-align: center; color: white; padding: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-container"><h1>🇯🇴 Jo Ai</h1><p>وكيلك الذكي الأردني المستقر</p></div>', unsafe_allow_html=True)

# 3. إعداد Gemini (تم التحويل إلى 1.5 المستقر)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام النسخة المستقرة لتجنب خطأ الـ Quota
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"خطأ في تشغيل Gemini: {str(e)}")
else:
    st.warning("⚠️ ضيف GOOGLE_API_KEY في الـ Secrets")

# 4. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for msg in st.session_state.messages:
    role_icon = "👤" if msg["role"] == "user" else "🤖"
    st.markdown(f"**{role_icon}:** {msg['content']}")

# 5. منطقة الإدخال
user_input = st.chat_input("اسألني أي شيء يا شهم...")

if user_input:
    # إضافة رسالة المستخدم للسجل فوراً
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("⏳ خليني أشوفلك وأرد عليك..."):
        try:
            # البحث في الإنترنت
            search_data = ""
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(user_input, max_results=3)]
                search_data = str(results)
            
            # صياغة الرد باللهجة الأردنية
            prompt = f"""
            أنت Jo Ai، وكيل ذكي من الأردن. 
            المستخدم سأل: {user_input}
            نتائج البحث: {search_data}
            رد عليه بلهجة أردنية ودودة، خليك "نشمي" وساعده بكل أمانة.
            """
            
            response = model.generate_content(prompt)
            reply_text = response.text
            
            # إضافة رد الوكيل للسجل
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            st.rerun()
            
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ جوجل بتقول شوي شوي! انتظر ثواني وجرب مرة ثانية (هذا ضغط على السيرفر).")
            else:
                st.error(f"حدث خطأ: {str(e)}")

# الفوتر
st.markdown(f"<div style='text-align:center; color:white; font-size:12px; margin-top:50px;'>© {datetime.now().year} Jo Ai - أجدع وكيل ذكي</div>", unsafe_allow_html=True)
