import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
from tkcalendar import DateEntry  # New import

# Sample data
data = {
    'Patient_ID': [101, 102, 103, 104, 105, 106],
    'Name': ['kevin', 'preethi', 'sanjay', 'ram', 'priya', 'ravi'],
    'Age': [19, 20, 25, 30, 26, 28],
    'Gender': ['Male', 'Female', 'Male', 'Male', 'Female', 'Male'],
    'Diagnosis': ['Flu', 'Diabetes', 'Hypertension', 'Dengu', 'Cold', 'Malaria'],
    'Admission_Date': ['05 04 2025', '04 03 2025', '06 03 2025', '10 04 2025', '12 02 2025', '20 04 2025'],
    'Discharge_Date': ['10 04 2025', '07 03 2025', '10 03 2025', '15 04 2025', '16 02 2025', '25 04 2025'],
}

hospital_data = pd.DataFrame(data)

# Format dates to datetime
hospital_data['Admission_Date'] = pd.to_datetime(hospital_data['Admission_Date'], format='%d %m %Y')
hospital_data['Discharge_Date'] = pd.to_datetime(hospital_data['Discharge_Date'], format='%d %m %Y')

# GUI Functions
def view_all_patients():
    top = tk.Toplevel(root)
    top.title("All Patients")

    tree = ttk.Treeview(top)
    tree["columns"] = list(hospital_data.columns)
    tree["show"] = "headings"

    for col in hospital_data.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for _, row in hospital_data.iterrows():
        row = row.copy()
        row['Admission_Date'] = row['Admission_Date'].strftime("%d %m %Y")
        row['Discharge_Date'] = row['Discharge_Date'].strftime("%d %m %Y")
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill="both")

def add_patient():
    def save_patient():
        global hospital_data
        try:
            admission_date = datetime.strptime(e_admission.get(), "%d %m %Y")
            discharge_date = datetime.strptime(e_discharge.get(), "%d %m %Y")

            new_patient = {
                'Patient_ID': int(e_id.get()),
                'Name': e_name.get(),
                'Age': int(e_age.get()),
                'Gender': gender_var.get(),
                'Diagnosis': e_diagnosis.get(),
                'Admission_Date': admission_date,
                'Discharge_Date': discharge_date
            }

            if new_patient['Patient_ID'] in hospital_data['Patient_ID'].values:
                messagebox.showerror("Error", "Patient ID already exists.")
                return

            hospital_data = pd.concat([hospital_data, pd.DataFrame([new_patient])], ignore_index=True)
            messagebox.showinfo("Success", f"Patient {new_patient['Name']} added successfully!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    win = tk.Toplevel(root)
    win.title("Add New Patient")

    tk.Label(win, text="Patient_ID").grid(row=0, column=0, padx=5, pady=5)
    e_id = tk.Entry(win)
    e_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="Name").grid(row=1, column=0, padx=5, pady=5)
    e_name = tk.Entry(win)
    e_name.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(win, text="Age").grid(row=2, column=0, padx=5, pady=5)
    e_age = tk.Entry(win)
    e_age.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(win, text="Gender").grid(row=3, column=0, padx=5, pady=5)
    gender_var = tk.StringVar(value="Male")
    gender_dropdown = ttk.Combobox(win, textvariable=gender_var, values=["Male", "Female"], state="readonly")
    gender_dropdown.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(win, text="Diagnosis").grid(row=4, column=0, padx=5, pady=5)
    e_diagnosis = tk.Entry(win)
    e_diagnosis.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(win, text="Admission_Date (DD MM YYYY)").grid(row=5, column=0, padx=5, pady=5)
    e_admission = tk.Entry(win)
    e_admission.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(win, text="Discharge_Date (DD MM YYYY)").grid(row=6, column=0, padx=5, pady=5)
    e_discharge = tk.Entry(win)
    e_discharge.grid(row=6, column=1, padx=5, pady=5)

    tk.Button(win, text="Add Patient", command=save_patient).grid(row=7, columnspan=2, pady=10)

