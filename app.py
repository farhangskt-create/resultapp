import streamlit as st
import pdfplumber
import os

st.set_page_config(page_title="BISE Result Search Portal", page_icon="🎓", layout="wide")

st.markdown("<h2 style='text-align: center;'>🎓 BISE Result Search Portal</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Fast & Crash-Free Gazette Search System</b></p>", unsafe_allow_html=True)

pdf_path = "gazette.pdf"
txt_path = "gazette.txt"

# 1. اگر ٹیکسٹ فائل نہیں بنی تو PDF کو ایک بار TXT میں تبدیل کرنا (صرف ایک بار ہوگا)
if not os.path.exists(txt_path) and os.path.exists(pdf_path):
    with st.spinner("Optimizing gazette for fast search (One-time process)..."):
        text_content = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_content.append(t)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(text_content))

# 2. سرچ کا مین سسٹم (اب یہ انتہائی تیز اور کریش فری ٹیکسٹ فائل سے پڑھے گا)
if os.path.exists(txt_path):
    search_option = st.radio("Select Search Type:", ["Search by Roll Number", "Search by Institution Code / School Name"])
    st.markdown("---")

    if search_option == "Search by Roll Number":
        roll_input = st.text_input("Enter Roll Number:")
        if st.button("Search Result", type="primary"):
            if roll_input:
                found = False
                with st.spinner("Searching record..."):
                    with open(txt_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if roll_input in line:
                                st.subheader("📋 Student Result Details:")
                                st.success(line.strip())
                                
                                # پاس یا فیل کا پیغام
                                lower_line = line.lower()
                                if "fail" in lower_line or "f" in lower_line.split():
                                    st.warning("⚠️ **Better luck next time!** Work harder for the next attempt.")
                                else:
                                    st.balloons()
                                    st.success("🎉 **Congratulations!** You have successfully passed the examination.")
                                found = True
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
                with st.spinner("Fetching school records..."):
                    with open(txt_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if school_input.lower() in line.lower():
                                school_records.append(line.strip())
                
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
