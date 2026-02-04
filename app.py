import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS # التغيير هنا لضمان السرعة
from datetime import datetime

# دالة بسيطة للبحث لتجنب أخطاء المكتبات المعقدة
def simple_search(query):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=3)]
        return str(results)

# 1. إعدادات الصفحة
st.set_page_config(page_title="Jo Ai - الوكيل الأردني", page_icon="🇯🇴", layout="centered")

# 2. تصميم الواجهة (CSS)
st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; }
    .chat-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); min-height: 400px; }
    .header-container { text-align: center; color: white; padding: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-container"><h1>🇯🇴 Jo Ai</h1><p>وكيلك الذكي المتصل بالإنترنت</p></div>', unsafe_allow_html=True)

# 3. إعداد الأدوات والمفتاح (الجزء الذي سألت عنه)
search_tool = DuckDuckGoSearchRun() # تعريف الأداة خارج الـ try

if "GOOGLE_API_KEY" in st.secrets:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"⚠️ خطأ في تشغيل Gemini: {str(e)}")
else:
    st.warning("⚠️ يرجى التأكد من إضافة GOOGLE_API_KEY في إعدادات Secrets")

# 4. سجل المحادثة والواجهة
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_box = st.container()
with chat_box:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role = "👤 أنت" if msg["role"] == "user" else "🤖 Jo Ai"
        st.write(f"**{role}:** {msg['content']}")
    st.markdown('</div>', unsafe_allow_html=True)

user_input = st.text_input("", placeholder="اكتب سؤالك هنا...", key="input", label_visibility="collapsed")
submit = st.button("إرسال")

if submit and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("⏳ جاري البحث والتفكير..."):
        try:
            results = search_tool.run(user_input)
            prompt = f"أنت Jo Ai، وكيل أردني. المستخدم طلب: {user_input}\nنتائج البحث: {results}\nأجب بأسلوب أردني وودود."
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
