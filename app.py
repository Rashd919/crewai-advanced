
import streamlit as st
import google.generativeai as genai

# --- CSS لتعديل خلفية الصفحة والنص ---
# لون كحلي داكن: #0A1931 (مثال للون Midnight Blue الداكن)
# لون النص: أبيض ليكون مرئياً على الخلفية الداكنة
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0A1931; /* لون كحلي داكن */
        color: #FFFFFF; /* لون النص أبيض */
    }
    h1 {
        color: #E0E0E0; /* لون أفتح قليلاً للعنوان لتمييزه */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- نص الترحيب ---
st.markdown("<h1>أهلاً بك يا راشد في حصنك الرقمي</h1>", unsafe_allow_html=True)

# --- تضمين google-generativeai (يمكن إضافة المزيد من المنطق هنا لاحقاً) ---
# مثال لكيفية تهيئة المكتبة (ستحتاج إلى مفتاح API فعلي للاستخدام الحقيقي)
# genai.configure(api_key="YOUR_GOOGLE_API_KEY")

# يمكنك إضافة المزيد من مكونات Streamlit هنا
st.write("هنا يمكنك البدء في بناء تطبيقك باستخدام قدرات الذكاء الاصطناعي التوليدي.")
# مثال بسيط جداً لتأكيد وجود المكتبة، دون أي تفاعل معها
# model = genai.GenerativeModel('gemini-pro')
# st.write("تم تهيئة نموذج Generative AI.")
