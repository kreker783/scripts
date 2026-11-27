$Runtime  = Join-Path $PSScriptRoot "runtime"
$Main = Join-Path $PSScriptRoot "auto_update.py"
$Temp = Join-Path $env:TEMP ("py_" + [guid]::NewGuid().ToString("N"))

$Zips = @{
    python = Join-Path $Runtime "python.zip"
    hpia   = Join-Path $Runtime "hpia.zip"
}

foreach ($z in $Zips.Values) {
    if (!(Test-Path $z)) {
        Write-Host "Missing: $z" -ForegroundColor Red
        Start-Sleep -Seconds 10
        exit 1
    }
}

try {
    $procs = foreach ($name in $Zips.Keys) {
        $dest = Join-Path $Temp $name
        New-Item $dest -ItemType Directory -Force | Out-Null
        Start-Process tar.exe -ArgumentList '-xf', "`"$($Zips[$name])`"", '-C', "`"$dest`"" `
            -WindowStyle Hidden -PassThru
    }
    $procs | Wait-Process

    $env:PYTHONDONTWRITEBYTECODE = 1
    $env:HPIA_PATH = Join-Path $Temp "hpia"
    
    & (Join-Path $Temp "python\python.exe") $Main
    
    $code = $LASTEXITCODE
}
finally {
    Remove-Item $Temp -Recurse -Force -ErrorAction SilentlyContinue
}

exit $code