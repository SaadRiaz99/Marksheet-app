import tkinter as tk
from tkinter import messagebox
import csv
import os
from PIL import Image, ImageTk

File_name = "show_marksheet.csv"

if not os.path.exists(File_name):
    with open(File_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Name", "Roll No", "English", "Math",
            "Islamiat", "Urdu", "Total",
            "Percentage", "Grade", "Result"
        ])

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
        for mark in [eng, math, isl, urdu]:
            if mark < 0 or mark > 100:
                messagebox.showerror("Error", "Marks must be between 0 and 100")
                return
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
        with open(File_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, roll, eng, math, isl, urdu, total, f"{percent:.2f}", grade, result])
        display_marksheet(name, roll, eng, math, isl, urdu, total, percent, grade, result)
        messagebox.showinfo("Success", "Marksheet shown & data saved")
    except ValueError:
        messagebox.showerror("Error", "Marks must be numbers only")

def display_marksheet(name, roll, eng, math, isl, urdu, total, percent, grade, result):
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
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, output)
    text_output.config(state=tk.DISABLED)

def clear_form():
    for entry in entries:
        entry.delete(0, tk.END)
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.config(state=tk.DISABLED)

def search_marksheet():
    roll_to_search = entry_roll.get().strip()
    if not roll_to_search:
        messagebox.showerror("Error", "Enter Roll No to search")
        return
    found = False
    with open(File_name, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["Roll No"] == roll_to_search:
                found = True
                display_marksheet(row["Name"], row["Roll No"],
                                  int(row["English"]), int(row["Math"]),
                                  int(row["Islamiat"]), int(row["Urdu"]),
                                  int(row["Total"]), float(row["Percentage"]),
                                  row["Grade"], row["Result"])
                break
    if not found:
        messagebox.showinfo("Not Found", f"No record found for Roll No {roll_to_search}")

root = tk.Tk()
root.title("Student Marksheet")
root.geometry("500x700")
root.configure(bg="#2c3e50")

if os.path.exists("logo.jpg"):
    img = Image.open("logo.jpg")
    img = img.resize((100, 100))
    photo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(root, image=photo, bg="#2c3e50")
    logo_label.photo = photo
    logo_label.pack(pady=10)

tk.Label(root, text="Student Marksheet", fg="#ecf0f1", bg="#2c3e50",
         font=("Helvetica", 20, "bold")).pack(pady=5)

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

button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Show Marksheet", command=show_marksheet,
          bg="#27ae60", fg="white", font=("Helvetica", 12, "bold"),
          width=20).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Search", command=search_marksheet,
          bg="#2980b9", fg="white", font=("Helvetica", 12, "bold"),
          width=20).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Clear", command=clear_form,
          bg="#c0392b", fg="white", font=("Helvetica", 12, "bold"),
          width=42).grid(row=1, column=0, columnspan=2, pady=5)

text_output = tk.Text(root, height=15, width=60, bg="#ecf0f1", fg="#2c3e50",
                      font=("Helvetica", 11))
text_output.pack(pady=10)
text_output.config(state=tk.DISABLED)

root.mainloop()
