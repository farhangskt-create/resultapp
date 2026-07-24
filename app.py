import streamlit as st
import pdfplumber

st.set_page_config(page_title="BISE Result Gazette Search App", page_icon="📚", layout="wide")

st.markdown("<h2 style='text-align: center;'>📚 BISE Result Gazette Search App</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Instant Search by Roll Number or School Code from PDF Gazette</b></p>", unsafe_allow_html=True)

# فائل اپ لوڈ کرنے کا سیکشن
uploaded_file = st.file_uploader("Upload Result Gazette (PDF)", type=["pdf"])

if uploaded_file is not None:
    # کیشنگ (Caching) کی مدد سے پی ڈی ایف کو صرف ایک بار ریڈ کیا جائے گا تاکہ یہ بالکل سلو نہ ہو
    @st.cache_data
    def load_gazette_data(file_bytes):
        results_map = {}
        school_map = {}
        with pdfplumber.open(file_bytes) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    for line in text.split('\n'):
                        line_clean = line.strip()
                        if line_clean:
                            # لائن کو اسٹور کرنا
                            # فرض کریں رول نمبر لائن کے شروع میں ہے (پہلا لفظ یا ڈیجٹ)
                            words = line_clean.split()
                            if words:
                                roll_candidate = words[0]
                                if roll_candidate.isdigit() and len(roll_candidate) >= 5:
                                    results_map[roll_candidate] = line_clean
                            # اسکول کوڈ یا نام کے لیے پوری لائن کو محفوظ کرنا
                            school_map.setdefault("all_lines", []).append(line_clean)
        return results_map, school_map

    with st.spinner("Processing Gazette efficiently, please wait a moment..."):
        # بائٹس کے ذریعے تیز رفتار پروسیسنگ
        file_bytes = uploaded_file.getvalue()
        results_map, school_data = load_gazette_data(file_bytes)
    
    st.success("Gazette indexed successfully! Fast search is now ready.")

    search_type = st.radio("Select Search Method:", ["Search by Roll Number", "Search by School Code"])

    if search_type == "Search by Roll Number":
        col1, col2 = st.form("roll_form") if False else st.columns([3, 1])
        with col1:
            roll_no = st.text_input("Enter Roll Number (e.g., 123456):")
        
        if st.button("Search Roll Number", type="primary"):
            if roll_no:
                if roll_no in results_map:
                    st.subheader("🎯 Student Result Found:")
                    st.success(results_map[roll_no])
                else:
                    # اگر ڈائریکت کی نہ ملے تو لکی سرچ
                    matched = [line for line in school_data.get("all_lines", []) if roll_no in line]
                    if matched:
                        st.subheader("🎯 Search Result:")
                        for m in matched:
                            st.info(m)
                    else:
                        st.warning("No record found against this Roll Number.")
            else:
                st.error("Please enter a valid Roll Number.")

    elif search_type == "Search by School Code":
        school_code = st.text_input("Enter School Code / Institution Keyword:")
        if st.button("Search School Students", type="primary"):
            if school_code:
                all_lines = school_data.get("all_lines", [])
                matched_lines = [line for line in all_lines if school_code.lower() in line.lower()]
                
                if matched_lines:
                    st.subheader(f"🏫 Found {len(matched_lines)} records for: {school_code}")
                    # نتائج کو صاف ستھرے ٹیبل یا بکس میں دکھانا
                    for line in matched_lines[:100]: # زیادہ بوجھ سے بچنے کے لیے پہلے 100 نتائج
                        st.write(f"- {line}")
                    if len(matched_lines) > 100:
                        st.info("Showing first 100 matching results.")
                else:
                    st.warning("No records found matching this School Code.")
            else:
                st.error("Please enter a School Code.")

else:
    st.info("👆 براہ کرم رزلٹ گزیٹ (PDF) یہاں اپ لوڈ کریں۔")

st.markdown("---")
                    
