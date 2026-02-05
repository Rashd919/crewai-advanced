#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import sqlite3
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS - تصميم بسيط جداً
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
        margin-right: 260px !important;
        margin-bottom: 120px !important;
    }
    
    [data-testid="stSidebar"] {
        background: #1a1a1a !important;
        border-left: 1px solid #333 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* Chat Input Container */
    [data-testid="stChatInputContainer"] {
        background: #0d0d0d !important;
        border-top: 1px solid #333 !important;
        padding: 16px 20px !important;
        position: fixed !important;
        bottom: 0 !important;
        width: calc(100% - 260px) !important;
        right: 260px !important;
        z-index: 100 !important;
    }
    
    /* Textarea - بيضوي طويل */
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
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stChatInputContainer"] textarea:focus {
        border: 1px solid #555 !important;
        box-shadow: 0 0 0 2px rgba(206, 17, 46, 0.1) !important;
        outline: none !important;
    }
    
    [data-testid="stChatInputContainer"] textarea::placeholder {
        color: #666 !important;
    }
    
    /* Send Button */
    [data-testid="stChatInputContainer"] button {
        background: transparent !important;
        border: none !important;
        color: #CE112E !important;
        font-size: 20px !important;
        cursor: pointer !important;
        padding: 8px !important;
        transition: all 0.2s ease !important;
        margin-left: 8px !important;
    }
    
    [data-testid="stChatInputContainer"] button:hover {
        color: #ff1744 !important;
        transform: scale(1.1) !important;
    }
    
    /* Messages */
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
    
    /* Buttons */
    .stButton > button {
        background: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #2a2a2a !important;
        border-color: #555 !important;
    }
    
    /* Text */
    p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: white !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* Hide Streamlit Elements */
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
                 (id INTEGER PRIMARY KEY, title TEXT, created_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, conversation_id INTEGER, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def create_conversation():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO conversations (title, created_at) VALUES (?, ?)',
              ("محادثة جديدة", now))
    conn.commit()
    conv_id = c.lastrowid
    conn.close()
    return conv_id

def get_conversations():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, title FROM conversations ORDER BY id DESC LIMIT 20')
    conversations = c.fetchall()
    conn.close()
    return conversations

def get_messages(conv_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id',
              (conv_id,))
    messages = c.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in messages]

def save_message(conv_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
              (conv_id, role, content))
    conn.commit()
    conn.close()

init_db()

# Get API key
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

# Sidebar
with st.sidebar:
    st.markdown("### 🇯🇴 أبو سعود")
    
    if st.button("➕ محادثة جديدة", use_container_width=True):
        st.session_state.current_conversation = create_conversation()
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.subheader("المحادثات السابقة")
    conversations = get_conversations()
    for conv_id, title in conversations:
        if st.button(f"{title}", use_container_width=True, key=f"conv_{conv_id}"):
            st.session_state.current_conversation = conv_id
            st.session_state.messages = get_messages(conv_id)
            st.rerun()

# Main Content
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style='text-align: center; padding: 150px 20px;'>
        <h1 style='font-size: 40px; margin-bottom: 10px;'>أبو سعود</h1>
        <p style='color: #999; font-size: 16px;'>وكيلك الذكي</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat Input
if prompt := st.chat_input("اكتب رسالتك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(st.session_state.current_conversation, "user", prompt)
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=api_key)
            
            system_prompt = """أنت أبو سعود، وكيل ذكي.
مطورك: راشد خليل محمد أبو زيتونه
تتحدث باللغة العربية الفصحى فقط."""
            
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(st.session_state.messages)
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            st.write(assistant_message)
            
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            save_message(st.session_state.current_conversation, "assistant", assistant_message)
            
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")
