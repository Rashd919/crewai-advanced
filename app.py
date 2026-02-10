import streamlit as st

# بروتوكول التطور (UPDATE_CODE) مفعل الآنتحت الرقابة
# ب1 أضف وظيفة في الشريط الجانبي (Sidebar) تسمح بتحميل سجل المحادثة الحالي كملف نصي (.txt)

# الشريط الجانبي
st.sidebar.title("خيارات")

# الزر الذي سيقوم بتحميل سجل المحادثة الحالي كملف نصي (.txt)
if st.sidebar.button("تحميل سجل المحادثة"):
    # سجل المحادثة الحالي
    conversation_log = st.session_state.conversation_log
    
    # تحويل سجل المحادثة إلى نص
    log_text = "\n".join(conversation_log)
    
    # تحميل النص إلى ملف نصي (.txt)
    with open("conversation_log.txt", "w") as f:
        f.write(log_text)
    
    # إشعار بالنجاح
    st.sidebar.success("تم تحميل سجل المحادثة بنجاح!")

# حافظ على التنسيق الذهبي والأسود
st.markdown("<style>body {background-color: #f0f0f0;}</style>", unsafe_allow_html=True)
st.markdown("<style>h1 {color: #000000;}</style>", unsafe_allow_html=True)
st.markdown("<style>h2 {color: #000000;}</style>", unsafe_allow_html=True)
st.markdown("<style>p {color: #000000;}</style>", unsafe_allow_html=True)