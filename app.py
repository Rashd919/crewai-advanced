import streamlit as st
import google.generativeai as genai

st.title("⚡ فحص قوة الرعد")

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # هذا السطر رح يطبع لنا كل الموديلات اللي مفتاحك بيقدر يشوفها
        models = [m.name for m in genai.list_models()]
        st.write("✅ المفتاح شغال! الموديلات المتاحة لك هي:")
        st.json(models)
        
        # اختيار أول موديل متاح تلقائياً عشان ما يعطي 404
        available_model = models[0] if models else "gemini-pro"
        st.info(f"سيتم تشغيل الرعد باستخدام: {available_model}")
        
    except Exception as e:
        st.error(f"❌ مشكلة في المفتاح (API Key): {str(e)}")
else:
    st.warning("أدخل المفتاح في Secrets")
