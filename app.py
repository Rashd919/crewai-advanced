#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="جو آي",
    page_icon="🇯🇴",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

st.title("🇯🇴 جو آي - النشمي")

# الحصول على API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح Groq API غير موجود في Secrets!")
    st.stop()

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# حقل الإدخال
user_input = st.chat_input("سولف معي...")

if user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    # الحصول على الرد من Groq
    with st.chat_message("assistant"):
        with st.spinner("⏳ جاري الرد..."):
            try:
                client = Groq(api_key=api_key)
                
                # تحضير الرسائل
                messages = [
                    {
                        "role": "system",
                        "content": "أنت Jo Ai، وكيل ذكي أردني احترافي. تتحدث باللغة العربية بطابع أردني أصيل. كن مفيداً وودي."
                    }
                ]
                
                # إضافة الرسائل السابقة
                for msg in st.session_state.messages:
                    messages.append(msg)
                
                # استدعاء Groq API
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000
                )
                
                assistant_message = response.choices[0].message.content
                st.write(assistant_message)
                
                # حفظ الرد
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
