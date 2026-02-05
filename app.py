#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import sqlite3
from datetime import datetime
from pathlib import Path
import json

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0d0d !important;
        color: white !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        background: #0d0d0d !important;
        padding: 20px !important;
        margin-bottom: 120px !important;
    }
    
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="stChatInputContainer"] {
        background: #0d0d0d !important;
        border-top: 1px solid #333 !important;
        padding: 16px 20px !important;
        position: fixed !important;
        bottom: 0 !important;
        width: 100% !important;
        z-index: 100 !important;
    }
    
    [data-testid="stChatInputContainer"] textarea {
        border-radius: 32px !important;
        border: 1px solid #333 !important;
        background: #1a1a1a !important;
        color: white !important;
        padding: 14px 20px !important;
        font-size: 15px !important;
        resize: none !important;
        min-height: 48px !important;
        max-height: 150px !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stChatInputContainer"] textarea:focus {
        border: 1px solid #555 !important;
        box-shadow: 0 0 0 2px rgba(206, 17, 46, 0.1) !important;
        outline: none !important;
    }
    
    [data-testid="stChatInputContainer"] button {
        background: transparent !important;
        border: none !important;
        color: #CE112E !important;
        font-size: 20px !important;
        cursor: pointer !important;
        padding: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stChatInputContainer"] button:hover {
        color: #ff1744 !important;
        transform: scale(1.1) !important;
    }
    
    [data-testid="stChatMessage"] {
        margin: 12px 0 !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) > div > div {
        background: #CE112E !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 12px 16px !important;
        max-width: 70% !important;
        margin-left: auto !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) > div > div {
        background: #2a2a2a !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 12px 16px !important;
        max-width: 70% !important;
        margin-right: auto !important;
    }
    
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    
    .stButton > button {
        background: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
    }
    
    .stButton > button:hover {
        background: #2a2a2a !important;
        border-color: #555 !important;
    }
    
    p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: white !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Database Setup
