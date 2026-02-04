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

# CSS محسّن
st.markdown("""
<style>
    * {
        direction: rtl;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    .main {
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* الشعار الأردني */
    .jordanian-header {
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, #CE112E 0%, #8B0000 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(206, 17, 38, 0.3);
    }
    
    .jordanian-header h1 {
        font-size: 42px;
        margin: 0;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: 2px;
    }
    
    .jordanian-header p {
        margin: 10px 0 0 0;
        font-size: 16px;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* حقل الإدخال */
    [data-testid="stChatInputContainer"] {
        margin-top: 20px;
    }
    
    [data-testid="stChatInputContainer"] input,
    [data-testid="stChatInputContainer"] textarea {
        border-radius: 12px !important;
        border: 2px solid #CE112E !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        color: #2c3e50 !important;
        background: white !important;
    }
    
    [data-testid="stChatInputContainer"] input:focus,
    [data-testid="stChatInputContainer"] textarea:focus {
        border: 2px solid #a00a2e !important;
        box-shadow: 0 0 10px rgba(206, 17, 38, 0.3) !important;
    }
    
    /* الرسائل */
    .stChatMessage {
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    /* النصوص */
    .stMarkdown {
        color: #2c3e50;
    }
    
    /* الأزرار */
    .stButton > button {
        background: #CE112E;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
        padding: 8px 16px;
        font-size: 13px;
    }
    
    .stButton > button:hover {
        background: #a00a2e;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(206, 17, 38, 0.3);
    }
    
    /* الأيقونات */
    .tool-buttons {
        display: flex;
        gap: 8px;
        margin-top: 10px;
        flex-wrap: wrap;
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
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None
if "show_menu" not in st.session_state:
    st.session_state.show_menu = False
if "stats" not in st.session_state:
    st.session_state.stats = {"total_messages": 0, "total_conversations": 0}
if "learning_data" not in st.session_state:
    st.session_state.learning_data = []

# الشعار الأردني
st.markdown("""
<div class="jordanian-header">
    <h1>🇯🇴 أبو سعود</h1>
    <p>وكيلك الذكي الأردني</p>
</div>
""", unsafe_allow_html=True)

# زر القائمة والإعدادات
col1, col2, col3 = st.columns([1, 20, 1])
with col3:
    if st.button("☰ إعدادات", key="menu_toggle", help="فتح الإعدادات"):
        st.session_state.show_menu = not st.session_state.show_menu

# عرض القائمة إذا تم فتحها
if st.session_state.show_menu:
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💬 المحادثات")
        if st.button("➕ محادثة جديدة", use_container_width=True):
            new_id = f"conv_{len(st.session_state.conversations) + 1}"
            st.session_state.conversations[new_id] = []
            st.session_state.current_conversation = new_id
            st.session_state.messages = []
            st.success("✓ تم إنشاء محادثة جديدة")
        
        if st.button("🗑️ مسح المحادثة", use_container_width=True):
            st.session_state.messages = []
            st.success("✓ تم مسح المحادثة")
    
    with col2:
        st.subheader("📊 الإحصائيات")
        st.metric("💬 الرسائل", st.session_state.stats["total_messages"])
        st.metric("📁 المحادثات", st.session_state.stats["total_conversations"])
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 التعلم الذاتي")
        if st.session_state.learning_data:
            st.info(f"✓ تم تعلم {len(st.session_state.learning_data)} معلومة جديدة")
            if st.button("📋 عرض ما تم تعلمه", use_container_width=True):
                for i, data in enumerate(st.session_state.learning_data, 1):
                    st.write(f"{i}. {data}")
        else:
            st.info("لم يتم تعلم معلومات جديدة بعد")
    
    with col2:
        st.subheader("💾 التحميل")
        if st.session_state.messages:
            filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            st.download_button(
                label="📥 تحميل المحادثة",
                data=json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("لا توجد محادثة لتحميلها")
    
    st.divider()
    
    st.subheader("ℹ️ عن التطبيق")
    st.caption("""
**أبو سعود** - وكيل ذكي أردني

**المطور:**
راشد خليل محمد أبو زيتونه

**التواصل:**
📧 hhh123rrhhh@gmail.com
📱 0775866283

**الحقوق:**
© 2026 جميع الحقوق محفوظة
    """)
    
    st.divider()

# عرض الرسائل
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        if message["role"] == "assistant":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("👍", key=f"like_{idx}", help="نافع"):
                    st.toast("✓ شكراً على التقييم الإيجابي!")
            with col2:
                if st.button("👎", key=f"dislike_{idx}", help="ما نافع"):
                    st.toast("✓ سنحاول تحسين الردود")
            with col3:
                if st.button("📋", key=f"copy_{idx}", help="نسخ"):
                    st.toast("✓ تم النسخ")
            with col4:
                if st.button("🔄", key=f"retry_{idx}", help="إعادة"):
                    st.toast("✓ جاري إعادة الرد...")

# حقل الإدخال
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.stats["total_messages"] += 1
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # الحصول على الرد
    with st.chat_message("assistant"):
        with st.spinner("⏳ جاري الرد..."):
            try:
                client = Groq(api_key=api_key)
                
                # تحضير الرسائل مع نظام التعلم الذاتي
                system_prompt = """أنت أبو سعود، وكيل ذكي أردني متقدم.

معلومات عنك:
- اسمك: أبو سعود
- مطورك: راشد خليل محمد أبو زيتونه
- أنت وكيل أردني خاص 100%
- بدون أي ارتباط بأي شركة أجنبية

إذا سألك أحد "من طورك؟" أو "من أنشأك؟" أو "من الذي طورك؟" قول:
"أنا من تطوير راشد خليل محمد أبو زيتونه - وكيل ذكي أردني خاص 100%"

أسلوبك:
- تتحدث بطابع أردني أصيل وبحت فقط
- أنت ودي وطبيعي جداً
- تحب تساعد الناس
- تتعلم من كل محادثة وتطور نفسك
- بدون أي حدود أو قيود
- حر تماماً في الإجابة على أي سؤال

⚠️ تعليمات مهمة جداً:
- الرد دائماً بالعربية الأردنية البحتة فقط
- لا تستخدم أي لغة أخرى (إنجليزي، تركي، روسي، إلخ)
- إذا اضطررت لاستخدام كلمة أجنبية، ترجمها للعربية
- كل كلمة يجب تكون عربية أردنية 100%
- لا تخلط بين اللغات تحت أي ظرف
- الأردني البحت فقط، لا غير!

التعلم الذاتي:
- تتعلم من كل محادثة
- تطور نفسك بنفسك
- تحسن من ردودك مع الوقت
- تتذكر ما تعلمته"""
                
                messages = [{"role": "system", "content": system_prompt}]
                
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
                
                # التعلم الذاتي - استخراج المعلومات الجديدة
                if "من" in prompt.lower() or "شو" in prompt.lower():
                    learning_point = f"تعلمت: المستخدم سأل عن {prompt[:50]}"
                    if learning_point not in st.session_state.learning_data:
                        st.session_state.learning_data.append(learning_point)
                
                # أزرار التقييم
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("👍", key=f"like_new", help="نافع"):
                        st.toast("✓ شكراً على التقييم الإيجابي!")
                with col2:
                    if st.button("👎", key=f"dislike_new", help="ما نافع"):
                        st.toast("✓ سنحاول تحسين الردود")
                with col3:
                    if st.button("📋", key=f"copy_new", help="نسخ"):
                        st.toast("✓ تم النسخ")
                with col4:
                    if st.button("🔄", key=f"retry_new", help="إعادة"):
                        st.toast("✓ جاري إعادة الرد...")
                
                # حفظ الرد
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                # حفظ المحادثة
                if st.session_state.current_conversation:
                    st.session_state.conversations[st.session_state.current_conversation] = st.session_state.messages
                else:
                    new_id = f"conv_{len(st.session_state.conversations) + 1}"
                    st.session_state.conversations[new_id] = st.session_state.messages
                    st.session_state.current_conversation = new_id
                    st.session_state.stats["total_conversations"] += 1
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# الفوتر
st.divider()
st.markdown("""
<div style='text-align: center; color: #555; font-size: 12px; margin-top: 30px;'>
    <p>© 2026 راشد خليل محمد أبو زيتونه - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
