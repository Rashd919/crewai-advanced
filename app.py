import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
from datetime import datetime

# 1. إعدادات الصفحة والواجهة الاحترافية
st.set_page_config(page_title="Jo Ai - النسخة المستقرة", page_icon="🇯🇴", layout="centered")

st.markdown("""
<style>
    * { direction: rtl; text-align: right; }
    .stApp { background: #1a1a2e; color: white; }
    .stChatMessage { background: #16213e; border-radius: 10px; border: 1px solid #0f3460; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center;"><h1>🇯🇴 جو آي - النشمي</h1><p>نسخة مستقرة وسريعة جداً</p></div>', unsafe_allow_html=True)

# 2. إعداد الاتصال المضمون
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # هاي النسخة هي الأثبت حالياً وما بتعطي خطأ ضغط السيرفر بسهولة
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        st.error("مشكلة في الاتصال، تأكد من المفتاح.")
else:
    st.warning("⚠️ المفتاح ناقص في Secrets")

# 3. الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("سولف معي يا نشمي...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("⏳ لحظة يا غالي..."):
        try:
            # نظام بحث قوي
            search_info = ""
            try:
                with DDGS() as ddgs:
                    search_info = str([r for r in ddgs.text(user_input, max_results=2)])
            except: pass

            prompt = f"أنت Jo Ai، وكيل أردني فزعة. جاوب بلهجة أردنية أصيلة. السؤال: {user_input}\nمعلومات: {search_info}"
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error("استنى 10 ثواني وجرب مرة ثانية، السيرفر عم يصحصح.")
