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
    .chat-container { background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 20px; color: black; margin-bottom: 10px; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; color:white;"><h1>🇯🇴 Jo Ai</h1><p>أهلاً بيك يا نشمي، أنا وكيلك الذكي</p></div>', unsafe_allow_html=True)

# 2. إعداد الاتصال بالـ API (حل مشكلة 404 و 429)
if "GOOGLE_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام النسخة المستقرة gemini-1.5-flash لأنها تدعم API v1beta و v1 معاً
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"⚠️ خطأ في إعداد الاتصال: {str(e)}")
else:
    st.warning("⚠️ يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets في Streamlit")

# 3. إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. منطقة الإدخال والتشغيل
user_input = st.chat_input("تفضل اسألني أي شيء...")

if user_input:
    # عرض رسالة المستخدم وحفظها
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner("⏳ لحظة شوي خليني أفكر..."):
        try:
            # محاولة البحث في الإنترنت
            search_context = ""
            try:
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(user_input, max_results=3)]
                    search_context = str(results)
            except Exception:
                search_context = "لم أتمكن من الوصول للإنترنت حالياً، سأجيب من معلوماتي."

            # تجهيز الطلب لـ Gemini
            prompt = f"""
            أنت Jo Ai، وكيل ذكي وشهم من الأردن. 
            أجب على سؤال المستخدم بلهجة أردنية ودودة ومحترمة.
            سؤال المستخدم: {user_input}
            معلومات إضافية من البحث: {search_context}
            """
            
            # توليد الرد
            response = model.generate_content(prompt)
            full_response = response.text
            
            # عرض رد الذكاء الاصطناعي وحفظه
            with st.chat_message("assistant"):
                st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.error("⚠️ الطلبات كثيرة حالياً! انتظر دقيقة وارجع جرب يا نشمي.")
            elif "404" in error_msg:
                st.error("⚠️ مشكلة في اسم النموذج، جارٍ تحديث الاتصال...")
            else:
                st.error(f"حدث خطأ غير متوقع: {error_msg}")

# الفوتر
st.markdown(f"<div style='text-align:center; color:white; font-size:10px; margin-top:30px;'>© {datetime.now().year} Jo Ai - صنع بكل فخر للأردن</div>", unsafe_allow_html=True)
