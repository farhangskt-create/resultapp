import streamlit as st
import pdfplumber
import os

st.set_page_config(page_title="BISE Result Gazette Search App", page_icon="📚", layout="wide")

st.markdown("<h2 style='text-align: center;'>BISE Result Gazette Search App</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Search Student Results Instantly by Roll Number or School Code</b></p>", unsafe_allow_html=True)

GAZETTE_PATH = "gazette.pdf"

if not os.path.exists(GAZETTE_PATH):
    st.error("⚠️ Official Gazette PDF is not uploaded in the repository yet. Please upload 'gazette.pdf' to GitHub.")
else:
    # سرچ کا انٹرفیس فوراً سامنے آ جائے گا بغیر کسی لمبی لوڈنگ کے
    search_type = st.radio("Select Search Method:", ["Search by Roll Number", "Search by School Code / Name"])

    if search_type == "Search by Roll Number":
        roll_no = st.text_input("Enter Roll Number:")
        if st.button("Search Roll Number", type="primary"):
            if roll_no:
                found_results = []
                with st.spinner("Searching gazette, please wait..."):
                    with pdfplumber.open(GAZETTE_PATH) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text:
                                for line in text.split('\n'):
                                    if roll_no in line:
                                        found_results.append(line)
                
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
                school_results = []
                with st.spinner("Searching school records, please wait..."):
                    with pdfplumber.open(GAZETTE_PATH) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text:
                                for line in text.split('\n'):
                                    if school_query.lower() in line.lower():
                                        school_results.append(line)
                
                if school_results:
                    st.subheader(f"Students found for: {school_query} (Total records: {len(school_results)})")
                    for line in school_results:
                        st.write(line)
                else:
                    st.warning("No records found matching this School Code or Name.")
            else:
                st.error("Please enter a School Code or Name.")
