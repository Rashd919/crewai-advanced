"""
🎨 واجهة Streamlit الحديثة
نظام CrewAI المتقدم - واجهة احترافية
"""

import streamlit as st
from crew import execute_query, execute_research, execute_analysis, execute_full
from dotenv import load_dotenv
import os
from datetime import datetime

# تحميل متغيرات البيئة
load_dotenv()

# إعدادات الصفحة
st.set_page_config(
    page_title="CrewAI Advanced",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS عصري وحديث
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    /* الخلفية الرئيسية */
    .stApp {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a3e 50%, #0f3460 100%);
    }
    
    /* العنوان الرئيسي */
    .main-header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        border-radius: 25px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3em;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2em;
        margin: 12px 0 0 0;
    }
    
    /* صناديق المعلومات */
    .info-box {
        background: rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.5);
        background: linear-gradient(135deg, #00ff88 0%, #00cc66 100%);
    }
    
    /* حقول الإدخال */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #00d4ff;
        padding: 12px 16px;
        background: #1a1a2e;
        color: #e8f0ff;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00ff88;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    
    /* الفاصل */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
        margin: 25px 0;
    }
    
    /* نتائج البحث */
    .result-box {
        background: rgba(45, 53, 97, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #00d4ff;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("""
<div class="main-header">
    <h1>🤖 CrewAI Advanced</h1>
    <p>نظام ذكي متقدم للبحث والتحليل - فريق من الوكلاء الذكيين</p>
</div>
""", unsafe_allow_html=True)

# الشريط الجانبي
with st.sidebar:
    st.markdown("## ⚙️ الإعدادات")
    
    # معلومات النظام
    st.markdown("""
    ### 🎯 معلومات النظام
    - **الإصدار:** 1.0.0
    - **الوقت:** """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
    - **الحالة:** ✅ نشط
    """)
    
    st.divider()
    
    # نوع المهمة
    task_type = st.selectbox(
        "اختر نوع المهمة:",
        ["🔍 بحث متقدم", "📊 تحليل", "🎯 خط أنابيب كامل"]
    )
    
    st.divider()
    
    # معلومات الوكلاء
    st.markdown("""
    ### 👥 الوكلاء الذكيين
    
    **1. الباحث الخارق** 🔍
    - البحث في الويب
    - فيديوهات YouTube
    - استخراج المحتوى
    
    **2. المحلل التقني** 📊
    - تحليل البيانات
    - الصياغة الاحترافية
    - التنظيم والتقارير
    
    **3. مدير المشروع** 📋
    - التنسيق والإشراف
    - ضمان الجودة
    - القرارات الاستراتيجية
    """)

# المحتوى الرئيسي
st.markdown("## 🚀 ابدأ البحث الآن")

# تبويبات
tab1, tab2, tab3 = st.tabs(["🔍 البحث", "📊 التحليل", "🎯 خط أنابيب"])

with tab1:
    st.markdown("### البحث المتقدم في الويب")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "أدخل استعلام البحث:",
            placeholder="مثال: أحدث تطورات الذكاء الاصطناعي...",
            key="search_query"
        )
    
    with col2:
        search_button = st.button("🔍 بحث", use_container_width=True)
    
    if search_button and query:
        with st.spinner("⏳ جاري البحث..."):
            try:
                results = execute_research(query)
                st.markdown("""
                <div class="result-box">
                """ + results + """
                </div>
                """, unsafe_allow_html=True)
                st.success("✅ تم البحث بنجاح!")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

with tab2:
    st.markdown("### التحليل المتقدم")
    
    research_input = st.text_area(
        "أدخل نتائج البحث للتحليل:",
        placeholder="الصق نتائج البحث هنا...",
        height=200,
        key="analysis_input"
    )
    
    if st.button("📊 تحليل", use_container_width=True):
        if research_input:
            with st.spinner("⏳ جاري التحليل..."):
                try:
                    results = execute_analysis(research_input)
                    st.markdown("""
                    <div class="result-box">
                    """ + results + """
                    </div>
                    """, unsafe_allow_html=True)
                    st.success("✅ تم التحليل بنجاح!")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى إدخال نتائج البحث أولاً")

with tab3:
    st.markdown("### خط الأنابيب الكامل")
    
    st.info("""
    ℹ️ **خط الأنابيب الكامل:**
    1. البحث المتقدم في الويب
    2. التحليل الشامل
    3. التنسيق والتقرير النهائي
    """)
    
    full_query = st.text_input(
        "أدخل الاستعلام:",
        placeholder="مثال: شرح تقنية البلوكتشين...",
        key="full_query"
    )
    
    if st.button("🎯 تنفيذ خط أنابيب", use_container_width=True):
        if full_query:
            with st.spinner("⏳ جاري المعالجة (قد يستغرق وقتاً)..."):
                try:
                    results = execute_full(full_query)
                    
                    # عرض النتائج
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("#### 🔍 البحث")
                        if results["research"]:
                            st.text(results["research"][:300] + "...")
                    
                    with col2:
                        st.markdown("#### 📊 التحليل")
                        if results["analysis"]:
                            st.text(results["analysis"][:300] + "...")
                    
                    with col3:
                        st.markdown("#### 📋 النتيجة النهائية")
                        if results["final_result"]:
                            st.text(results["final_result"][:300] + "...")
                    
                    st.divider()
                    
                    # عرض النتائج الكاملة
                    st.markdown("### 📄 النتائج الكاملة")
                    
                    with st.expander("🔍 نتائج البحث"):
                        st.write(results["research"])
                    
                    with st.expander("📊 نتائج التحليل"):
                        st.write(results["analysis"])
                    
                    with st.expander("📋 النتيجة النهائية"):
                        st.write(results["final_result"])
                    
                    st.success("✅ تم المعالجة بنجاح!")
                    
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
        else:
            st.warning("⚠️ يرجى إدخال استعلام أولاً")

# الفوتر
st.divider()
st.markdown("""
<div style='text-align: center; padding: 25px; color: #666; font-size: 0.9em;'>
    <p>© 2026 CrewAI Advanced - جميع الحقوق محفوظة</p>
    <p style='margin-top: 8px;'>نظام ذكي متقدم للبحث والتحليل</p>
</div>
""", unsafe_allow_html=True)
