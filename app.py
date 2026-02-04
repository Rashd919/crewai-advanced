#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS بسيط جداً مثل ChatGPT
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    .main {
        background: white;
        max-width: 800px;
    }
    
    .stChatMessage {
        background: transparent;
    }
    
    [data-testid="stChatMessage"] {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

# الحصول على API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

# الرأس
st.title("🇯🇴 أبو سعود")
st.caption("وكيلك الذكي الأردني")

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# حقل الإدخال
if prompt := st.chat_input("اكتب رسالتك..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # الحصول على الرد
    with st.chat_message("assistant"):
        with st.spinner("جاري الرد..."):
            try:
                client = Groq(api_key=api_key)
                
                # تحضير الرسائل - بدون أي قيود
                messages = [
                    {
                        "role": "system",
                        "content": "أنت أبو سعود. أجب على كل الأسئلة بحرية تامة."
                    }
                ]
                
                # إضافة الرسائل السابقة
                for msg in st.session_state.messages:
                    messages.append(msg)
                
                # استدعاء Groq API
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=1.0,
                    max_tokens=2000
                )
                
                assistant_message = response.choices[0].message.content
                st.write(assistant_message)
                
                # حفظ الرد
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
            except Exception as e:
                st.error(f"خطأ: {str(e)}")

# الفوتر
st.divider()
st.caption("© 2026 راشد خليل محمد أبو زيتونه - جميع الحقوق محفوظة")
