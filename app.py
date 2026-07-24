import streamlit as st
import pdfplumber
import pandas as pd
import os

st.set_page_config(page_title="BISE Result Search Portal", page_icon="🎓", layout="wide")

# صاف ستھرا اور سادہ ہیڈر
st.markdown("<h2 style='text-align: center;'>🎓 BISE Result Search Portal</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Fast & Direct Gazette Search System</b></p>", unsafe_allow_html=True)

default_pdf_path = "gazette.pdf"

# بیک گراؤنڈ میں تیز رفتار ڈیٹا ریڈنگ اور کیشنگ
@st.cache_data
def load_gazette_fast(pdf_path):
    records = []
    if os.path.exists(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    for line in text.split('\n'):
                        line_clean = line.strip()
                        if line_clean:
                            words = line_clean.split()
                            if words:
                                roll_candidate = words[0]
                                records.append({
                                    "RollNo": roll_candidate,
                                    "Record": line_clean
                                })
    return pd.DataFrame(records)

# فائل لوڈنگ
if os.path.exists(default_pdf_path):
    with st.spinner("Loading Gazette in background..."):
        df = load_gazette_fast(default_pdf_path)

    # صرف مطلوبہ دو آپشنز
    search_option = st.radio("Select Search Type:", ["Search by Roll Number", "Search by Institution Code / School Name"])
    st.markdown("---")

    if search_option == "Search by Roll Number":
        roll_input = st.text_input("Enter Roll Number:")
        if st.button("Search Result", type="primary"):
            if roll_input:
                # رول نمبر تلاش کرنا
                result_row = df[df['RollNo'] == roll_input]
                
                if not result_row.empty:
                    st.subheader("📋 Student Result Details:")
                    for _, row in result_row.iterrows():
                        full_line = row['Record']
                        st.success(full_line)
                        
                        # پاس یا فیل چیک کرنے کی لاجک (گزیٹ کے الفاظ کے مطابق)
                        lower_text = full_line.lower()
                        if "fail" in lower_text or "f" in words_checker(lower_text):
                            st.warning("⚠️ **Better luck next time!** Work harder for the next attempt.")
                        else:
                            st.balloons()
                            st.success("🎉 **Congratulations!** You have successfully passed the examination.")
                else:
                    # اگر ایگزیکٹ میچ نہ ہو تو لائن کے اندر سرچ
                    sub_match = df[df['Record'].str.contains(roll_input, case=False, na=False)]
                    if not sub_match.empty:
                        st.subheader("📋 Search Result:")
                        for _, row in sub_match.iterrows():
                            st.info(row['Record'])
                            st.success("🎉 **Congratulations!**")
                    else:
                        st.error("No record found against this Roll Number.")
            else:
                st.warning("Please enter a valid Roll Number.")

    else: # اسکول کوڈ یا نام کے ذریعے سرچ
        school_input = st.text_input("Enter School Code or Name:")
        if st.button("Search School Gazette List", type="primary"):
            if school_input:
                school_matches = df[df['Record'].str.contains(school_input, case=False, na=False)]
                
                if not school_matches.empty:
                    st.subheader(f"🏫 Institution Results (Total Records: {len(school_matches)})")
                    # گزیٹ کی طرح ہو بہو لسٹ دکھانا
                    for idx, row in school_matches.iterrows():
                        st.text(row['Record']) # گزیٹ فارمیٹ کے لیے st.text بہترین ہے
                else:
                    st.warning("No records found matching this School Code or Name.")
            else:
                st.warning("Please enter a School Code or Name.")

else:
    st.error("⚠️ Error: 'gazette.pdf' file is missing in the GitHub repository. Please upload it.")

# ہیلپر فنکشن
def words_checker(text):
    return text.split()
