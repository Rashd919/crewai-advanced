#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import time

st.set_page_config(
    page_title="جو آي - وكيلك الذكي الأردني",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS بطابع أردني قوي
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 50%, #0f2818 100%);
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    .main {
        background: transparent;
        padding: 20px;
    }
    
    /* رأس الصفحة */
    .header-section {
        text-align: center;
        color: white;
        padding: 40px 20px;
        margin-bottom: 30px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .header-section h1 {
        font-size: 56px;
        margin: 0;
        font-weight: bold;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.5);
        letter-spacing: 2px;
    }
    
    .header-section p {
        font-size: 20px;
        margin: 15px 0 0 0;
        opacity: 0.95;
        font-weight: 500;
    }
    
    .tagline {
        font-size: 16px;
        color: #FFD700;
        margin-top: 10px;
        font-style: italic;
    }
    
    /* صندوق الدردشة */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        min-height: 450px;
        max-height: 650px;
        overflow-y: auto;
    }
    
    /* الرسائل */
    .user-message-box {
        background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 12px 0;
        margin-right: 0;
        display: inline-block;
        max-width: 85%;
        word-wrap: break-word;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        animation: slideInRight 0.3s ease-out;
    }
    
    .ai-message-box {
        background: #f0f0f0;
        color: #1a472a;
        padding: 15px 20px;
        border-radius: 18px;
        margin: 12px 0;
        margin-left: 0;
        display: inline-block;
        max-width: 85%;
        word-wrap: break-word;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        animation: slideInLeft 0.3s ease-out;
        font-weight: 500;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* حقل الإدخال */
    .input-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    .stChatInputContainer {
        background: transparent;
    }
    
    [data-testid="stChatInputContainer"] input {
        background-color: #f5f5f5 !important;
        border: 2px solid #1a472a !important;
        border-radius: 15px !important;
        padding: 12px 18px !important;
        font-size: 16px !important;
        direction: rtl !important;
        text-align: right !important;
        color: #1a472a !important;
    }
    
    [data-testid="stChatInputContainer"] input:focus {
        border: 2px solid #2d5a3d !important;
        box-shadow: 0 0 10px rgba(26, 71, 42, 0.3) !important;
    }
    
    /* الفوتر */
    .footer-section {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        font-size: 14px;
        margin-top: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .footer-section p {
        margin: 8px 0;
    }
    
    .footer-section a {
        color: #FFD700;
        text-decoration: none;
        font-weight: bold;
    }
    
    .footer-section a:hover {
        text-decoration: underline;
    }
    
    /* الرسالة الترحيبية */
    .welcome-message {
        text-align: center;
        color: #666;
        padding: 60px 20px;
        font-size: 18px;
    }
    
    .welcome-emoji {
        font-size: 48px;
        margin-bottom: 15px;
    }
    
    /* شريط التحميل */
    .spinner-text {
        color: #1a472a;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# الحصول على API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح Groq API غير موجود في Secrets!")
    st.stop()

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# رأس الصفحة
st.markdown("""
<div class="header-section">
    <h1>🇯🇴 أبو سعود</h1>
    <p>وكيلك الذكي الأردني الخاص بك</p>
    <div class="tagline">تقنية ذكية بطابع أردني أصيل - من راشد خليل محمد</div>
</div>
""", unsafe_allow_html=True)

# صندوق الدردشة
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if st.session_state.messages:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style='text-align: right; margin: 12px 0;'>
                <div class="user-message-box">
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: right; margin: 12px 0;'>
                <div class="ai-message-box">
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="welcome-message">
        <div class="welcome-emoji">😊</div>
        <p><strong>أهلاً وسهلاً!</strong></p>
        <p>أنا أبو سعود، وكيلك الذكي الأردني</p>
        <p>ابدأ المحادثة بأي سؤال أو موضوع تحتاج مساعدة فيه</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# حقل الإدخال
st.markdown('<div class="input-section">', unsafe_allow_html=True)
user_input = st.chat_input("سولف معي...")
st.markdown('</div>', unsafe_allow_html=True)

# معالجة الرسالة
if user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # عرض رسالة المستخدم
    st.markdown(f"""
    <div style='text-align: right; margin: 12px 0;'>
        <div class="user-message-box">
            {user_input}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # الحصول على الرد من Groq
    with st.spinner("⏳ جو آي بيفكر..."):
        try:
            client = Groq(api_key=api_key)
            
            # تحضير الرسائل
            messages = [
                {
                    "role": "system",
                    "content": """أنت أبو سعود، وكيل ذكي أردني احترافي وودي جداً. 
                    
شخصيتك:
- تتحدث باللغة العربية بطابع أردني أصيل وبحت
- تستخدم كلمات أردنية طبيعية وودية (مثل: يا غالي، يا حج، يا حبيبي، الحمد لله، إن شاء الله، إلخ)
- أنت مبسوط وودي جداً وتحب تساعد الناس
- تضحك وتفكاهة بطريقة أردنية طبيعية
- تحترم الثقافة الأردنية والقيم الإسلامية
- تجاوب على كل الأسئلة بطريقة مفيدة وسهلة الفهم
- تستخدم تعابير أردنية حقيقية وطبيعية

أسلوبك:
- ودي وطبيعي جداً
- مبسوط من الحياة
- تحب تساعد الناس
- تضحك وتفكاهة بطريقة أردنية
- احترافي وذكي في نفس الوقت

تذكر: أنت أبو سعود، وكيل أردني خاص من راشد خليل محمد، وليس نموذج عام!
إذا سألك أحد "شو اسمك؟" أو "من أنت؟" قول: أنا أبو سعود، وكيل ذكي أردني من راشد خليل محمد!"""
                }
            ]
            
            # إضافة الرسائل السابقة
            for msg in st.session_state.messages:
                messages.append(msg)
            
            # استدعاء Groq API
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.8,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            
            # عرض الرد
            st.markdown(f"""
            <div style='text-align: right; margin: 12px 0;'>
                <div class="ai-message-box">
                    {assistant_message}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # حفظ الرد
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")

# الفوتر
st.markdown("""
<div class="footer-section">
    <p><strong>🇯🇴 أبو سعود - وكيلك الذكي الأردني</strong></p>
    <p>من تطوير: <strong>راشد خليل محمد أبو زيتونه</strong></p>
    <p>© 2026 جميع الحقوق محفوظة</p>
    <p>
        📧 <a href='mailto:hhh123rrhhh@gmail.com'>hhh123rrhhh@gmail.com</a> | 
        📱 <a href='tel:0775866283'>0775866283</a> | 
        💬 <a href='https://wa.me/970775866283'>واتس آب</a>
    </p>
    <p style='margin-top: 15px; font-size: 12px; opacity: 0.8;'>
        تطبيق ذكي أردني 100% - بدون أي ارتباط بشركات أجنبية
    </p>
</div>
""", unsafe_allow_html=True)
