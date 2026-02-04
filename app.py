#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import json
from datetime import datetime

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS احترافي مثل ChatGPT
st.markdown("""
<style>
    * {
        direction: rtl;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: #ffffff;
        color: #2c3e50;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* الحاوية الرئيسية */
    .main {
        max-width: 900px;
        margin: 0 auto;
        padding: 0;
    }
    
    /* رسائل المستخدم */
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) {
        background: transparent;
        padding: 0;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) > div {
        background: #E8F0FE;
        border-radius: 18px;
        padding: 12px 16px;
        margin-right: 0;
        max-width: 70%;
        margin-left: auto;
    }
    
    /* رسائل الوكيل */
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) {
        background: transparent;
        padding: 0;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) > div {
        background: #f5f5f5;
        border-radius: 18px;
        padding: 12px 16px;
        margin-left: 0;
        max-width: 70%;
    }
    
    /* صندوق الإدخال */
    [data-testid="stChatInputContainer"] {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,1) 20%);
        padding: 20px;
        z-index: 100;
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
        color: #2c3e50 !important;
        background: white !important;
        resize: vertical !important;
        min-height: 44px !important;
        max-height: 200px !important;
    }
    
    [data-testid="stChatInputContainer"] textarea:focus {
        border: 1px solid #CE112E !important;
        box-shadow: 0 0 0 3px rgba(206, 17, 38, 0.1) !important;
    }
    
    [data-testid="stChatInputContainer"] textarea::placeholder {
        color: #999;
    }
    
    /* زر الإرسال */
    [data-testid="stChatInputContainer"] button {
        background: #CE112E !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInputContainer"] button:hover {
        background: #a00a2e !important;
        transform: scale(1.05) !important;
    }
    
    /* الأزرار العامة */
    .stButton > button {
        background: #CE112E !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: #a00a2e !important;
    }
    
    /* أيقونات الأدوات */
    .tool-icon {
        font-size: 18px;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .tool-icon:hover {
        background: #f0f0f0;
    }
    
    /* مساحة للمحادثة */
    [data-testid="stChatMessageContainer"] {
        padding-bottom: 180px;
    }
    
    /* الرسالة الترحيبية */
    .welcome-message {
        text-align: center;
        padding: 60px 20px;
        color: #999;
    }
    
    .welcome-message h2 {
        font-size: 32px;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    
    .welcome-message p {
        font-size: 16px;
        color: #999;
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
if "show_header" not in st.session_state:
    st.session_state.show_header = True

# الرأس (Header)
if st.session_state.show_header and len(st.session_state.messages) == 0:
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px;'>
        <h1 style='font-size: 42px; margin: 0; color: #2c3e50;'>🇯🇴 أبو سعود</h1>
        <p style='font-size: 16px; color: #999; margin-top: 10px;'>وكيلك الذكي الأردني</p>
        <p style='font-size: 14px; color: #ccc; margin-top: 20px;'>ابدأ محادثة جديدة أو اسأل أي سؤال</p>
    </div>
    """, unsafe_allow_html=True)

# عرض الرسائل
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # أدوات الرد (تحت رسائل الوكيل فقط)
        if message["role"] == "assistant":
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 8])
            
            with col1:
                if st.button("👍", key=f"like_{idx}", help="نافع"):
                    st.toast("✓ شكراً على التقييم الإيجابي!")
            
            with col2:
                if st.button("👎", key=f"dislike_{idx}", help="ما نافع"):
                    st.toast("✓ سنحاول تحسين الردود")
            
            with col3:
                if st.button("📋", key=f"copy_{idx}", help="نسخ"):
                    st.toast("✓ تم نسخ الرد")
            
            with col4:
                if st.button("🔁", key=f"retry_{idx}", help="إعادة توليد"):
                    st.toast("✓ جاري إعادة الرد...")

# زر مسح المحادثة (في الأعلى)
if len(st.session_state.messages) > 0:
    col1, col2, col3 = st.columns([1, 20, 1])
    with col3:
        if st.button("🗑️", help="مسح المحادثة"):
            st.session_state.messages = []
            st.rerun()

# حقل الإدخال
if prompt := st.chat_input("اكتب رسالتك هنا…"):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.show_header = False
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # الحصول على الرد
    with st.chat_message("assistant"):
        with st.spinner("⏳ جاري الرد..."):
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
                
                # حفظ الرد
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                # أدوات الرد
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 8])
                
                with col1:
                    if st.button("👍", key=f"like_new", help="نافع"):
                        st.toast("✓ شكراً على التقييم الإيجابي!")
                
                with col2:
                    if st.button("👎", key=f"dislike_new", help="ما نافع"):
                        st.toast("✓ سنحاول تحسين الردود")
                
                with col3:
                    if st.button("📋", key=f"copy_new", help="نسخ"):
                        st.toast("✓ تم نسخ الرد")
                
                with col4:
                    if st.button("🔁", key=f"retry_new", help="إعادة توليد"):
                        st.toast("✓ جاري إعادة الرد...")
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# معلومات التطبيق (في الأسفل)
st.markdown("""
<div style='text-align: center; color: #ccc; font-size: 12px; margin-top: 100px; padding: 20px;'>
    <p>© 2026 راشد خليل محمد أبو زيتونه</p>
    <p>📧 hhh123rrhhh@gmail.com | 📱 0775866283</p>
</div>
""", unsafe_allow_html=True)
