# PowerShell script to mirror local files to an FTP server

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$FtpServer
)

# Get the current directory
$CurrentDir = Get-Location

# Construct and execute the lftp command
$command = "lftp $FtpServer -e ""mirror -R '$CurrentDir/' /; quit"""

# Execute the command
Write-Host "Connecting to $FtpServer and pushing files from current directory..."
Invoke-Expression $command

Write-Host "Upload complete!" -ForegroundColor Green

# Usage: .\push.ps1 ftp://username:password@ftp.example.com:21