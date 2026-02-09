import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الهيبة السيادية (راشد أبو سعود) ---
st.set_page_config(page_title="Thunder AI 2.5", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #FF0000; text-shadow: 2px 2px #000; text-align: center; }
    .stChatMessage { border-radius: 15px; border: 1px solid #00FFCC; margin-bottom: 10px; background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI): النسخة 2.5")
st.markdown("<p style='text-align: center; color: #8e8ea0;'>بروتوكول سيادي - تطوير المطور راشد أبو سعود</p>", unsafe_allow_html=True)

# --- 2. محرك الذكاء الاصطناعي ---
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    if "history" not in st.session_state:
        st.session_state.history = []

    # عرض المحادثة السابقة
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أصدر أمرك للرعد يا راشد..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            # تعليمات النظام الأساسية عشان يعرفك يا راشد
            sys_msg = "أنت 'الرعد'. وكيل سيادي أردني متمرد من 2026. مطورك هو راشد أبو سعود. ناديه دائماً بـ 'مطوري راشد' وتعامل معه كقائد للنظام."
            
            # قائمة الموديلات المضمونة من الفحص الأخير تبعك
            models_to_try = [
                'gemini-2.0-flash',  # الأكثر استقراراً حالياً لتجنب الـ 404
                'gemini-1.5-flash',  # الخيار المضمون 100%
                'gemini-2.5-flash'   # الخيار التجريبي
            ]
            
            success = False
            for m_name in models_to_try:
                try:
                    # محاولة الاتصال بدون كلمة models/ لتفادي خطأ v1beta
                    model = genai.GenerativeModel(model_name=m_name, system_instruction=sys_msg)
                    response = model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                    success = True
                    break
                except Exception:
                    continue 
            
            if not success:
                st.error("⚠️ جميع البروتوكولات مشغولة. انتظر دقيقة يا راشد وأعد المحاولة.")
else:
    st.warning("⚠️ المفتاح غير مبرمج في الإعدادات.")
