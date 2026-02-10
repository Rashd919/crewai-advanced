import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# تعريف متغيرات
st.title("رعد")
st.write("مطور: راشد أبو سعود")

# تعريف بيانات
data = {
    "اسم": ["رعد", "عاصف", "رعد", "عاصف"],
    "عمر": [25, 30, 25, 30]
}

df = pd.DataFrame(data)

# عرض البيانات
st.write("بيانات:")
st.write(df)

# رسم диаграмة بار
st.write("رسم диаграмة بار:")
sns.barplot(x="اسم", y="عمر", data=df)
plt.title("رسم диаграмة بار")
plt.xlabel("اسم")
plt.ylabel("عمر")
st.pyplot(plt.gcf())

# عرض رسالة
st.write("رعد")
