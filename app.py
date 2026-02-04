#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🤖 CrewAI Advanced - محادثة ذكية
تطبيق بسيط وفعال للبحث والتحليل
"""

import streamlit as st
from datetime import datetime
import json

# إعدادات الصفحة
st.set_page_config(
    page_title="CrewAI Advanced",
    page_icon="🤖",
    layout="wide"
)

# CSS بسيط مثل ChatGPT
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }
    
    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: #f7f7f7;
    }
    
    .user-message {
        background: #10a37f;
        color: white;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 70%;
        margin-left: auto;
    }
    
    .assistant-message {
        background: #e5e5e5;
        color: #000;
        padding: 12px 16px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 70%;
    }
</style>
""", unsafe_allow_html=True)

# رأس الصفحة
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='margin: 0;'>🤖 CrewAI Advanced</h1>
        <p style='margin: 5px 0; color: #666;'>محادثة ذكية متقدمة</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# الشريط الجانبي
with st.sidebar:
    st.markdown("## 👤 معلومات المطور")
    st.markdown("""
    **الاسم:** راشد (Rashed)
    
    **البريد الإلكتروني:**
    📧 hhh123rrhhh@gmail.com
    
    **رقم الهاتف:**
    📱 0775866283
    
    **واتس آب:**
    💬 [تواصل معي](https://wa.me/970775866283)
    
    ---
    
    **جميع الحقوق محفوظة © 2026**
    **Rashed - CrewAI Advanced**
    """)
    
    st.divider()
    
    st.markdown("""
    ### ℹ️ معلومات النظام
    - **الوقت:** """ + datetime.now().strftime("%H:%M:%S") + """
    - **التاريخ:** """ + datetime.now().strftime("%Y-%m-%d") + """
    - **الحالة:** ✅ نشط
    - **الإصدار:** 1.0.0
    """)

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
messages_container = st.container()

with messages_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div style='text-align: right; margin: 10px 0;'>
                <div style='background: #10a37f; color: white; padding: 12px 16px; border-radius: 12px; display: inline-block; max-width: 70%;'>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: right; margin: 10px 0;'>
                <div style='background: #e5e5e5; color: #000; padding: 12px 16px; border-radius: 12px; display: inline-block; max-width: 70%;'>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

st.divider()

# حقل الإدخال
col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input(
        "أكتب رسالتك:",
        placeholder="اسأل عن أي شيء...",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("📤 إرسال", use_container_width=True)

# معالجة الرسالة
if send_button and user_input:
    # إضافة رسالة المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # معالجة الطلب
    response = ""
    
    # البحث عن الفيديوهات
    if "فيديو" in user_input or "youtube" in user_input.lower():
        response = f"""
✅ **تم استقبال طلب البحث عن فيديو**

📝 **الطلب:** {user_input}

🔍 **جاري البحث عن الفيديوهات ذات الصلة...**

📊 **النتائج:**
- 🎥 فيديو 1: شرح مفصل عن الموضوع
- 🎥 فيديو 2: دليل عملي خطوة بخطوة
- 🎥 فيديو 3: نصائح واستراتيجيات

✨ **يمكنك الضغط على أي فيديو لمشاهدته**
        """
    
    # الأسئلة العامة
    elif "كيف" in user_input or "ما" in user_input or "شنو" in user_input:
        response = f"""
✅ **تم استقبال سؤالك**

📝 **السؤال:** {user_input}

💭 **الإجابة:**

أنا وكيل ذكي متقدم يمكنني:
- 🔍 البحث عن المعلومات
- 🎥 جلب الفيديوهات
- 📊 تحليل البيانات
- ✍️ الإجابة على الأسئلة
- 💡 تقديم الاستشارات

كيف يمكنني مساعدتك أكثر؟
        """
    
    # الردود الافتراضية
    else:
        response = f"""
✅ **تم استقبال رسالتك**

📝 **الرسالة:** {user_input}

🤖 **الرد:**

شكراً على رسالتك! أنا هنا لمساعدتك في:
- 🔍 البحث والتحليل
- 🎥 جلب الفيديوهات من YouTube
- 📊 معالجة البيانات
- ✍️ الإجابة على الأسئلة

يمكنك أن تطلب مني:
- "ابحث عن فيديو لـ..."
- "اشرح لي..."
- "كيف أحل مشكلة..."
- "ما هو..."

كيف يمكنني مساعدتك؟
        """
    
    # إضافة رد الوكيل
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    
    # إعادة تحميل الصفحة
    st.rerun()

# الفوتر
st.divider()
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666; font-size: 0.85em;'>
    <p>© 2026 CrewAI Advanced - جميع الحقوق محفوظة لـ <strong>راشد</strong></p>
    <p style='margin: 8px 0;'>
        📧 <a href='mailto:hhh123rrhhh@gmail.com'>hhh123rrhhh@gmail.com</a> | 
        📱 0775866283 | 
        💬 <a href='https://wa.me/970775866283'>واتس آب</a>
    </p>
    <p style='margin: 8px 0; font-size: 0.8em;'>
        تطبيق ذكي متقدم للبحث والتحليل والمحادثة
    </p>
</div>
""", unsafe_allow_html=True)
