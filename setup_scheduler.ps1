<# 
.SYNOPSIS
    Set up Windows Task Scheduler tasks for Project Academy.

.DESCRIPTION
    Creates two scheduled tasks:
    1. Academy_Morning (07:00 daily) - Generates the daily sprint
    2. Academy_Evening (22:00 daily) - Runs weekly review (Sundays) or archives (weekdays)
    
    Both tasks call the orchestrator through the system Python interpreter.

.NOTES
    Run this script as Administrator (required for Task Scheduler).
    Modify the paths below if your Python or project directory differs.
#>

# --- Configuration ---
$PythonPath = "python"
$ProjectDir = "D:\Dev\Projects\AI Academy"
$OrchestratorPath = "$ProjectDir\orchestrator.py"

# --- Morning Sprint Task ---
$morningAction = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "`"$OrchestratorPath`"" `
    -WorkingDirectory $ProjectDir

$morningTrigger = New-ScheduledTaskTrigger -Daily -At 7:00AM

$morningSettings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

Register-ScheduledTask `
    -TaskName "Academy_Morning" `
    -Action $morningAction `
    -Trigger $morningTrigger `
    -Settings $morningSettings `
    -Description "Project Academy: Generate daily sprint (reads journal, calls Ollama, writes sprint)" `
    -Force

Write-Host "[OK] Academy_Morning task registered (07:00 daily)" -ForegroundColor Green

# --- Evening Review Task ---
$eveningAction = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "`"$OrchestratorPath`" --mode=review" `
    -WorkingDirectory $ProjectDir

$eveningTrigger = New-ScheduledTaskTrigger -Daily -At 10:00PM

$eveningSettings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

Register-ScheduledTask `
    -TaskName "Academy_Evening" `
    -Action $eveningAction `
    -Trigger $eveningTrigger `
    -Settings $eveningSettings `
    -Description "Project Academy: Evening review / weekly report (Sundays)" `
    -Force

Write-Host "[OK] Academy_Evening task registered (22:00 daily)" -ForegroundColor Green

# --- Verify ---
Write-Host "`n--- Registered Tasks ---" -ForegroundColor Cyan
Get-ScheduledTask -TaskName "Academy_*" | Format-Table TaskName, State, @{N="NextRun";E={($_ | Get-ScheduledTaskInfo).NextRunTime}} -AutoSize

Write-Host "`nTo remove tasks later:`n  Unregister-ScheduledTask -TaskName 'Academy_Morning' -Confirm:`$false`n  Unregister-ScheduledTask -TaskName 'Academy_Evening' -Confirm:`$false" -ForegroundColor DarkGray
