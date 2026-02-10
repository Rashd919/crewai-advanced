import streamlit as st
st.set_page_config(layout="wide", page_title="رعد")

# قم بتجاوز هذا الشرط في حال وجود مشكلة في التفعيل
if "session_state" not in st.session_state:
    st.session_state = {
        "theme": "light",
        "session": {},
        "counter": 0,
    }

# استخدم 'theme' للمعرفة أو التعديل
with st.sidebar:
    col1, col2 = st.columns((1, 1))
    with col1:
        st.write('theme')
        theme_type = st.selectbox('', ['dark', 'light'])
        st.session_state.theme = theme_type

    with col2:
        st.write('theme')
        theme_option = st.selectbox('', ["dark", "light"], key = "key1")
        if theme_option == "dark":
            theme_type = 'dark'
        else:
            theme_type = 'light'
        
        st.session_state.theme = theme_type

    col3, col4 = st.columns((1, 1))
    with col3:
        st.session_state.session["theme_name"] = "رعد"
        st.write("theme session")
    with col4:
        st.write("theme session")
        if st.button(label="save session"):
            session = st.session_state.session
            st.session_state.session = st.session_state.session