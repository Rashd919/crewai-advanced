import streamlit as st
import time

# تغيير لون عنوان التطبيق
st.title("الرعد", anchor=False)

# إضافة عداد ذكي في الشريط الجانبي
counter = 0
st.sidebar.write("عدد الرسائل الصادرة:")
with st.sidebar:
    while True:
        st.sidebar.write(counter)
        time.sleep(1)
        counter += 1

# تطبيق أمر التطور (UPDATE_CODE)
if st.button("تحديث التطبيق"):
    st.success("التطبيق تم تحديثه بنجاح!")