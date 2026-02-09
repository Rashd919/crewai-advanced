import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الواجهة البسيطة (الأصلية) ---
st.set_page_config(page_title="الرعد AI", layout="centered")

st.title("⚡ الرعد AI")
st.markdown("---")

# جلب مفتاح الـ API من الـ Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

# --- 2. تشغيل المحرك ---
if api_key:
    genai.configure(api_key=api_key)
    # استخدام الموديل الأكثر استقراراً وبساطة
    model = genai.GenerativeModel('gemini-1.5-flash')

    # تهيئة الذاكرة المؤقتة (Session State)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل القديمة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # صندوق الإدخال
    if prompt := st.chat_input("احكي مع الرعد..."):
        # إضافة رسالة المستخدم للذاكرة والعرض
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # استدعاء رد الرعد
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(f"أنت الرعد، مساعد ذكي بلهجة أردنية. رد على: {prompt}")
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("⚠️ حدث خطأ في الاتصال. تأكد من مفتاح الـ API في الإعدادات.")
else:
    st.warning("⚠️ لم يتم العثور على مفتاح GEMINI_API_KEY في إعدادات Secrets.")
