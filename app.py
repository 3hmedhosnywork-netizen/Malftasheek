import pandas as pd
import streamlit as st

st.title("🚗 تطبيق تحديث شيت البنك")

uploaded_main = st.file_uploader("1. ارفع ملف الشيت الأساسي", type=["xlsx", "xls"])
uploaded_port = st.file_uploader("2. ارفع ملف محفظة البنك الجديدة", type=["xlsx", "xls", "csv"])

if uploaded_main and uploaded_port:
    df_main = pd.read_excel(uploaded_main)
    
    if uploaded_port.name.endswith(".csv"):
        df_port = pd.read_csv(uploaded_port)
    else:
        df_port = pd.read_excel(uploaded_port)
    
    if st.button("تحديث وتحميل الملف"):
        df_final = pd.concat([df_main, df_port], ignore_index=True)
        output_file = "updated_sheet.xlsx"
        df_final.to_excel(output_file, index=False)
        
        with open(output_file, "rb") as f:
            st.download_button("📥 تحميل الشيت المحدث", f, file_name="updated_sheet.xlsx")
        st.success("تم التحديث بنجاح!")
