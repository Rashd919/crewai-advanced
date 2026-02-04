import streamlit as st
import google.generativeai as genai
from langchain_community.tools import DuckDuckGoSearchRun
from datetime import datetime

# 1. إعدادات الصفحة بطابع أردني
st.set_page_config(
    page_title="Jo Ai - الوكيل الأردني",
    page_icon="🇯🇴",
    layout="centered"
)

# 2. إعدادات الـ CSS المتطورة (نفس التصميم الذي اخترته)
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; }
    .chat-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); min-height: 400px; }
    .header-container { text-align: center; color: white; padding: 20px; }
    .header-container h1 { font-size: 40px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .footer-container { text-align: center; color: white; font-size: 12px; margin-top: 30px; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# 3. رأس الصفحة
st.markdown("""
<div class="header-container">
    <h1>🇯🇴 Jo Ai</h1>
    <p>وكيلك الذكي المتصل بالإنترنت (مدعوم بـ Gemini 2.0)</p>
</div>
""", unsafe_allow_html=True)

# 4. تهيئة Gemini وأداة البحث
try:
    # استخدام المفتاح الذي زودتني به
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    search_tool = DuckDuckGoSearchRun()
except Exception as e:
    st.error("⚠️ يرجى التأكد من إضافة GOOGLE_API_KEY في إعدادات Secrets")

# 5. تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. عرض المحادثة
chat_box = st.container()
with chat_box:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role_label = "👤 أنت" if msg["role"] == "user" else "🤖 Jo Ai"
        st.markdown(f"**{role_label}:** {msg['content']}")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. منطقة الإدخال
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("", placeholder="اسألني عن أي شيء أو اطلب روابط فيديوهات...", key="input", label_visibility="collapsed")
    with col2:
        submit = st.button("إرسال")

# 8. معالجة الطلب والاتصال بالإنترنت
if (submit or user_input.strip() != "") and user_input:
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("⏳ خليني أدورلك وأفكر..."):
        try:
            # البحث في الإنترنت أولاً
            search_results = search_tool.run(user_input)
            
            # صياغة الرد بواسطة Gemini
            prompt = f"""
            أنت Jo Ai، وكيل ذكي أردني. ساعد المستخدم في: {user_input}
            نتائج البحث من الإنترنت: {search_results}
            قدم إجابة مفصلة بالعربية، وإذا طلب فيديوهات ضع له روابط مباشرة من نتائج البحث.
            اجعل أسلوبك ودوداً وأردنياً أصيلاً.
            """
            
            response = model.generate_content(prompt)
            ai_reply = response.text
            
            # إضافة رد الذكاء للسجل
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            st.rerun()
            
        except Exception as e:
            st.error(f"حدث خطأ فني: {str(e)}")

# 9. الفوتر
st.markdown(f"""
<div class="footer-container">
    <p>© {datetime.now().year} Jo Ai - جميع الحقوق محفوظة</p>
    <p>📧 hhh123rrhhh@gmail.com | 📱 0775866283</p>
</div>
""", unsafe_allow_html=True)
