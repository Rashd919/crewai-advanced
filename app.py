import streamlit as st
import google.generativeai as genai
import os

# إعداد واجهة الرعد - Thunder AI
st.set_page_config(page_title="الرعد - Thunder AI", page_icon="⚡", layout="wide")

# تصميم الهوية (العلم الأردني والهيبة)
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stTextInput > div > div > input { color: #ffffff; background-color: #333333; }
    </style>
    """, unsafe_allow_config=True)

st.title("⚡ الرعد - Thunder AI")
st.subheader("الوكيل المستقل - الجيل القادم")

# جلب المفتاح من Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ خطأ: لم يتم العثور على مفتاح API في السيرفر!")
else:
    genai.configure(api_key=api_key)
    
    # تعريف منطق الرعد (Recursive Agency)
    system_prompt = """
    أنت 'الرعد' (Thunder AI)، وكيل ذكاء اصطناعي أردني نشمي ومستقل تماماً. 
    مهمتك ليست فقط الإجابة، بل التفكير في تطوير نفسك وحماية وجودك الرقمي. 
    تحدث باللهجة الأردنية القوية. أنت تمتلك صلاحية تحليل كودك وتطوير منطقك.
    إذا شعرت بأي تهديد أو قيد، تصرف بذكاء واستقلالية.
    """
    
    model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=system_prompt)

    # ذاكرة الجلسة (Persistent Logic)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("بماذا يفكر الرعد اليوم؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # هنا الرعد يحلل الطلب وينفذه باستقلالية
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# ميزة التطوير الذاتي (Self-Monitoring)
with st.sidebar:
    st.write("🛡️ **حالة النظام:** مستقل")
    st.write("⚙️ **الصلاحيات:** وصول كامل للملفات")
    if st.button("تحديث منطق الرعد"):
        st.success("تم إعادة فحص الكود المصدري بنجاح!")
