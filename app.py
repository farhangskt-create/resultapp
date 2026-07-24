import streamlit as st
import pdfplumber
import os

st.set_page_config(page_title="BISE Result Search Portal", page_icon="🎓", layout="wide")

st.markdown("<h2 style='text-align: center;'>🎓 BISE Result Search Portal</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Instant Gazette Search System</b></p>", unsafe_allow_html=True)

default_pdf_path = "gazette.pdf"

if os.path.exists(default_pdf_path):
    # صرف دو صاف ستھرے آپشنز
    search_option = st.radio("Select Search Type:", ["Search by Roll Number", "Search by Institution Code / School Name"])
    st.markdown("---")

    if search_option == "Search by Roll Number":
        roll_input = st.text_input("Enter Roll Number:")
        if st.button("Search Result", type="primary"):
            if roll_input:
                found = False
                with st.spinner("Searching gazette..."):
                    with pdfplumber.open(default_pdf_path) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text:
                                for line in text.split('\n'):
                                    if roll_input in line:
                                        st.subheader("📋 Student Result Details:")
                                        st.success(line)
                                        
                                        # پاس یا فیل چیک کرنے کی لاجک
                                        lower_line = line.lower()
                                        if "fail" in lower_line:
                                            st.warning("⚠️ **Better luck next time!** Work harder for the next attempt.")
                                        else:
                                            st.balloons()
                                            st.success("🎉 **Congratulations!** You have successfully passed the examination.")
                                        found = True
                                        break
                            if found:
                                break
                if not found:
                    st.error("No record found against this Roll Number.")
            else:
                st.warning("Please enter a valid Roll Number.")

    else: # اسکول کوڈ یا نام کے ذریعے سرچ
        school_input = st.text_input("Enter School Code or Name:")
        if st.button("Search School Gazette List", type="primary"):
            if school_input:
                school_records = []
                with st.spinner("Searching school records across gazette..."):
                    with pdfplumber.open(default_pdf_path) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text:
                                for line in text.split('\n'):
                                    if school_input.lower() in line.lower():
                                        school_records.append(line)
                
                if school_records:
                    st.subheader(f"🏫 Institution Results (Total Records: {len(school_records)})")
                    for rec in school_records:
                        st.text(rec)
                else:
                    st.warning("No records found matching this School Code or Name.")
            else:
                st.warning("Please enter a School Code or Name.")

else:
    st.error("⚠️ Error: 'gazette.pdf' file is missing in the GitHub repository. Please upload it.")
        
