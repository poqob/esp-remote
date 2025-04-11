#!/usr/bin/env python3
import argparse
import subprocess
import os
import py_compile
import platform
from constants import ESP_REMOTE_SERVER_PORT, ESP_API_KEY
from activities import restart_esp

def fetch(ip, port, username, password):
    """Performs the fetch operation."""
    try:
        if platform.system() == "Windows":
            # Use PowerShell script on Windows
            command = f'powershell -ExecutionPolicy Bypass -File "./scripts/get.ps1" "ftp://{username}:{password}@{ip}:{port}"'
        else:
            # Use bash script on Linux/Unix
            command = f'lftp -u {username},{password} -p {port} {ip} -e "mirror --verbose . ./project/; bye"'
        
        subprocess.run(command, shell=True, check=True)
        print("Fetch operation completed successfully.")
    except Exception as e:
        print(f"Error: {e}")

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

def push(ip, port, username, password):
    """Performs the push operation with Python file verification."""
    # First verify all Python files
    is_valid, invalid_files = verify_python_files()
    
    if not is_valid:
        print("Python syntax errors found in these files:")
        for file_path, error in invalid_files:
            print(f"• {os.path.relpath(file_path)}")
            print(f"  Error: {error}")
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
        print("Push operation completed successfully.")
        push_success = True
    except Exception as e:
        print(f"Error during push: {e}")
    
    # Always restart ESP after push attempt, regardless of success or failure
    try:
        restart_result = restart_esp(ip, ESP_REMOTE_SERVER_PORT, ESP_API_KEY)
        if restart_result:
            if push_success:
                print("Push successful and ESP restarted successfully.")
            else:
                print("Push failed but ESP was restarted.")
        else:
            if push_success:
                print("Push successful but failed to restart ESP.")
            else:
                print("Push failed and failed to restart ESP.")
    except Exception as e:
        print(f"Error restarting ESP: {e}")
    
    check_remove_file(ip, port, username, password)

def check_remove_file(ip, port, username, password):
    try:
        remove_file = ".remove"
        if not os.path.exists(remove_file):
            print("No .remove file found. Skipping remove operation.")
            return
            
        with open(remove_file, "r+") as file:
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
                
                print("Remove operation completed successfully.")
                # Truncate the file after successful removal
                file.seek(0)
                file.truncate()
            else:
                print("No files to remove.")
    except Exception as e:
        print(f"Error during remove operation: {e}")

def main():
    parser = argparse.ArgumentParser(description="ESP FTP CLI Tool")
    parser.add_argument("action", choices=["fetch", "push"], help="Operation to perform: fetch or push")
    parser.add_argument("--ip", required=True, help="FTP server IP address")
    parser.add_argument("--port", required=False, default=21, help="FTP server port number")
    parser.add_argument("--username", required=False, default="", help="FTP username")
    parser.add_argument("--password", required=False, default="", help="FTP password")

    args = parser.parse_args()

    print(f"Running on {platform.system()} operating system")

    if args.action == "fetch":
        fetch(args.ip, args.port, args.username, args.password)
    elif args.action == "push":
        push(args.ip, args.port, args.username, args.password)

if __name__ == "__main__":
    main()