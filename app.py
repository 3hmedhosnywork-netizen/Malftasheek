import streamlit as st
import openpyxl
import re

st.set_page_config(page_title="تحديث الشيت الذكي بدقة", page_icon="🚗")
st.title("🚗 نظام إدارة وتحديث شيت البنك الذكي")

def clean_plate_text(text):
    if not text:
        return ""
    text = str(text).strip()
    chars = "".join(re.findall(r'[\u0600-\u06FF\d]', text))
    return chars

if 'step' not in st.session_state:
    st.session_state.step = 1

uploaded_main = st.file_uploader("1. ارفع الشيت الأساسي (المجمع)", type=["xlsx"])
uploaded_port = st.file_uploader("2. ارفع شيت المحفظة الجديدة", type=["xlsx"])

if st.button("🔄 إعادة ضبط التطبيق"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.step = 1
    st.rerun()

if uploaded_main and uploaded_port:
    
    if st.session_state.step == 1:
        if st.button("🔍 بدء التحليل الدقيق ومطابقة اللوحات"):
            try:
                wb_main = openpyxl.load_workbook(uploaded_main)
                sheet_main = wb_main.active
                
                wb_port = openpyxl.load_workbook(uploaded_port, data_only=True)
                sheet_port = wb_port.active

                port_data = []
                port_plates_set = set()

                for row in range(2, sheet_port.max_row + 1):
                    plate_val = sheet_port.cell(row=row, column=1).value
                    if plate_val:
                        cleaned = clean_plate_text(plate_val)
                        if cleaned:
                            car_type = sheet_port.cell(row=row, column=4).value
                            port_data.append({
                                'original': plate_val,
                                'cleaned': cleaned,
                                'type': car_type
                            })
                            port_plates_set.add(cleaned)

                matched_owners = set()
                found_count = 0

                for row in range(2, sheet_main.max_row + 1):
                    main_plate_val = sheet_main.cell(row=row, column=1).value
                    if main_plate_val:
                        cleaned_main = clean_plate_text(main_plate_val)
                        if cleaned_main in port_plates_set:
                            found_count += 1
                            owner_val = sheet_main.cell(row=row, column=3).value
                            if owner_val:
                                matched_owners.add(str(owner_val).strip())

                st.session_state.port_data = port_data
                st.session_state.port_plates_set = port_plates_set
                st.session_state.matched_owners = list(matched_owners)
                st.session_state.found_count = found_count
                st.session_state.total_port = len(port_data)
                st.session_state.uploaded_main = uploaded_main
                st.session_state.step = 2
                st.rerun()

            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملفات: {e}")

    elif st.session_state.step == 2:
        st.info(f"📊 **تقرير التحليل:** تم فحص المحفظة ووجدنا أن **{st.session_state.found_count}** لوحة (من أصل {st.session_state.total_port}) موجودة مسبقاً في الشيت الأساسي.")

        if st.session_state.matched_owners:
            owners_list = "، ".join(st.session_state.matched_owners)
            st.warning(f"⚠️ هذه اللوحات مسجلة حالياً بأسماء الملاك التاليين: **{owners_list}**")
            default_name = st.session_state.matched_owners[0]
        else:
            st.success("✨ جميع لوحات المحفظة جديدة كلياً وغير مسجلة في الشيت الأساسي.")
            default_name = ""

        st.write("---")
        new_owner_input = st.text_input("✍️ أدخل اسم المالك الجديد الذي ترغب في تسجيل هذه المحفظة باسمه:", value=default_name)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ تأكيد واعتماد التحديث"):
                if new_owner_input:
                    st.session_state.final_owner = new_owner_input
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.error("الرجاء كتابة اسم المالك بشكل صحيح.")

    elif st.session_state.step == 3:
        st.success(f"جاهز الآن لتحديث البيانات واعتماد اسم المالك: **{st.session_state.final_owner}**")
        
        if st.button("🚀 تنفيذ التحديث واستخراج ملف الإكسل النهائي"):
            try:
                wb_final = openpyxl.load_workbook(st.session_state.uploaded_main)
                sheet_final = wb_final.active

                for row in range(sheet_final.max_row, 1, -1):
                    p_val = sheet_final.cell(row=row, column=1).value
                    if p_val:
                        if clean_plate_text(p_val) in st.session_state.port_plates_set:
                            sheet_final.delete_rows(row, 1)

                for item in st.session_state.port_data:
                    sheet_final.append([item['original'], item['type'], st.session_state.final_owner])

                output_filename = "Master_Sheet_Updated.xlsx"
                wb_final.save(output_filename)

                with open(output_filename, "rb") as file_download:
                    st.download_button(
                        label="📥 اضغط هنا لتحميل ملف الإكسل المحدث",
                        data=file_download,
                        file_name="Master_Sheet_Updated.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                st.balloons()
                st.success("تم الانتهاء بنجاح واستخراج الملف جاهز للاستخدام!")

            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة وإخراج الملف: {e}")
                