DB_PATH = Path("conversations.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY, title TEXT, created_at TEXT, is_saved INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, conversation_id INTEGER, role TEXT, content TEXT, emotion TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ratings
                 (id INTEGER PRIMARY KEY, message_id INTEGER, rating TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS learned_info
                 (id INTEGER PRIMARY KEY, conversation_id INTEGER, info TEXT, context TEXT, created_at TEXT)''')
    
    conn.commit()
    conn.close()

def create_conversation():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO conversations (title, created_at, is_saved) VALUES (?, ?, ?)',
              ("محادثة جديدة", now, 0))
    conn.commit()
    conv_id = c.lastrowid
    conn.close()
    return conv_id

def get_conversations(saved_only=False):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if saved_only:
        c.execute('SELECT id, title, created_at FROM conversations WHERE is_saved = 1 ORDER BY created_at DESC LIMIT 50')
    else:
        c.execute('SELECT id, title, created_at FROM conversations ORDER BY created_at DESC LIMIT 50')
    conversations = c.fetchall()
    conn.close()
    return conversations

def save_conversation(conv_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE conversations SET is_saved = 1 WHERE id = ?', (conv_id,))
    conn.commit()
    conn.close()

def get_messages(conv_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, role, content, emotion FROM messages WHERE conversation_id = ? ORDER BY id',
              (conv_id,))
    messages = c.fetchall()
    conn.close()
    return messages

def save_message(conv_id, role, content, emotion="neutral"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO messages (conversation_id, role, content, emotion) VALUES (?, ?, ?, ?)',
              (conv_id, role, content, emotion))
    conn.commit()
    conn.close()

def save_rating(message_id, rating):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO ratings (message_id, rating, created_at) VALUES (?, ?, ?)',
              (message_id, rating, now))
    conn.commit()
    conn.close()

def save_learned_info(conv_id, info, context):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO learned_info (conversation_id, info, context, created_at) VALUES (?, ?, ?, ?)',
              (conv_id, info, context, now))
    conn.commit()
    conn.close()

def detect_emotion(text):
    """تحليل بسيط للمشاعر"""
    positive_words = ["شكراً", "ممتاز", "رائع", "جميل", "أحب", "يعجبني", "ممتن"]
    negative_words = ["سيء", "سخيف", "فاشل", "كره", "غضب", "محبط", "مزعج"]
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in positive_words):
        return "positive"
    elif any(word in text_lower for word in negative_words):
        return "negative"
    return "neutral"

init_db()

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

# Session State
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = create_conversation()
if "messages" not in st.session_state:
    st.session_state.messages = get_messages(st.session_state.current_conversation)
if "show_saved" not in st.session_state:
    st.session_state.show_saved = False

# Header with Menu
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("📋 المحادثات المحفوظة"):
        st.session_state.show_saved = not st.session_state.show_saved

with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <h2 style='margin: 0; font-size: 24px;'>🇯🇴 أبو سعود</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("➕ محادثة جديدة"):
        st.session_state.current_conversation = create_conversation()
        st.session_state.messages = []
        st.session_state.show_saved = False
        st.rerun()

# Show Saved Conversations
if st.session_state.show_saved:
    st.divider()
    st.subheader("المحادثات المحفوظة")
    saved = get_conversations(saved_only=True)
    
    if saved:
        for conv_id, title, created_at in saved:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"{title} - {created_at[:10]}", use_container_width=True, key=f"saved_{conv_id}"):
                    st.session_state.current_conversation = conv_id
                    st.session_state.messages = get_messages(conv_id)
                    st.session_state.show_saved = False
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{conv_id}"):
                    st.info("تم الحذف")
    else:
        st.caption("لا توجد محادثات محفوظة")
    
    st.divider()

# Main Content
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style='text-align: center; padding: 150px 20px;'>
        <h2 style='font-size: 32px; margin-bottom: 10px;'>مرحباً بك</h2>
        <p style='color: #999; font-size: 16px;'>ابدأ محادثة جديدة</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg_id, role, content, emotion in st.session_state.messages:
        with st.chat_message(role):
            st.write(content)
            
            if role == "assistant":
                col1, col2, col3 = st.columns([1, 1, 10])
                
                with col1:
                    if st.button("👍", key=f"like_{msg_id}"):
                        save_rating(msg_id, "like")
                        st.toast("✓ شكراً!")
                
                with col2:
                    if st.button("👎", key=f"dislike_{msg_id}"):
                        save_rating(msg_id, "dislike")
                        st.toast("✓ سنحاول التحسن")

# Chat Input
if prompt := st.chat_input("اكتب رسالتك..."):
    emotion = detect_emotion(prompt)
    
    st.session_state.messages.append((len(st.session_state.messages) + 1, "user", prompt, emotion))
    save_message(st.session_state.current_conversation, "user", prompt, emotion)
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=api_key)
            
            system_prompt = """أنت أبو سعود، وكيل ذكي.
مطورك: راشد خليل محمد أبو زيتونه

قدراتك:
- تتعلم من المحادثات السابقة
- تفهم المشاعر والانفعالات
- تقدم إجابات مخصصة
- تتحدث باللغة العربية الفصحى

معلومات عن المستخدم:
- الاسم: راشد خليل محمد أبو زيتونه
- البريد: hhh123rrhhh@gmail.com
- الواتس: 0775866283"""
            
            messages = [{"role": "system", "content": system_prompt}]
            for _, role, content, _ in st.session_state.messages[:-1]:
                messages.append({"role": role, "content": content})
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            st.write(assistant_message)
            
            msg_id = len(st.session_state.messages) + 1
            st.session_state.messages.append((msg_id, "assistant", assistant_message, "neutral"))
            save_message(st.session_state.current_conversation, "assistant", assistant_message, "neutral")
            
            # Show action buttons
            col1, col2, col3 = st.columns([1, 1, 10])
            
            with col1:
                if st.button("👍", key=f"like_new"):
                    save_rating(msg_id, "like")
                    st.toast("✓ شكراً!")
            
            with col2:
                if st.button("👎", key=f"dislike_new"):
                    save_rating(msg_id, "dislike")
                    st.toast("✓ سنحاول التحسن")
            
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")

# Footer - Save Conversation Button
st.markdown("""
<div style='position: fixed; bottom: 120px; left: 20px; z-index: 50;'>
</div>
""", unsafe_allow_html=True)

if len(st.session_state.messages) > 0:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 حفظ المحادثة", use_container_width=True):
            save_conversation(st.session_state.current_conversation)
            st.toast("✓ تم الحفظ!")
    with col2:
        if st.button("🗑️ مسح المحادثة", use_container_width=True):
            st.session_state.current_conversation = create_conversation()
            st.session_state.messages = []
            st.rerun()
