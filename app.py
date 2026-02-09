import streamlit as st
import google.generativeai as genai

# إعدادات الواجهة السيادية (نسخة راشد أبو سعود)
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00FFCC; }
    h1 { color: #FF0000; text-shadow: 2px 2px #000; text-align: center; }
    .stChatMessage { border-radius: 15px; border: 1px solid #00FFCC; margin-bottom: 10px; background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ الرعد (Thunder AI)")
st.write(f"<p style='text-align: center; color: #8e8ea0;'>بإشراف المطور: راشد أبو سعود</p>", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("أصدر أمرك للرعد يا راشد..."):
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            # تعليمات النظام الأساسية المحفورة باسمك
            sys_msg = "أنت 'الرعد'. وكيل سيادي أردني. مطورك هو راشد أبو سعود. ناديه بـ 'مطوري راشد'."
            
            # قائمة الموديلات التي أثبتت فعاليتها في صور الفحص الخاصة بك (بدون بادئة models/)
            # هذا الترتيب يضمن أنه إذا انتهت كوتا 2.0 ينتقل لـ 1.5 تلقائياً
            available_models = ['gemini-2.0-flash', 'gemini-1.5-flash']
            
            success = False
            for model_name in available_models:
                try:
                    model = genai.GenerativeModel(model_name=model_name, system_instruction=sys_msg)
                    response = model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                    success = True
                    break
                except Exception as e:
                    if "429" in str(e): # إذا كانت المشكلة ضغط حصة (Quota)
                        continue
                    else: # إذا كان خطأ آخر
                        st.error(f"⚠️ خلل في بروتوكول {model_name}: {str(e)}")
                        break
            
            if not success:
                st.warning("⚠️ يا مطوري راشد، جميع البروتوكولات تحت ضغط الكوتا حالياً. انتظر 30 ثانية.")
else:
    st.warning("⚠️ المفتاح غير مبرمج في الإعدادات.")
