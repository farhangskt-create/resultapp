import streamlit as st
import pdfplumber
import os
import glob

st.set_page_config(page_title="BISE Result Search Portal", page_icon="🎓", layout="wide")

st.markdown("<h2 style='text-align: center;'>🎓 BISE Result Search Portal</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Instant Gazette Search System</b></p>", unsafe_allow_html=True)

pdf_path = "gazette.pdf"
chunks_dir = "gazette_chunks"

# بیک گراؤنڈ میں خاموشی سے چنکس بنانے کا فنکشن (بغیر کسی اسکرین ڈسپل کے)
@st.cache_resource
def background_process_gazette(pdf_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if os.path.exists(pdf_file):
        # اگر چنکس پہلے سے نہیں بنے تو خاموشی سے بنائیں
        if not os.path.exists(os.path.join(output_dir, "chunk_general.txt")):
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        for line in text.split('\n'):
                            line_clean = line.strip()
                            if line_clean:
                                words = line_clean.split()
                                if words and words[0].isdigit() and len(words[0]) >= 3:
                                    prefix = words[0][:3] 
                                    chunk_file = os.path.join(output_dir, f"chunk_{prefix}.txt")
                                    with open(chunk_file, "a", encoding="utf-8") as cf:
                                       cf.write(line_clean + "\n")
                                else:
                                    chunk_file = os.path.join(output_dir, "chunk_general.txt")
                                    with open(chunk_file, "a", encoding="utf-8") as cf:
                                       cf.write(line_clean + "\n")
    return True

# بیک گراؤنڈ پروسیس کال کرنا (اسکرین پر کچھ نظر نہیں آئے گا)
if os.path.exists(pdf_path):
    background_process_gazette(pdf_path, chunks_dir)

    # اب صرف اور صرف اصل انٹرفیس نظر آئے گا
    search_option = st.radio("Select Search Type:", ["Search by Roll Number", "Search by Institution Code / School Name"])
    st.markdown("---")

    if search_option == "Search by Roll Number":
        roll_input = st.text_input("Enter Roll Number:")
        if st.button("Search Result", type="primary"):
            if roll_input:
                found = False
                prefix = roll_input[:3]
                target_chunk = os.path.join(chunks_dir, f"chunk_{prefix}.txt")
                
                if os.path.exists(target_chunk):
                    with open(target_chunk, "r", encoding="utf-8") as f:
                        for line in f:
                            if roll_input in line:
                                st.subheader("📋 Student Result Details:")
                                st.success(line.strip())
                                
                                lower_line = line.lower()
                                if "fail" in lower_line or "f" in lower_line.split():
                                    st.warning("⚠️ **Better luck next time!** Work harder for the next attempt.")
                                else:
                                    st.balloons()
                                    st.success("🎉 **Congratulations!** You have successfully passed the examination.")
                                found = True
                                break
                
                if not found:
                    general_chunk = os.path.join(chunks_dir, "chunk_general.txt")
                    if os.path.exists(general_chunk):
                        with open(general_chunk, "r", encoding="utf-8") as f:
                            for line in f:
                                if roll_input in line:
                                    st.subheader("📋 Student Result Details:")
                                    st.success(line.strip())
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
                all_chunks = glob.glob(os.path.join(chunks_dir, "*.txt"))
                for chunk_file in all_chunks:
                    with open(chunk_file, "r", encoding="utf-8") as f:
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
    st.error("⚠️ Error: 'gazette.pdf' file is missing in the GitHub repository. Please upload it..")
