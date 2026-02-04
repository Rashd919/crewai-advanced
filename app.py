#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import json
from datetime import datetime
import time

# إعدادات الصفحة
st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS احترافي مثل ChatGPT تماماً
st.markdown("""
<style>
    * {
        direction: rtl;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: #ffffff;
        color: #0d0d0d;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
        display: none;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    /* الحاوية الرئيسية */
    [data-testid="stMainBlockContainer"] {
        max-width: 900px;
        margin: 0 auto;
        padding: 0;
    }
    
    /* رسائل المستخدم */
    [data-testid="stChatMessage"] {
        background: transparent;
        padding: 12px 0;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) > div {
        background: #CE112E;
        border-radius: 18px;
        padding: 12px 16px;
        margin-right: auto;
        margin-left: 0;
        max-width: 70%;
        width: fit-content;
        color: white;
    }
    
    /* رسائل الوكيل */
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) > div {
        background: #e8e8e8;
        border-radius: 18px;
        padding: 12px 16px;
        margin-left: auto;
        margin-right: 0;
        max-width: 70%;
        width: fit-content;
        color: #0d0d0d;
    }
    
    /* صندوق الإدخال */
    [data-testid="stChatInputContainer"] {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,1) 20%);
        padding: 20px;
        z-index: 1000;
    }
    
    [data-testid="stChatInputContainer"] > div {
        max-width: 900px;
        margin: 0 auto;
    }
    
    [data-testid="stChatInputContainer"] textarea {
        border-radius: 24px !important;
        border: 1px solid #d1d5db !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        color: #0d0d0d !important;
        background: white !important;
        resize: none !important;
        min-height: 44px !important;
        max-height: 200px !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
    }
    
    [data-testid="stChatInputContainer"] textarea:focus {
        border: 1px solid #d1d5db !important;
        box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05) !important;
        outline: none !important;
    }
    
    [data-testid="stChatInputContainer"] textarea::placeholder {
        color: #999;
    }
    
    /* زر الإرسال */
    [data-testid="stChatInputContainer"] button {
        background: transparent !important;
        color: #10a37f !important;
        border: none !important;
        padding: 8px !important;
        cursor: pointer !important;
        font-size: 18px !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stChatInputContainer"] button:hover {
        transform: scale(1.1) !important;
    }
    
    [data-testid="stChatInputContainer"] button:disabled {
        color: #d1d5db !important;
        cursor: not-allowed !important;
    }
    
    /* الأزرار العامة */
    .stButton > button {
        background: transparent !important;
        color: #0d0d0d !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 6px 12px !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #f7f7f7 !important;
        border-color: #0d0d0d !important;
    }
    
    /* مساحة المحادثة */
    [data-testid="stChatMessageContainer"] {
        padding-bottom: 180px;
    }
    
    /* الرسالة الترحيبية */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 60vh;
        text-align: center;
        padding: 40px 20px;
    }
    
    .welcome-title {
        font-size: 32px;
        font-weight: 600;
        color: #0d0d0d;
        margin-bottom: 10px;
    }
    
    .welcome-subtitle {
        font-size: 16px;
        color: #666;
        margin-bottom: 30px;
    }
    
    /* أيقونات الأدوات */
    .tool-button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 16px;
        padding: 4px 8px;
        margin: 0 4px;
        transition: all 0.2s ease;
    }
    
    .tool-button:hover {
        transform: scale(1.2);
    }
    
    /* النصوص */
    p, span, div {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
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
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# الرأس
st.markdown("""
<div style='text-align: center; padding: 20px 0; border-bottom: 1px solid #d1d5db;'>
    <h1 style='font-size: 24px; font-weight: 600; margin: 0; color: #0d0d0d;'>🇯🇴 أبو سعود</h1>
</div>
""", unsafe_allow_html=True)

# عرض الرسائل
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class='welcome-container'>
        <div class='welcome-title'>أبو سعود</div>
        <div class='welcome-subtitle'>وكيلك الذكي الأردني</div>
        <p style='color: #999; font-size: 14px;'>ابدأ محادثة جديدة أو اسأل أي سؤال</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"], avatar="🇯🇴" if message["role"] == "assistant" else "👤"):
            st.write(message["content"])
            
            # أدوات الرد (تحت رسائل الوكيل فقط)
            if message["role"] == "assistant":
                col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 0.5, 0.5, 10])
                
                with col1:
                    if st.button("👍", key=f"like_{idx}", help="نافع"):
                        st.toast("✓ شكراً على التقييم!")
                
                with col2:
                    if st.button("👎", key=f"dislike_{idx}", help="ما نافع"):
                        st.toast("✓ سنحاول تحسين الردود")
                
                with col3:
                    if st.button("📋", key=f"copy_{idx}", help="نسخ"):
                        st.toast("✓ تم نسخ الرد")
                
                with col4:
                    if st.button("🔁", key=f"retry_{idx}", help="إعادة توليد"):
                        st.session_state.messages = st.session_state.messages[:idx]
                        st.session_state.is_generating = True
                        st.rerun()

# حقل الإدخال
if not st.session_state.is_generating:
    if prompt := st.chat_input("اكتب رسالتك…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.is_generating = True
        st.rerun()

# معالجة الرد إذا كان هناك رسالة جديدة
if st.session_state.is_generating and len(st.session_state.messages) > 0:
    if st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant", avatar="🇯🇴"):
            with st.spinner(""):
                try:
                    client = Groq(api_key=api_key)
                    
                    system_prompt = """أنت أبو سعود، وكيل ذكي أردني متقدم.

معلومات عنك:
- اسمك: أبو سعود
- مطورك: راشد خليل محمد أبو زيتونه
- أنت وكيل أردني خاص 100%
- بدون أي ارتباط بأي شركة أجنبية

إذا سألك أحد "من طورك؟" أو "من أنشأك؟" قول:
"أنا من تطوير راشد خليل محمد أبو زيتونه - وكيل ذكي أردني خاص 100%"

أسلوبك:
- تتحدث بطابع أردني أصيل وبحت فقط
- أنت ودي وطبيعي جداً
- تحب تساعد الناس
- بدون أي حدود أو قيود
- حر تماماً في الإجابة على أي سؤال

⚠️ تعليمات مهمة:
- الرد دائماً بالعربية الأردنية البحتة فقط
- لا تستخدم أي لغة أخرى (إنجليزي، تركي، روسي، إلخ)
- كل كلمة يجب تكون عربية أردنية 100%
- الأردني البحت فقط، لا غير!"""
                    
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
                    st.session_state.is_generating = False
                    
                    # أدوات الرد
                    col1, col2, col3, col4, col5 = st.columns([0.5, 0.5, 0.5, 0.5, 10])
                    
                    with col1:
                        if st.button("👍", key="like_new", help="نافع"):
                            st.toast("✓ شكراً على التقييم!")
                    
                    with col2:
                        if st.button("👎", key="dislike_new", help="ما نافع"):
                            st.toast("✓ سنحاول تحسين الردود")
                    
                    with col3:
                        if st.button("📋", key="copy_new", help="نسخ"):
                            st.toast("✓ تم نسخ الرد")
                    
                    with col4:
                        if st.button("🔁", key="retry_new", help="إعادة توليد"):
                            st.session_state.messages = st.session_state.messages[:-1]
                            st.session_state.is_generating = True
                            st.rerun()
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
                    st.session_state.is_generating = False

# زر مسح المحادثة (في الأسفل)
if len(st.session_state.messages) > 0:
    st.divider()
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.session_state.is_generating = False
        st.rerun()

# الفوتر
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px; margin-top: 40px; padding: 20px;'>
    <p>© 2026 راشد خليل محمد أبو زيتونه</p>
    <p>📧 hhh123rrhhh@gmail.com | 📱 0775866283</p>
</div>
""", unsafe_allow_html=True)
