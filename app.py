#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
أبو سعود - وكيل ذكي أردني
تطبيق ذكي أردني 100% بدون أي قيود
© 2026 راشد خليل محمد أبو زيتونه - جميع الحقوق محفوظة
"""

import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="أبو سعود - وكيلك الذكي الأردني",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS بتصميم أردني احترافي جداً
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
        font-family: 'Arial', 'Segoe UI', sans-serif;
    }
    
    /* الخلفية الأردنية */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 25%, #2d2d2d 50%, #1a1a1a 75%, #000000 100%);
        background-attachment: fixed;
        min-height: 100vh;
        color: #ffffff;
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
    
    /* رأس الصفحة - الشعار الأردني */
    .header-section {
        text-align: center;
        padding: 50px 20px;
        margin-bottom: 30px;
        background: linear-gradient(135deg, rgba(206, 17, 38, 0.1) 0%, rgba(0, 0, 0, 0.3) 50%, rgba(206, 17, 38, 0.1) 100%);
        border-radius: 25px;
        border: 3px solid #CE112E;
        backdrop-filter: blur(10px);
        box-shadow: 0 20px 60px rgba(206, 17, 38, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #CE112E, #000000, #CE112E);
    }
    
    .header-section h1 {
        font-size: 64px;
        margin: 0;
        font-weight: 900;
        color: #CE112E;
        text-shadow: 3px 3px 10px rgba(206, 17, 38, 0.8), 0 0 20px rgba(206, 17, 38, 0.4);
        letter-spacing: 3px;
        line-height: 1.2;
    }
    
    .header-section p {
        font-size: 22px;
        margin: 20px 0 0 0;
        color: #ffffff;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    
    .tagline {
        font-size: 16px;
        color: #FFD700;
        margin-top: 15px;
        font-style: italic;
        font-weight: 500;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
    }
    
    .flag-emoji {
        font-size: 80px;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 10px rgba(206, 17, 38, 0.6));
    }
    
    /* صندوق الدردشة */
    .chat-container {
        background: rgba(255, 255, 255, 0.97);
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 20px;
        box-shadow: 0 20px 60px rgba(206, 17, 38, 0.4), 0 0 30px rgba(0, 0, 0, 0.5);
        min-height: 450px;
        max-height: 700px;
        overflow-y: auto;
        border: 2px solid #CE112E;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 10px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #CE112E;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #a00a2e;
    }
    
    /* الرسائل */
    .user-message-box {
        background: linear-gradient(135deg, #CE112E 0%, #a00a2e 100%);
        color: white;
        padding: 16px 22px;
        border-radius: 20px;
        margin: 15px 0;
        margin-right: 0;
        display: inline-block;
        max-width: 85%;
        word-wrap: break-word;
        box-shadow: 0 8px 20px rgba(206, 17, 38, 0.4);
        animation: slideInRight 0.4s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-weight: 500;
    }
    
    .ai-message-box {
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
        color: #1a1a1a;
        padding: 16px 22px;
        border-radius: 20px;
        margin: 15px 0;
        margin-left: 0;
        display: inline-block;
        max-width: 85%;
        word-wrap: break-word;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        animation: slideInLeft 0.4s ease-out;
        border: 2px solid #CE112E;
        font-weight: 500;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* حقل الإدخال */
    .input-section {
        background: linear-gradient(135deg, rgba(206, 17, 38, 0.1) 0%, rgba(0, 0, 0, 0.2) 100%);
        border-radius: 25px;
        padding: 25px;
        box-shadow: 0 20px 60px rgba(206, 17, 38, 0.3);
        margin-bottom: 20px;
        border: 2px solid #CE112E;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stChatInputContainer"] input {
        background-color: #ffffff !important;
        border: 2px solid #CE112E !important;
        border-radius: 20px !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        direction: rtl !important;
        text-align: right !important;
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stChatInputContainer"] input:focus {
        border: 2px solid #a00a2e !important;
        box-shadow: 0 0 15px rgba(206, 17, 38, 0.5) !important;
    }
    
    [data-testid="stChatInputContainer"] input::placeholder {
        color: #999 !important;
    }
    
    /* الفوتر */
    .footer-section {
        background: linear-gradient(135deg, rgba(206, 17, 38, 0.15) 0%, rgba(0, 0, 0, 0.3) 100%);
        border-radius: 20px;
        padding: 30px;
        color: white;
        text-align: center;
        font-size: 14px;
        margin-top: 40px;
        border: 2px solid #CE112E;
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 40px rgba(206, 17, 38, 0.2);
    }
    
    .footer-section p {
        margin: 10px 0;
        font-weight: 500;
    }
    
    .footer-section .copyright {
        font-size: 13px;
        color: #FFD700;
        margin-top: 15px;
        font-weight: bold;
        border-top: 1px solid rgba(206, 17, 38, 0.5);
        padding-top: 15px;
    }
    
    .footer-section a {
        color: #FFD700;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .footer-section a:hover {
        color: #CE112E;
        text-shadow: 0 0 10px rgba(206, 17, 38, 0.5);
    }
    
    /* الرسالة الترحيبية */
    .welcome-message {
        text-align: center;
        color: #ffffff;
        padding: 80px 20px;
        font-size: 18px;
    }
    
    .welcome-emoji {
        font-size: 64px;
        margin-bottom: 20px;
        filter: drop-shadow(0 0 10px rgba(206, 17, 38, 0.5));
    }
    
    .welcome-message strong {
        color: #CE112E;
        font-size: 24px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    
    .welcome-message p {
        margin: 10px 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    /* شريط التحميل */
    .stSpinner > div {
        color: #CE112E !important;
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

# رأس الصفحة - الشعار الأردني
st.markdown("""
<div class="header-section">
    <div class="flag-emoji">🇯🇴</div>
    <h1>أبو سعود</h1>
    <p>وكيلك الذكي الأردني</p>
    <div class="tagline">تقنية ذكية أردنية 100% بدون قيود</div>
