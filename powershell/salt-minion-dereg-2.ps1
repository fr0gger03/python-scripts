This is the script i am using (thank you Gemini):# 1. Configuration
$LogDir      = "$env:LOCALAPPDATA\SaltLogs"  # Saves to User's AppData to avoid permission issues
$LogFile     = "$LogDir\SaltLogoff.log"
$SaltPath    = "C:\Program Files\Salt Project\Salt\salt-call.exe" # Update to your actual path
$Username    = $env:USERNAME

# 2. Ensure the log directory exists
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# 3. Helper function (Fixed: Explicitly accepts the log path as a parameter)
function Write-Log {
    param (
        [string]$Message,
        [string]$Type = "INFO",
        [string]$Path
    )
    $CurrentTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $Path -Value "[$CurrentTime] [$Type] $Message"
}

# Initial Log Entry
Write-Log -Message "Logoff script initiated for user: $Username" -Path $LogFile

# 4. Build the Payload
$Payload = @{
    username = $Username
    message  = "User logging off, delete key"
}
$JsonPayload = $Payload | ConvertTo-Json -Compress

# 5. Execute and Catch Errors
try {
    if (-not (Test-Path $SaltPath)) {
        throw "Salt executable not found at path: $SaltPath"
    }

    # Start the process and capture standard error
    $ProcessArgs = @{
        FilePath               = $SaltPath
        ArgumentList           = @("event.send", "win/user/logoff", "'$JsonPayload'")
        NoNewWindow            = $true
        Wait                   = $true
        PassThru               = $true
        RedirectStandardError  = "$LogDir\salt_stderr.txt" 
    }

    $Result = Start-Process @ProcessArgs

    # Check the exit code of salt-call
    if ($Result.ExitCode -eq 0) {
        Write-Log -Message "Successfully sent salt-call logoff event for $Username." -Type "SUCCESS" -Path $LogFile
    } else {
        $StdErrContent = Get-Content "$LogDir\salt_stderr.txt" -Raw
        throw "salt-call exited with code $($Result.ExitCode). Error: $StdErrContent"
    }

} catch {
    Write-Log -Message "Failed to send salt-call event. Reason: $_" -Type "ERROR" -Path $LogFile
} finally {
    # Clean up temporary stderr file if it exists
    if (Test-Path "$LogDir\salt_stderr.txt") {
        Remove-Item "$LogDir\salt_stderr.txt" -Force
    }
    Write-Log -Message "Logoff script finished." -Path $LogFile
}