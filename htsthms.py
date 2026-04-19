import streamlit as st
import pandas as pd
import csv
import os

def local_css(file_name):
    """Loads custom CSS if the file exists."""
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
local_css("style.css")

# --- Configuration ---
FILENAME = 'patients_record.csv'
HEADERS = [
    "Patient ID", "Name", "Age", "Gender", "Address", "Mobile No", 
    "Case", "Date of Admit", "Date of Discharge", "Treatment", 
    "Room No", "Hospital Charges", "Treatment Charges", "Total Bill"
]

def initialize_file():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)

def get_patient_data():
    """Safely loads patient data into a DataFrame."""
    if not os.path.exists(FILENAME):
        return pd.DataFrame(columns=HEADERS)
    try:
        df = pd.read_csv(FILENAME)
        return df
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=HEADERS)

# --- App Layout & Initialization ---
st.set_page_config(page_title="GLS Hospital Management System", layout="wide", page_icon="🏥")
initialize_file()

# --- Sidebar Navigation ---
st.sidebar.title("🏥 GLS Hospital")
# Strictly two operations
menu = ["Add Patient", "View All Patients"]
choice = st.sidebar.radio("Navigation Menu", menu)

# --- Page: Add Patient ---
if choice == "Add Patient":
    st.header("➕ Register New Patient")
    st.markdown("---")
    
    with st.form("add_patient_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            patid = st.text_input("Patient ID")
            patname = st.text_input("Full Name")
            age = st.number_input("Age", min_value=0, max_value=120, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            patadd = st.text_area("Address")
            
        with col2:
            mobno = st.text_input("Mobile No")
            p_case = st.text_input("Case/Diagnosis")
            date_of_admit = st.date_input("Date of Admit")
            date_of_discharge = st.date_input("Date of Discharge")
            treat = st.text_input("Treatment")
            
        with col3:
            roomno = st.text_input("Room No")
            hoscharge = st.number_input("Hospital Charges", min_value=0.0, step=100.0)
            trecharge = st.number_input("Treatment Charges", min_value=0.0, step=100.0)
            
        submit_button = st.form_submit_button("Save Patient Record")
        
        if submit_button:
            if not patid or not patname:
                st.error("Patient ID and Name are required fields.")
            else:
                totalbill = round(hoscharge + trecharge, 2)
                data = [
                    patid, patname, str(age), gender, patadd, mobno, 
                    p_case, str(date_of_admit), str(date_of_discharge), treat, 
                    roomno, str(hoscharge), str(trecharge), str(totalbill)
                ]
                
                with open(FILENAME, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(data)
                    
                st.success(f"Record for **{patname}** saved successfully!")
                st.info(f"Calculated Total Bill: **${totalbill}**")

# --- Page: View All Patients ---
elif choice == "View All Patients":
    st.header("📋 Patient Records")
    st.markdown("---")
    
    df = get_patient_data()
    
    if df.empty:
        st.info("No patient records available to display.")
    else:
        # Display the relevant columns
        display_df = df[["Patient ID", "Name", "Age", "Gender", "Case", "Date of Admit", "Room No", "Total Bill"]]
        st.dataframe(display_df, use_container_width=True, hide_index=True)