import tkinter as tk
from tkinter import messagebox
import csv
import os
from PIL import Image, ImageTk

File_name = "show_marksheet.csv"

# ===== Create CSV if not exists =====
if not os.path.exists(File_name):
    with open(File_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Name", "Roll No", "English", "Math",
            "Islamiat", "Urdu", "Total",
            "Percentage", "Grade", "Result"
        ])

# ===== Function to Show & Save Marksheet =====
def show_marksheet():
    try:
        name = entry_name.get().strip()
        roll = entry_roll.get().strip()

        if not name or not roll:
            messagebox.showerror("Error", "Name and Roll No required")
            return

        eng = int(entry_eng.get())
        math = int(entry_math.get())
        isl = int(entry_isl.get())
        urdu = int(entry_urdu.get())

        total = eng + math + isl + urdu
        percent = total / 4

        if percent >= 80:
            grade = "A+"
        elif percent >= 70:
            grade = "A"
        elif percent >= 60:
            grade = "B"
        elif percent >= 50:
            grade = "C"
        else:
            grade = "Fail"

        result = "Pass" if grade != "Fail" else "Fail"

        # Save to CSV
        with open(File_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                name, roll, eng, math, isl, urdu,
                total, f"{percent:.2f}", grade, result
            ])

        # Show in Text Box
        output = f"""
======= MARKSHEET =======
Name     : {name}
Roll No  : {roll}

English  : {eng}
Math     : {math}
Islamiat : {isl}
Urdu     : {urdu}

-------------------------
Total Marks : {total}/400
Percentage  : {percent:.2f}%
Grade       : {grade}
Result      : {result}
=========================
"""
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)

        messagebox.showinfo("Success", "Marksheet shown & data saved")

    except ValueError:
        messagebox.showerror("Error", "Marks must be numbers only")


root = tk.Tk()
root.title("Student Marksheet")
root.geometry("450x600")
root.configure(bg="#2c3e50")   





tk.Label(root, text="Student Marksheet",
         fg="#ecf0f1", bg="#2c3e50",
         font=("Helvetica", 20, "bold")).pack(pady=15)


form = tk.Frame(root, bg="#34495e", padx=20, pady=20)
form.pack(pady=10)


label_fg = "#ecf0f1"
entry_bg = "#ecf0f1"
entry_fg = "#2c3e50"

fields = ["Name", "Roll No", "English", "Math", "Islamiat", "Urdu"]
entries = []

for i, field in enumerate(fields):
    tk.Label(form, text=field, fg=label_fg, bg="#34495e",
             font=("Helvetica", 12, "bold")).grid(row=i, column=0, sticky="w", pady=5)
    entry = tk.Entry(form, width=25, bg=entry_bg, fg=entry_fg, font=("Helvetica", 11))
    entry.grid(row=i, column=1, pady=5, padx=5)
    entries.append(entry)

entry_name, entry_roll, entry_eng, entry_math, entry_isl, entry_urdu = entries


tk.Button(root, text="Show Marksheet",
          command=show_marksheet,
          bg="#27ae60", fg="white",
          font=("Helvetica", 12, "bold"),
          width=20).pack(pady=15)


text_output = tk.Text(root, height=14, width=52, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 11))
text_output.pack(pady=10)

root.mainloop()
