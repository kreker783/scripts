$Scripts = @(
    @{ Name = 'Clear temp files';      Path = 'clear_temp.bat' }
    @{ Name = 'Network diagnostics';   Path = 'netdiag.bat' }
    @{ Name = 'Collect system info';   Path = 'sysinfo.bat' }
    @{ Name = 'Check disk health';     Path = 'disk_check.bat' }
)
 
$line = '=' * 50
$thin = '-' * 50
 
while ($true) {
    Clear-Host
    Write-Host $line -ForegroundColor Cyan
    Write-Host "  ADMIN TOOLKIT  |  $env:COMPUTERNAME" -ForegroundColor Cyan
    Write-Host $line -ForegroundColor Cyan
    Write-Host ""
 
    for ($i = 0; $i -lt $Scripts.Count; $i++) {
        Write-Host "  [$($i + 1)] " -ForegroundColor Yellow -NoNewline
        Write-Host $Scripts[$i].Name
    }
 
    Write-Host ""
    Write-Host $thin -ForegroundColor DarkGray
    Write-Host "  [q] " -ForegroundColor Yellow -NoNewline
    Write-Host "Quit"
    Write-Host $thin -ForegroundColor DarkGray
    Write-Host ""
 
    $choice = Read-Host "  Select"
    if ($choice -eq 'q') { break }
 
    $item = $Scripts[[int]$choice - 1]
 
    Write-Host ""
    Write-Host $line -ForegroundColor Green
    Write-Host "  Running: $($item.Name)" -ForegroundColor Green
    Write-Host $line -ForegroundColor Green
    Write-Host ""
 
    cmd /c "$PSScriptRoot\$($item.Path)"
 
    Write-Host ""
    Write-Host $thin -ForegroundColor DarkGray
    Read-Host "  Done. Press Enter to return to menu"
}
 