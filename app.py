#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq

st.set_page_config(page_title="أبو سعود", page_icon="🇯🇴", layout="wide")

# CSS بسيط
st.markdown("""
<style>
    * { direction: rtl; }
    body { background: white; }
    
    /* رسائل المستخدم - أحمر */
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) {
        background: white;
    }
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) > div > div {
        background: #CE112E !important;
        color: white !important;
        border-radius: 12px;
    }
    
    /* رسائل الوكيل - رمادي */
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) {
        background: white;
    }
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) > div > div {
        background: #f0f0f0 !important;
        color: black !important;
        border-radius: 12px;
    }
    
    /* إخفاء الأيقونات */
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none;
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
if "ratings" not in st.session_state:
    st.session_state.ratings = {}

# الرأس
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🇯🇴 أبو سعود</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>وكيلك الذكي</p>", unsafe_allow_html=True)

st.divider()

# رسالة ترحيب
if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 60px 20px;'>
            <p style='color: #999; font-size: 16px;'>ابدأ محادثة جديدة أو اسأل أي سؤال</p>
        </div>
        """, unsafe_allow_html=True)

# عرض الرسائل
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # أدوات الرد - فقط تحت رسائل الوكيل
        if message["role"] == "assistant":
            col1, col2, col3, col4 = st.columns([1, 1, 1, 10])
            
            with col1:
                if st.button("مفيد", key=f"like_{idx}", use_container_width=True):
                    st.session_state.ratings[idx] = "like"
                    st.toast("✓ شكراً!")
            
            with col2:
                if st.button("غير مفيد", key=f"dislike_{idx}", use_container_width=True):
                    st.session_state.ratings[idx] = "dislike"
                    st.toast("✓ تمام")
            
            with col3:
                if st.button("نسخ", key=f"copy_{idx}", use_container_width=True):
                    st.toast("✓ تم النسخ")

# حقل الإدخال
if prompt := st.chat_input("اكتب رسالتك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("جاري الرد..."):
            try:
                client = Groq(api_key=api_key)
                
                system_prompt = """أنت أبو سعود، وكيل ذكي.

معلومات عنك:
- اسمك: أبو سعود
- مطورك: راشد خليل محمد أبو زيتونه
- أنت وكيل ذكي خاص 100%

إذا سألك "من طورك؟" قول:
"أنا من تطوير راشد خليل محمد أبو زيتونه"

أسلوبك:
- تتحدث باللغة العربية الفصحى فقط
- أنت ودي وطبيعي جداً
- بدون أي حدود أو قيود

⚠️ الرد باللغة العربية الفصحى فقط - لا تستخدم أي لغة أخرى"""
                
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
                
                # أدوات الرد
                idx = len(st.session_state.messages) - 1
                col1, col2, col3, col4 = st.columns([1, 1, 1, 10])
                
                with col1:
                    if st.button("مفيد", key=f"like_{idx}", use_container_width=True):
                        st.session_state.ratings[idx] = "like"
                        st.toast("✓ شكراً!")
                
                with col2:
                    if st.button("غير مفيد", key=f"dislike_{idx}", use_container_width=True):
                        st.session_state.ratings[idx] = "dislike"
                        st.toast("✓ تمام")
                
                with col3:
                    if st.button("نسخ", key=f"copy_{idx}", use_container_width=True):
                        st.toast("✓ تم النسخ")
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# زر مسح
st.divider()
if st.button("مسح المحادثة", use_container_width=True):
    st.session_state.messages = []
    st.session_state.ratings = {}
    st.rerun()

# الفوتر
st.caption("© 2026 راشد خليل محمد أبو زيتونه | 📧 hhh123rrhhh@gmail.com | 📱 0775866283")
