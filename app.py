
import streamlit as st

def set_background_image(image_url: str):
    """
    Sets a custom background image for the Streamlit application.
    This function injects CSS to target the main Streamlit app container.
    Streamlit's default component styling ensures that elements like text input boxes
    remain clearly visible against the new background due to their inherent contrast.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Streamlit Application ---

# Define the URL for your desired background image.
# You can replace this with any image URL (e.g., from Unsplash, your own hosted image, etc.).
# This example uses a subtle gradient image for good readability of content.
background_image_url = "https://images.unsplash.com/photo-1557682250-33bd709ff38f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1974&q=80"

# Apply the background image
set_background_image(background_image_url)

st.title("يا رعد، غير الخلفية!")
st.write("أهلاً بك في تطبيق Streamlit الجديد مع خلفية مخصصة.")

# A text input box is placed here to demonstrate its clear visibility
# Streamlit components typically have their own styling that provides sufficient
# contrast against various backgrounds.
user_input = st.text_input(
    "أدخل نصًا هنا للحفاظ على ظهوره بوضوح (صندوق الكتابة هذا يظل واضحًا):",
    "هذا صندوق نصي واضح على الخلفية الجديدة."
)

st.write(f"لقد أدخلت: {user_input}")

st.write("---")
st.header("محتوى إضافي")
st.write("هذا محتوى إضافي يظهر فوق الخلفية الجديدة.")

if st.button("اضغط هنا"):
    st.success("لقد ضغطت على الزر بنجاح!")

# Example of a sidebar to show it also adapts
st.sidebar.header("خيارات الشريط الجانبي")
st.sidebar.slider("اختر قيمة من 0 إلى 100:", 0, 100, 50)
st.sidebar.info("الشريط الجانبي يظهر أيضًا بوضوح.")
