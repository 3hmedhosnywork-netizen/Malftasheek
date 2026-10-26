import streamlit as st
import openpyxl
import re

st.set_page_config(page_title="تحديث الشيت الذكي", page_icon="🚗")
st.title("🚗 تطبيق تحديث الشيت الذكي")

# دالة ذكية لترتيب وتنظيف اللوحات (حروف ثم أرقام وبدون مسافات)
def normalize_plate(plate_str):
    if not plate_str: return ""
    # تحويل لنص ومسح المسافات
    plate_str = str(plate_str).replace(" ", "").strip()
    # استخراج الحروف العربية فقط
    letters = "".join(re.findall(r'[\u0600-\u06FF]+', plate_str))
    # استخراج الأرقام فقط
    numbers = "".join(re.findall(r'\d+', plate_str))
    # تجميع اللوحة: حروف ثم أرقام
    return letters + numbers

if 'step' not in st.session_state:
    st.session_state.step = 1

uploaded_main = st.file_uploader("1. ارفع الشيت الأساسي (المجمع)", type=["xlsx"])
uploaded_port = st.file_uploader("2. ارفع شيت المحفظة الجديدة", type=["xlsx"])

if st.button("🔄 إعادة البدء من جديد"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.step = 1
    st.rerun()
    
if uploaded_main and uploaded_port:
    if st.session_state.step == 1:
        if st.button("🔍 تحليل المحفظة ومطابقة اللوحات"):
            try:
                wb_main = openpyxl.load_workbook(uploaded_main)
                sheet_main = wb_main.active
                wb_port = openpyxl.load_workbook(uploaded_port, data_only=True)
                sheet_port = wb_port.active

                port_data = []
                port_plates_normalized = set()
                
                # قراءة المحفظة (بدءاً من الصف 2)
                for row in range(2, sheet_port.max_row + 1):
                    plate = sheet_port.cell(row=row, column=1).value
                    if plate:
                        norm_plate = normalize_plate(plate)
                        if norm_plate: # للتأكد أن الخلية ليست فارغة بعد التنظيف
                            car_type = sheet_port.cell(row=row, column=4).value
                            port_data.append({
                                'original_plate': plate, 
                                'norm_plate': norm_plate, 
                                'type': car_type
                            })
                            port_plates_normalized.add(norm_plate)

                current_owners = set()
                plates_found = 0
                
                # قراءة الشيت الأساسي والمطابقة باللوحة المرتبة
                for row in range(2, sheet_main.max_row + 1):
                    main_plate = sheet_main.cell(row=row, column=1).value
                    if main_plate:
                        norm_main_plate = normalize_plate(main_plate)
                        if norm_main_plate in port_plates_normalized:
                            owner = sheet_main.cell(row=row, column=3).value
                            if owner:
                                current_owners.add(str(owner).strip())
                            plates_found += 1

                st.session_state.port_data = port_data
                st.session_state.port_plates_normalized = port_plates_normalized
                st.session_state.current_owners = list(current_owners)
                st.session_state.plates_found = plates_found
                st.session_state.port_plates_count = len(port_data)
                st.session_state.step = 2
                st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ أثناء التحليل: {e}")

    elif st.session_state.step == 2:
        st.info(f"📊 **نتيجة التحليل:** تم العثور على {st.session_state.plates_found} لوحة مكررة في الشيت الأساسي من أصل {st.session_state.port_plates_count} لوحة مرفوعة في المحفظة.")
        
        if st.session_state.current_owners:
            owners_str =
