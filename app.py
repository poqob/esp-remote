#!/usr/bin/env python3
import tkinter as tk
import subprocess
import os
import py_compile
import platform
from activities import restart_esp
from constants import *


def run_fetch_script():
    ip = ip_entry.get()
    port = port_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    try:
        if platform.system() == "Windows":
            # Use PowerShell script on Windows
            command = f'powershell -ExecutionPolicy Bypass -File "./scripts/get.ps1" "ftp://{username}:{password}@{ip}:{port}"'
        else:
            # Use bash script on Linux/Unix
            command = f'lftp -u {username},{password} -p {port} {ip} -e "mirror --verbose . ./project/; bye"'
        
        subprocess.run(command, shell=True, check=True)
        result_label.config(text="Fetch operation completed successfully.", fg="green")
    except Exception as e:
        result_label.config(text=f"Error: {e}", fg="red")

def verify_python_files():
    """Verify all Python files in the project directory using py_compile."""
    project_dir = "./project"
    invalid_files = []
    
    if not os.path.exists(project_dir):
        return True, []
    
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    py_compile.compile(file_path, doraise=True)
                except py_compile.PyCompileError as e:
                    invalid_files.append((file_path, str(e)))
    
    return len(invalid_files) == 0, invalid_files

def get_ignore_patterns():
    """Read .ignore file and return list of patterns to be excluded."""
    ignore_patterns = []
    ignore_file = ".ignore"
    
    if os.path.exists(ignore_file):
        try:
            with open(ignore_file, "r") as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        ignore_patterns.append(line)
        except Exception as e:
            print(f"Error reading .ignore file: {e}")
    
    return ignore_patterns

def run_push_script():
    ip = ip_entry.get()
    port = port_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    
    # First verify all Python files
    is_valid, invalid_files = verify_python_files()
    
    if not is_valid:
        error_message = "Python syntax errors found in these files:\n"
        for file_path, error in invalid_files:
            error_message += f"• {os.path.relpath(file_path)}\n"
        result_label.config(text=error_message, fg="red")
        # Show detailed errors in console for debugging
        for file_path, error in invalid_files:
            print(f"Error in {file_path}: {error}")
        return
    
    # Get ignore patterns
    ignore_patterns = get_ignore_patterns()
    exclude_options = ""
    if ignore_patterns and platform.system() != "Windows":
        # Format each pattern for lftp exclude option (Linux/Unix only)
        exclude_options = " ".join([f"--exclude {pattern}" for pattern in ignore_patterns])
        print(f"Excluding patterns: {ignore_patterns}")
    
    push_success = False
    try:
        if platform.system() == "Windows":
            # Use PowerShell script on Windows
            # Note: Ignore patterns need to be handled separately in the PowerShell script
            command = f'powershell -ExecutionPolicy Bypass -File "./scripts/push.ps1" "ftp://{username}:{password}@{ip}:{port}"'
        else:
            # Use bash script on Linux/Unix
            command = f'lftp -u {username},{password} -p {port} {ip} -e "mirror --reverse --verbose {exclude_options} ./project/ .; bye"'
        
        subprocess.run(command, shell=True, check=True)
        result_label.config(text="Push operation completed successfully.", fg="green")
        push_success = True
    except Exception as e:
        result_label.config(text=f"Error during push: {e}", fg="red")
        
    # Always restart ESP after push attempt, regardless of success or failure
    try:
        restart_result = restart_esp(ip, ESP_REMOTE_SERVER_PORT, ESP_API_KEY)
        if restart_result:
            if push_success:
                result_label.config(text="Push successful and ESP restarted successfully.", fg="green")
            else:
                result_label.config(text="Push failed but ESP was restarted.", fg="orange")
        else:
            if push_success:
                result_label.config(text="Push successful but failed to restart ESP.", fg="orange")
            else:
                result_label.config(text="Push failed and failed to restart ESP.", fg="red")
    except Exception as e:
        result_label.config(text=f"Error restarting ESP: {e}", fg="red")
    
    check_remove_file()

def check_remove_file():
    ip = ip_entry.get()
    port = port_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    
    try:
        remove_file = ".remove"
        if not os.path.exists(remove_file):
            return
            
        with open(remove_file, "r") as file:
            lines = file.readlines()
            if lines:
                for line in lines:
                    line_stripped = line.strip()
                    if not line_stripped:
                        continue
                        
                    if platform.system() == "Windows":
                        # Use lftp directly in PowerShell on Windows
                        command = f'powershell -Command "lftp -u {username},{password} -p {port} {ip} -e \'rm {line_stripped}; bye\'"'
                    else:
                        # Use bash command on Linux/Unix
                        command = f'lftp -u {username},{password} -p {port} {ip} -e "rm {line_stripped}; bye"'
                    
                    subprocess.run(command, shell=True, check=True)
                
                # Truncate the file after successful removal
                with open(remove_file, "w") as file:
                    file.truncate(0)
                result_label.config(text="Remove operation completed successfully.", fg="green")
    except Exception as e:
        result_label.config(text=f"Error during remove operation: {e}", fg="red")


# Main window
root = tk.Tk()
root.title("ESP Remote")

# Display OS type in title
os_type = platform.system()
root.title(f"ESP Remote - {os_type}")

# Set application icon
try:
    app_icon = tk.PhotoImage(file=APPLICATION_ICON_PATH)
    root.iconphoto(False, app_icon)
except Exception as e:
    print(f"Error loading icon: {e}")

# Window dimensions
root.geometry("400x340")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Client", font=("Arial", 16, "bold"))
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