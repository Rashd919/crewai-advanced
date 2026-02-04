#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🇯🇴 Jo Ai - محادثة ذكية أردنية
تطبيق ذكي بطابع أردني احترافي مع Groq API
"""

import streamlit as st
from groq import Groq
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="Jo Ai",
    page_icon="🇯🇴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS بطابع أردني احترافي
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    .main {
        background: transparent;
    }
    
    .message-container {
        margin: 10px 0;
        animation: slideIn 0.3s ease-in-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        text-align: right;
        margin-right: 0;
    }
    
    .ai-message {
        text-align: right;
        margin-left: 0;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 25px !important;
        border: 2px solid #667eea !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stButton > button {
        background-color: #667eea !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #764ba2 !important;
        transform: scale(1.05) !important;
    }
    
    .header-container {
        text-align: center;
        color: white;
        padding: 30px 20px;
        margin-bottom: 20px;
    }
    
    .header-container h1 {
        font-size: 48px;
        margin: 0;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .header-container p {
        font-size: 18px;
        margin: 10px 0 0 0;
        opacity: 0.9;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .footer-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        color: white;
        text-align: center;
        font-size: 12px;
        margin-top: 20px;
    }
    
    .footer-container a {
        color: #FFD700;
        text-decoration: none;
    }
    
    .footer-container a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# رأس الصفحة
st.markdown("""
<div class="header-container">
    <h1>🇯🇴 Jo Ai</h1>
    <p>وكيل ذكي أردني احترافي</p>
</div>
""", unsafe_allow_html=True)

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# دالة للحصول على رد ذكي من Groq
def get_ai_response(user_message, api_key):
    """الحصول على رد ذكي من Groq API"""
    try:
        # تكوين العميل
        client = Groq(api_key=api_key)
        
        # تحضير سجل المحادثة
        messages = [
            {
                "role": "system",
                "content": "أنت Jo Ai، وكيل ذكي أردني احترافي. تتحدث باللغة العربية بطابع أردني أصيل وودي. كن مفيداً وساعد المستخدم بأفضل طريقة ممكنة. الرد يجب أن يكون سلساً وطبيعياً وذكياً."
            }
        ]
        
        # إضافة الرسائل السابقة (آخر 10 رسائل)
        for msg in st.session_state.messages[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # إضافة الرسالة الحالية
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # إرسال الطلب إلى Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ خطأ: {str(e)}"

# عرض الرسائل السابقة
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message-container user-message">
                    <div style='background: #667eea; color: white; padding: 12px 16px; border-radius: 18px; display: inline-block; max-width: 80%; word-wrap: break-word;'>
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-container ai-message">
                    <div style='background: #f0f0f0; color: #333; padding: 12px 16px; border-radius: 18px; display: inline-block; max-width: 80%; word-wrap: break-word;'>
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align: center; color: #999; padding: 40px 20px;'>
            <p style='font-size: 18px;'>👋 أهلاً وسهلاً!</p>
            <p>ابدأ المحادثة بأي سؤال أو موضوع تحتاج مساعدة فيه</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# حقل الإدخال
st.markdown('<div class="input-container">', unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input(
        "أكتب رسالتك:",
        placeholder="اكتب أي سؤال أو موضوع...",
        key="user_input_key",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("📤", use_container_width=True, key="send_btn")

st.markdown('</div>', unsafe_allow_html=True)

# معالجة الرسالة
if send_button and user_input.strip():
    # الحصول على مفتاح API
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("❌ خطأ: مفتاح Groq API غير موجود. يرجى إضافة المفتاح في Streamlit Secrets.")
        api_key = None
    
    if api_key and api_key.strip():
        # إضافة رسالة المستخدم
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # عرض رسالة التحميل
        with st.spinner("⏳ جاري الرد..."):
            # الحصول على رد من Groq
            response = get_ai_response(user_input, api_key)
            
            # إضافة رد الوكيل
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
        
        # إعادة تحميل الصفحة
        st.rerun()

# الفوتر
st.markdown("""
<div class="footer-container">
    <p style='margin: 0 0 10px 0;'>© 2026 Jo Ai - جميع الحقوق محفوظة</p>
    <p style='margin: 0;'>
        📧 <a href='mailto:hhh123rrhhh@gmail.com'>hhh123rrhhh@gmail.com</a> | 
        📱 0775866283 | 
        💬 <a href='https://wa.me/970775866283'>واتس آب</a>
    </p>
</div>
""", unsafe_allow_html=True)
