#!/usr/bin/env python3
import argparse
import subprocess

def fetch(ip, port, username, password):
    """Performs the fetch operation."""
    try:
        command = f'lftp -u {username},{password} -p {port} {ip} -e "mirror --verbose . ./project/; bye"'
        subprocess.run(command, shell=True, check=True)
        print("Fetch operation completed successfully.")
    except Exception as e:
        print(f"Error: {e}")

def push(ip, port, username, password):
    """Performs the push operation."""
    try:
        command = f'lftp -u {username},{password} -p {port} {ip} -e "mirror --reverse --verbose ./project/ .; bye"'
        subprocess.run(command, shell=True, check=True)
        print("Push operation completed successfully.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="ESP FTP CLI Tool")
    parser.add_argument("action", choices=["fetch", "push"], help="Operation to perform: fetch or push")
    parser.add_argument("--ip", required=True, help="FTP server IP address")
    parser.add_argument("--port", required=False, default=21, help="FTP server port number")
    parser.add_argument("--username", required=False, default="", help="FTP username")
    parser.add_argument("--password", required=False, default="", help="FTP password")

    args = parser.parse_args()

    if args.action == "fetch":
        fetch(args.ip, args.port, args.username, args.password)
    elif args.action == "push":
        push(args.ip, args.port, args.username, args.password)

if __name__ == "__main__":
    main()