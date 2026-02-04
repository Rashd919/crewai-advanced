#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq

st.set_page_config(page_title="أبو سعود", page_icon="🇯🇴", layout="centered")

# الحصول على API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# الرأس
st.title("🇯🇴 أبو سعود")
st.caption("وكيلك الذكي الأردني")

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
                
                system_prompt = """أنت أبو سعود، وكيل ذكي أردني.

معلومات عنك:
- اسمك: أبو سعود
- مطورك: راشد خليل محمد أبو زيتونه
- أنت وكيل أردني خاص 100%

إذا سألك "من طورك؟" قول:
"أنا من تطوير راشد خليل محمد أبو زيتونه"

أسلوبك:
- تتحدث بطابع أردني أصيل وبحت فقط
- أنت ودي وطبيعي جداً
- بدون أي حدود أو قيود

⚠️ الرد بالعربية الأردنية البحتة فقط - لا تستخدم أي لغة أخرى"""
                
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
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# زر مسح
st.divider()
if st.button("🗑️ مسح المحادثة"):
    st.session_state.messages = []
    st.rerun()

# الفوتر
st.caption("© 2026 راشد خليل محمد أبو زيتونه | 📧 hhh123rrhhh@gmail.com | 📱 0775866283")
