import streamlit as st
import pdfplumber
import pandas as pd
import os

st.set_page_config(page_title="BISE Result Gazette Search App (Pandas Powered)", page_icon="📊", layout="wide")

st.markdown("<h2 style='text-align: center;'>📊 BISE Result Gazette Search App (Pandas Engine)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Lightning-Fast Search using Pandas DataFrames</b></p>", unsafe_allow_html=True)

default_pdf_path = "gazette.pdf"

@st.cache_data
def load_gazette_with_pandas(pdf_path):
    data_rows = []
    
    if os.path.exists(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    for line in text.split('\n'):
                        line_clean = line.strip()
                        if line_clean:
                            words = line_clean.split()
                            if words:
                                roll_candidate = words[0]
                                # اگر پہلا لفظ رول نمبر (ڈیجٹ) ہے
                                if roll_candidate.isdigit() and len(roll_candidate) >= 5:
                                    data_rows.append({
                                        "RollNo": roll_candidate,
                                        "Record": line_clean
                                    })
                                else:
                                    # باقی لائنیں (جیسے اسکول کا نام یا دیگر تفصیلات)
                                    data_rows.append({
                                        "RollNo": "INFO",
                                        "Record": line_clean
                                    })
                                    
    # Pandas DataFrame بنانا
    df = pd.DataFrame(data_rows)
    return df

if os.path.exists(default_pdf_path):
    with st.spinner("Processing Gazette with Pandas, please wait..."):
        df_gazette = load_gazette_with_pandas(default_pdf_path)
    
    st.success(f"Pandas Database Ready! Total processed lines: {len(df_gazette):,}")

    search_type = st.radio("Select Search Method:", ["Search by Roll Number", "Search by School Code"])

    if search_type == "Search by Roll Number":
        roll_no = st.text_input("Enter Roll Number (e.g., 123456):")
        if st.button("Search Roll Number", type="primary"):
            if roll_no:
                # Pandas کی مدد سے فوری فلٹرنگ
                matched_df = df_gazette[df_gazette['RollNo'] == roll_no]
                
                if not matched_df.empty:
                    st.subheader("🎯 Student Result Found:")
                    for idx, row in matched_df.iterrows():
                        st.success(row['Record'])
                else:
                    # اگر ڈائریکٹ میچ نہ ہو تو پوری ریکارڈ لائنز میں سرچ کریں
                    sub_matched = df_gazette[df_gazette['Record'].str.contains(roll_no, case=False, na=False)]
                    if not sub_matched.empty:
                        st.subheader("🎯 Search Result:")
                        for idx, row in sub_matched.iterrows():
                            st.info(row['Record'])
                    else:
                        st.warning("No record found against this Roll Number.")
            else:
                st.error("Please enter a valid Roll Number.")

    elif search_type == "Search by School Code":
        school_code = st.text_input("Enter School Code / Keyword:")
        if st.button("Search School Students", type="primary"):
            if school_code:
                # Pandas کے ذریعے اسکول کوڈ یا نام تلاش کرنا
                school_matched = df_gazette[df_gazette['Record'].str.contains(school_code, case=False, na=False)]
                
                if not school_matched.empty:
                    st.subheader(f"🏫 Found {len(school_matched)} matching records for: {school_code}")
                    # Pandas کا خوبصورت ٹیبل شو کرنا
                    st.dataframe(school_matched[['Record']], use_container_width=True)
                else:
                    st.warning("No records found matching this School Code.")
            else:
                st.error("Please enter a School Code.")

else:
    st.error(f"⚠️ Error: Default gazette file ('{default_pdf_path}') not found in GitHub repository.")
