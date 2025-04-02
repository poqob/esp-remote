#!/usr/bin/env python3
import tkinter as tk
import subprocess

def run_fetch_script():
    ip = ip_entry.get()
    port = port_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    try:
        command = f'lftp -u {username},{password} -p {port} {ip} -e "mirror --verbose . ./project/; bye"'
        subprocess.run(command, shell=True, check=True)
        result_label.config(text="Fetch operation completed successfully.", fg="green")
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

def run_push_script():
    ip = ip_entry.get()
    port = port_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    try:
        command = f'lftp -u {username},{password} -p {port} {ip} -e "mirror --reverse --verbose ./project/ .; bye"'
        subprocess.run(command, shell=True, check=True)
        result_label.config(text="Push operation completed successfully.", fg="green")
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

# Main window
root = tk.Tk()
root.title("Poqob ESP FTP Client")


# Set application icon
icon_path = "./ico/esp.png"  # Ensure this file is in the same directory as your script
try:
    app_icon = tk.PhotoImage(file=icon_path)
    root.iconphoto(False, app_icon)
except Exception as e:
    print(f"Error loading icon: {e}")

# Window dimensions
root.geometry("400x340")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Basic FTP Client", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Description
description_label = tk.Label(root, text="Please enter the FTP details and click a button to perform the operation.", wraplength=380, justify="center")
description_label.pack(pady=5)

# Form area
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# IP Address Entry
tk.Label(form_frame, text="IP Address:", anchor="e", width=15).grid(row=0, column=0, padx=5, pady=5)
ip_entry = tk.Entry(form_frame, width=30)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

# Port Entry
tk.Label(form_frame, text="Port:", anchor="e", width=15).grid(row=1, column=0, padx=5, pady=5)
port_entry = tk.Entry(form_frame, width=30)
port_entry.grid(row=1, column=1, padx=5, pady=5)
port_entry.insert(0, "21")  # Default FTP port

# Username Entry
tk.Label(form_frame, text="Username:", anchor="e", width=15).grid(row=2, column=0, padx=5, pady=5)
username_entry = tk.Entry(form_frame, width=30)
username_entry.grid(row=2, column=1, padx=5, pady=5)

# Password Entry
tk.Label(form_frame, text="Password:", anchor="e", width=15).grid(row=3, column=0, padx=5, pady=5)
password_entry = tk.Entry(form_frame, width=30, show="*")
password_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

fetch_button = tk.Button(button_frame, text="Fetch", command=run_fetch_script, width=15, bg="#4CAF50", fg="white")
fetch_button.grid(row=0, column=0, padx=10)

push_button = tk.Button(button_frame, text="Push", command=run_push_script, width=15, bg="#2196F3", fg="white")
push_button.grid(row=0, column=1, padx=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 10), wraplength=380, justify="center")
result_label.pack(pady=5)

# Run the window
root.mainloop()