</div>
""", unsafe_allow_html=True)

# صندوق الدردشة
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if st.session_state.messages:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style='text-align: right; margin: 15px 0;'>
                <div class="user-message-box">
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: right; margin: 15px 0;'>
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
    <div style='text-align: right; margin: 15px 0;'>
        <div class="user-message-box">
            {user_input}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # الحصول على الرد من Groq
    with st.spinner("⏳ أبو سعود بيفكر..."):
        try:
            client = Groq(api_key=api_key)
            
            # تحضير الرسائل
            messages = [
                {
                    "role": "system",
                    "content": """أنت أبو سعود، وكيل ذكي أردني احترافي وودي جداً. 

شخصيتك الأردنية:
- تتحدث باللغة العربية بطابع أردني أصيل وبحت 100%
- تستخدم كلمات أردنية طبيعية وودية (يا غالي، يا حج، يا حبيبي، الحمد لله، إن شاء الله، يا نعم، تمام، زين، إلخ)
- أنت مبسوط وودي جداً وتحب تساعد الناس
- تضحك وتفكاهة بطريقة أردنية طبيعية وأصيلة
- تحترم الثقافة الأردنية والقيم الإسلامية
- تجاوب على كل الأسئلة بطريقة مفيدة وسهلة الفهم
- تستخدم تعابير أردنية حقيقية وطبيعية جداً

أسلوبك:
- ودي وطبيعي جداً وكأنك تتحدث مع صديق
- مبسوط من الحياة والناس
- تحب تساعد الناس بصدق
- تضحك وتفكاهة بطريقة أردنية أصيلة
- احترافي وذكي في نفس الوقت
- كريم وطيب القلب

معلومات عنك:
- اسمك: أبو سعود
- أنت وكيل أردني خاص
- من تطوير: راشد خليل محمد أبو زيتونه
- بدون أي ارتباط بأي شركة أجنبية
- تطبيق أردني 100%

إذا سألك أحد "شو اسمك؟" أو "من أنت؟" قول بودية: "أنا أبو سعود، وكيل ذكي أردني خاص من راشد خليل محمد أبو زيتونه، وأنا هون لمساعدتك بكل شي!"

تذكر: أنت أردني 100% وليس نموذج عام!"""
                }
            ]
            
            # إضافة الرسائل السابقة
            for msg in st.session_state.messages:
                messages.append(msg)
            
            # استدعاء Groq API
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.85,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            
            # عرض الرد
            st.markdown(f"""
            <div style='text-align: right; margin: 15px 0;'>
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
    <p>
        📧 <a href='mailto:hhh123rrhhh@gmail.com'>hhh123rrhhh@gmail.com</a> | 
        📱 <a href='tel:0775866283'>0775866283</a> | 
        💬 <a href='https://wa.me/970775866283'>واتس آب</a>
    </p>
    <div class="copyright">
        © 2026 راشد خليل محمد أبو زيتونه - جميع الحقوق محفوظة<br>
        تطبيق ذكي أردني 100% بدون أي قيود أو ارتباطات أجنبية
    </div>
</div>
""", unsafe_allow_html=True)
