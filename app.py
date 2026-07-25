import streamlit as st
import json
import time
import os

# Page Configuration
st.set_page_config(page_title="Result Gazette", page_icon="🎓", layout="centered")

# --- DATA LOADING (Fast as lightning) ---
# @st.cache_data ensures the file is read only once and kept in memory!
@st.cache_data
def load_data():
    file_path = "gazette_data.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Fallback dummy data if the file is missing
        return [
            {"roll_number": "10001", "institution_code": "333", "name": "Ali", "result": "Pass"},
            {"roll_number": "10002", "institution_code": "333", "name": "Sara", "result": "Fail"},
            {"roll_number": "10003", "institution_code": "444", "name": "Zain", "result": "Pass"},
        ]

data = load_data()

# --- UI DESIGN ---
st.title("🎓 Board Result Gazette")
st.write("Enter your **Roll Number** OR **Institution Code** to find results.")

# Create the search form
with st.form("search_form"):
    roll_input = st.text_input("Enter Roll Number:")
    st.write("**OR**")
    inst_input = st.text_input("Enter Institution Code:")
    
    # Submit button
    submitted = st.form_submit_button("Search ⚡")

# --- SEARCH LOGIC ---
if submitted:
    if not roll_input and not inst_input:
        st.warning("⚠️ Please enter either a Roll Number or an Institution Code.")
    else:
        # Show searching message
        with st.spinner("Searching as fast as lightning... ⚡"):
            time.sleep(0.5) # A tiny half-second delay just so the user can see the lightning message!
            
            # 1. SEARCH BY ROLL NUMBER
            if roll_input:
                found_student = None
                for student in data:
                    if student["roll_number"] == roll_input.strip():
                        found_student = student
                        break
                
                if found_student:
                    st.subheader("Student Result")
                    st.write(f"**Roll Number:** {found_student['roll_number']}")
                    st.write(f"**Name:** {found_student['name']}")
                    st.write(f"**Result:** {found_student['result']}")
                    
                    # Custom Pass/Fail Messages
                    if found_student['result'].lower() == "pass":
                        st.success("congratulations its the fruite of yous efforts")
                    else:
                        st.error("better luck next time")
                else:
                    st.error("❌ Roll Number not found in the gazette.")
            
            # 2. SEARCH BY INSTITUTION CODE
            elif inst_input:
                inst_students = [s for s in data if s["institution_code"] == inst_input.strip()]
                
                if inst_students:
                    st.subheader(f"🏫 Institution Code: {inst_input.strip()}")
                    st.write(f"**Total students found:** {len(inst_students)}")
                    
                    # Extract just the roll numbers for the list
                    roll_numbers = [s["roll_number"] for s in inst_students]
                    
                    st.write("### Attached Roll Numbers:")
                    # Display as a clean, comma-separated list
                    st.info(", ".join(roll_numbers))
                    
                    # Also show a detailed table of everyone in the institution
                    st.write("### Detailed List")
                    st.table(inst_students)
                else:
                    st.error("❌ Institution Code not found.")
