import streamlit as st

    # عنوان الواجهة
    st.title("الرعد - كوكيل سيادي")

    # زر تحليل الكود الحالي
    if st.button("تحليل الكود الحالي"):
        st.write("الواجهة الحالية لا تحتوي على أي كود.")
    """
    tree = ast.parse(code)
    st.write(ast.dump(tree))