def update_diagnosis():
    try:
        patient_id = int(simpledialog.askstring("Update Diagnosis", "Enter Patient ID:"))
        if patient_id in hospital_data['Patient_ID'].values:
            new_diag = simpledialog.askstring("Update Diagnosis", "Enter New Diagnosis:")
            hospital_data.loc[hospital_data['Patient_ID'] == patient_id, 'Diagnosis'] = new_diag
            messagebox.showinfo("Success", f"Diagnosis updated for Patient ID {patient_id}")
        else:
            messagebox.showerror("Error", "Patient ID not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

def find_by_diagnosis():
    diag = simpledialog.askstring("Find Patients", "Enter Diagnosis:")
    result = hospital_data[hospital_data['Diagnosis'].str.contains(diag, case=False)]

    top = tk.Toplevel(root)
    top.title(f"Patients with Diagnosis: {diag}")

    if result.empty:
        tk.Label(top, text="No matching patients found.").pack()
        return

    tree = ttk.Treeview(top)
    tree["columns"] = list(result.columns)
    tree["show"] = "headings"

    for col in result.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    for _, row in result.iterrows():
        row = row.copy()
        row['Admission_Date'] = row['Admission_Date'].strftime("%d %m %Y")
        row['Discharge_Date'] = row['Discharge_Date'].strftime("%d %m %Y")
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill="both")

def find_by_date_range():
    win = tk.Toplevel(root)
    win.title("Find by Date Range")

    tk.Label(win, text="Start Date:").grid(row=0, column=0, padx=5, pady=5)
    cal_start = DateEntry(win, date_pattern='dd mm yyyy')
    cal_start.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(win, text="End Date:").grid(row=1, column=0, padx=5, pady=5)
    cal_end = DateEntry(win, date_pattern='dd mm yyyy')
    cal_end.grid(row=1, column=1, padx=5, pady=5)

    def search():
        try:
            start_date = pd.to_datetime(cal_start.get_date())
            end_date = pd.to_datetime(cal_end.get_date())

            df = hospital_data.copy()
            result = df[(df['Admission_Date'] <= end_date) & (df['Discharge_Date'] >= start_date)]

            result_win = tk.Toplevel(root)
            result_win.title(f"Patients from {start_date.strftime('%d %m %Y')} to {end_date.strftime('%d %m %Y')}")

            if result.empty:
                tk.Label(result_win, text="No matching patients found.").pack()
                return

            tree = ttk.Treeview(result_win)
            tree["columns"] = list(result.columns)
            tree["show"] = "headings"

            for col in result.columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center")

            for _, row in result.iterrows():
                row = row.copy()
                row['Admission_Date'] = row['Admission_Date'].strftime("%d %m %Y")
                row['Discharge_Date'] = row['Discharge_Date'].strftime("%d %m %Y")
                tree.insert("", "end", values=list(row))

            tree.pack(expand=True, fill="both")

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    tk.Button(win, text="Search", command=search).grid(row=2, columnspan=2, pady=10)

# GUI Setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("400x400")

tk.Label(root, text="Hospital Management System", font=("Helvetica", 16)).pack(pady=10)

tk.Button(root, text="View All Patients", width=30, command=view_all_patients).pack(pady=5)
tk.Button(root, text="Add New Patient", width=30, command=add_patient).pack(pady=5)
tk.Button(root, text="Update Patient's Diagnosis", width=30, command=update_diagnosis).pack(pady=5)
tk.Button(root, text="Find Patients by Diagnosis", width=30, command=find_by_diagnosis).pack(pady=5)
tk.Button(root, text="Find Patients by Date Range", width=30, command=find_by_date_range).pack(pady=5)
tk.Button(root, text="Exit", width=30, command=root.destroy).pack(pady=20)

root.mainloop()
