import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="BISE Result Gazette Search App", page_icon="📚", layout="wide")

st.markdown("<h2 style='text-align: center;'>BISE Result Gazette Search App</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Search Student Results by Roll Number or School Code from PDF Gazette</b></p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Result Gazette (PDF)", type=["pdf"])

if uploaded_file is not None:
    @st.cache_data
    def load_pdf_text(file):
        extracted_text = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.extend(text.split('\n'))
        return extracted_text

    with st.spinner("Extracting text from PDF Gazette, please wait..."):
        pdf_lines = load_pdf_text(uploaded_file)
    
    st.success(f"Gazette loaded successfully! Total lines found: {len(pdf_lines):,}")

    search_type = st.radio("Select Search Method:", ["Search by Roll Number", "Search by School Code / Name"])

    if search_type == "Search by Roll Number":
        roll_no = st.text_input("Enter Roll Number:")
        if st.button("Search Roll Number", type="primary"):
            if roll_no:
                found_results = [line for line in pdf_lines if roll_no in line]
                if found_results:
                    st.subheader("Search Result:")
                    for res in found_results:
                        st.info(res)
                else:
                    st.warning("No record found against this Roll Number in the gazette.")
            else:
                st.error("Please enter a valid Roll Number.")

    elif search_type == "Search by School Code / Name":
        school_query = st.text_input("Enter School Code or Institution Name:")
        if st.button("Search School List", type="primary"):
            if school_query:
                school_results = [line for line in pdf_lines if school_query.lower() in line.lower()]
                if school_results:
                    st.subheader(f"Students found for: {school_query} (Total lines: {len(school_results)})")
                    for line in school_results:
                        st.write(line)
                else:
                    st.warning("No records found matching this School Code or Name.")
            else:
                st.error("Please enter a School Code or Name.")
else:
    st.info("👆 براہ کرم ٹیسٹنگ کے لیے کوئی بھی پرانا رزلٹ گزیٹ (PDF) یہاں اپ لوڈ کریں۔")
