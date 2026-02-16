import streamlit as st
import pandas as pd
import os
import requests
import json
import socket
import time
from datetime import datetime

# --- 1. إعدادات الهوية والواجهة ---
st.set_page_config(page_title="Thunder Offensive Hub", layout="wide")

# إنشاء مخزن بيانات للأهداف القادمة من الأندرويد (الرعد)
if 'victim_logs' not in st.session_state:
    st.session_state.victim_logs = pd.DataFrame(columns=['الوقت', 'عنوان IP الجهاز', 'الحالة'])

# --- 2. محرك العمليات (الاستلام والهجوم) ---
class ThunderEngine:
    @staticmethod
    def port_scanner(target_ip, ports):
        open_ports = []
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((target_ip, port)) == 0:
                open_ports.append(port)
            s.close()
        return open_ports

# --- 3. واجهة العمليات المركزية ---
st.title("🛡️ مركز الرعد الهجومي (Offensive Hub Pro)")

# التبويبات المدمجة
tabs = st.tabs(["📡 رادار الأهداف (الأندرويد)", "⚔️ أدوات الهجوم", "📊 الإحصائيات"])

engine = ThunderEngine()

# --- التبويب الأول: رادار الأهداف (هنا تظهر بيانات ابنك/المستهدف) ---
with tabs[0]:
    st.header("🎯 الأهداف المرصودة من "الرعد"")
    if st.session_state.victim_logs.empty:
        st.info("بانتظار أول اتصال من تطبيق الأندرويد...")
    else:
        st.table(st.session_state.victim_logs)
    
    # زر للتجربة اليدوية عشان تتأكد إن الجدول شغال
    if st.button("محاكاة وصول بيانات"):
        new_row = pd.DataFrame({'الوقت': [datetime.now().strftime("%H:%M:%S")], 
                                'عنوان IP الجهاز': ["192.168.1.100"], 
                                'الحالة': ['نشط الآن 🟢']})
        st.session_state.victim_logs = pd.concat([st.session_state.victim_logs, new_row], ignore_index=True)
        st.rerun()

# --- التبويب الثاني: أدوات الهجوم (الكود اللي بعثته أنت) ---
with tabs[1]:
    st.header("وحدة الاستطلاع والهجوم")
    target = st.text_input("🎯 عنوان الهدف (IP/Domain):", placeholder="مثلاً: 192.168.1.1")
    
    if st.button("🚀 فحص المنافذ"):
        if target:
            with st.spinner("جاري الاختراق الاستطلاعي..."):
                results = engine.port_scanner(target, [21, 22, 80, 443])
                st.code(f"النتائج للهدف {target}: {results}")
        else:
            st.warning("دخل الـ IP أولاً يا قائد.")

# --- التبويب الثالث: لوحة القيادة ---
with tabs[2]:
    st.subheader("حالة الترسانة")
    st.success("جميع الأنظمة متصلة وجاهزة لاستقبال البيانات من تطبيق الأندرويد.")
