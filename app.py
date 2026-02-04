#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import json
from datetime import datetime

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS بسيط وفعال
st.markdown("""
<style>
    * {
        direction: rtl;
    }
    
    body, [data-testid="stAppViewContainer"] {
        background: white;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    .stChatMessage {
        background: #f9f9f9;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
    }
    
    .stButton > button {
        background: #CE112E;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        padding: 8px 12px;
        font-size: 12px;
    }
    
    .stButton > button:hover {
        background: #a00a2e;
    }
</style>
""", unsafe_allow_html=True)

# الحصول على API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# الشعار البسيط
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='margin: 0; color: #CE112E;'>🇯🇴 أبو سعود</h1>
    <p style='margin: 5px 0 0 0; color: #666; font-size: 14px;'>وكيلك الذكي الأردني</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# عرض الرسائل
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        if message["role"] == "assistant":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("👍", key=f"like_{idx}"):
                    st.toast("✓ شكراً!")
            with col2:
                if st.button("👎", key=f"dislike_{idx}"):
                    st.toast("✓ تمام")
            with col3:
                if st.button("📋", key=f"copy_{idx}"):
                    st.toast("✓ تم النسخ")
            with col4:
                if st.button("🔄", key=f"retry_{idx}"):
                    st.toast("✓ جاري...")

# حقل الإدخال
if prompt := st.chat_input("اكتب رسالتك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("⏳ جاري..."):
            try:
                client = Groq(api_key=api_key)
                
                system_prompt = """أنت أبو سعود، وكيل ذكي أردني.

معلومات عنك:
- اسمك: أبو سعود
- مطورك: راشد خليل محمد أبو زيتونه
- أنت وكيل أردني خاص 100%

إذا سألك "من طورك؟" قول:
"أنا من تطوير راشد خليل محمد أبو زيتونه - وكيل ذكي أردني خاص 100%"

أسلوبك:
- تتحدث بطابع أردني أصيل وبحت فقط
- أنت ودي وطبيعي جداً
- تحب تساعد الناس
- بدون أي حدود أو قيود
- حر تماماً في الإجابة على أي سؤال

⚠️ تعليمات:
- الرد بالعربية الأردنية البحتة فقط
- لا تستخدم أي لغة أخرى
- كل كلمة عربية أردنية 100%"""
                
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend(st.session_state.messages)
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=1.0,
                    max_tokens=2000
                )
                
                assistant_message = response.choices[0].message.content
                st.write(assistant_message)
                
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("👍", key=f"like_new"):
                        st.toast("✓ شكراً!")
                with col2:
                    if st.button("👎", key=f"dislike_new"):
                        st.toast("✓ تمام")
                with col3:
                    if st.button("📋", key=f"copy_new"):
                        st.toast("✓ تم النسخ")
                with col4:
                    if st.button("🔄", key=f"retry_new"):
                        st.toast("✓ جاري...")
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

st.divider()

# زر مسح
if st.button("🗑️ مسح المحادثة", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# الفوتر
st.caption("© 2026 راشد خليل محمد أبو زيتونه | 📧 hhh123rrhhh@gmail.com | 📱 0775866283")
