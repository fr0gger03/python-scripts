# 1. Find the PID of the salt-minion service
$Service = Get-CimInstance -ClassName Win32_Service -Filter "Name='salt-minion'"
$PIDToKill = $Service.ProcessId

if (-not $PIDToKill) {
    Write-Error "salt-minion service is not running or could not be found."
    exit
}

# 2. Send the Salt logoff event
& "c:\program files\Salt Project\Salt\salt-call.exe" event.send win/user/logoff

# 3. IMMEDIATELY kill the process using the PID to block auth retries
Stop-Process -Id $PIDToKill -Force -ErrorAction SilentlyContinue

Write-Host "Salt logoff event sent and salt-minion (PID: $PIDToKill) forcefully terminated." -ForegroundColor Green
