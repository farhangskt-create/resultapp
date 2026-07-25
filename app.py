import streamlit as st
import pdfplumber
import os
import glob

# Page configuration
st.set_page_config(
    page_title="BISE Result Search Portal",
    page_icon="🎓",
    layout="wide"
)

# Header design
st.markdown("<h2 style='text-align: center;'>🎓 BISE Result Search Portal</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>High-Performance Secure Gazette Search Engine</b></p>", unsafe_allow_html=True)
st.markdown("---")

pdf_path = "gazette.pdf"
chunks_dir = "gazette_chunks"

# Background Silent Indexing Engine to avoid RAM overflow and UI blocking
@st.cache_resource
def initialize_smart_chunks(pdf_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    general_chunk_path = os.path.join(output_dir, "chunk_general.txt")
    if os.path.exists(pdf_file) and not os.path.exists(general_chunk_path):
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
                                with open(general_chunk_path, "a", encoding="utf-8") as cf:
                                    cf.write(line_clean + "\n")
    return True

# Execute background processing invisibly without visual spinners
if os.path.exists(pdf_path):
    initialize_smart_chunks(pdf_path, chunks_dir)

    # Clean UI: Exclusively two options via radio toggle
    search_option = st.radio(
        "Select Search Type:",
        ["Search by Roll Number", "Search by Institution Code / School Name"],
        horizontal=True
    )
    st.markdown("")

    if search_option == "Search by Roll Number":
        col1, col2 = st.columns([2, 1])
        with col1:
            roll_input = st.text_input("Enter Roll Number:")
        
        st.markdown("")
        if st.button("Search Result", type="primary"):
            if roll_input:
                found = False
                prefix = roll_input[:3]
                target_chunk = os.path.join(chunks_dir, f"chunk_{prefix}.txt")
                
                # Targeted prefix scan for high speed
                if os.path.exists(target_chunk):
                    with open(target_chunk, "r", encoding="utf-8") as f:
                        for line in f:
                            if roll_input in line:
                                st.subheader("📋 Student Result Record:")
                                st.success(line.strip())
                                
                                lower_line = line.lower()
                                if "fail" in lower_line or "f" in lower_line.split():
                                    st.warning("⚠️ **Better luck next time!** Work harder for the next attempt.")
                                else:
                                    st.balloons()
                                    st.success("🎉 **Congratulations!** You have successfully passed the examination.")
                                found = True
                                break
                
                # Fallback scan in general chunk if not found in prefix index
                if not found:
                    general_chunk = os.path.join(chunks_dir, "chunk_general.txt")
                    if os.path.exists(general_chunk):
                        with open(general_chunk, "r", encoding="utf-8") as f:
                            for line in f:
                                if roll_input in line:
                                    st.subheader("📋 Student Result Record:")
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
                    st.error("No record found matching the specified Roll Number.")
            else:
                st.warning("Please enter a valid Roll Number before searching.")

    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            school_input = st.text_input("Enter Institution Code or School Name:")
        
        st.markdown("")
        if st.button("Search Institution Gazette List", type="primary"):
            if school_input:
                school_records = []
                all_chunks = glob.glob(os.path.join(chunks_dir, "*.txt"))
                
                for chunk_file in all_chunks:
                    with open(chunk_file, "r", encoding="utf-8") as f:
                        for line in f:
                            if school_input.lower() in line.lower():
                                school_records.append(line.strip())
                
                if school_records:
                    st.subheader(f"🏫 Institution Records (Total Found: {len(school_records)})")
                    # Render layout preserving exact formatting using text display blocks
                    for rec in school_records:
                        st.text(rec)
                else:
                    st.warning("No records found matching this Institution Code or School Name.")
            else:
                st.warning("Please enter a valid Institution Code or School Name.")

else:
    st.error("⚠️ Critical Error: 'gazette.pdf' is missing from the repository root directory. Please upload the official gazette PDF.")
