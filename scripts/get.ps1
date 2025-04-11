# PowerShell script to mirror files from an FTP server

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$FtpServer
)

# Get the current directory
$CurrentDir = Get-Location

# Construct and execute the lftp command
$command = "lftp -e ""mirror --parallel=5 --use-pget-n=5 / '$CurrentDir'; quit"" $FtpServer"

# Execute the command
Write-Host "Connecting to $FtpServer and mirroring files to current directory..."
Invoke-Expression $command

Write-Host "Download complete!" -ForegroundColor Green

# Usage: .\get.ps1 ftp://username:password@ftp.example.com:21