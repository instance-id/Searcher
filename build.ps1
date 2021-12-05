#!/usr/bin/env pwsh

# .\build.ps1 -Zip -Version v0.1.0
Param (
    [Parameter()]
    [string]$Version,
    [switch]$Zip
)

if ($Version) {
    Write-Host "Building $Version..."
} else {
    Write-Host 'Just updating files...'
}

$date = Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'
$exclude = '--exclude-from=build/exclude.excl'
$include = '--include-from=build/include.incl'
$config = '--config=C:/Users/mosthated/.backup/rclone.conf'
$cmd = ''
$source1 = ''
$destination1 = ''

if ($IsWindows) {
    $cmd = 'C:\files\rclone\rclone.exe'
    $source1 = 'E:\GitHub\Searcher\'
    $destination1 = 'E:\Searcher'
    $log1 = "--log-file=C:\files\rclone\logs\Searcher_Build_$date.log"
} elseif ($IsLinux) {
    $cmd = 'rclone'
    $source1 = '/mnt/x/GitHub/instance-id/1_Projects/Searcher'
    $destination1 = '/mnt/x/_dev/Searcher'
    $log1 = "--log-file=$HOME/.backup/logs/Searcher_Build_$date.log"
}

&$cmd sync $source1 $destination1 $log1 $exclude $config --log-level NOTICE `
    --progress `
    --no-update-modtime `
    --transfers=4 `
    --checkers=8 `
    --contimeout=60s `
    --timeout=300s `
    --retries=3 `
    --low-level-retries=10 `
    -L `
    --stats=1s `
    --stats-file-name-length=0 `
    -P `
    --ignore-case `
    --fast-list `
    --drive-chunk-size=64M

if ($Version) {
    Write-Host "Building $Version..."

    $searcher = 'Searcher'
    $destination2 = $searcher, $Version -join '_'
    $folderVer = "$destination1\$destination2"

    Write-Host "Destination2: $destination2"

    if ([System.IO.File]::Exists($folderVer)) {
        Get-ChildItem $folderVer -Recurse -ErrorAction SilentlyContinue | Remove-Item -Recurse
    }
    New-Item "$folderVer\$searcher" -Type Directory
    Move-Item -Path $destination1\packages -Destination $folderVer\packages
    Move-Item -Path $destination1\README.md -Destination $folderVer\README.md
    Move-Item -Path $destination1\Searcher_install_instructions.url -Destination $folderVer\Searcher_install_instructions.url

    Move-Item -Path $destination1\dso -Destination $folderVer\$searcher\dso
    Move-Item -Path $destination1\help -Destination $folderVer\$searcher\help
    Move-Item -Path $destination1\python2.7libs -Destination $folderVer\$searcher\python2.7libs
    Move-Item -Path $destination1\python3.7libs -Destination $folderVer\$searcher\python3.7libs
    Move-Item -Path $destination1\toolbar -Destination $folderVer\$searcher\toolbar

    $listfiles = Get-ChildItem $folderVer -Recurse -File -Include '*.md', '*.txt'
    $old = '{#version}'
    foreach ($file in $listfiles) {
        (Get-Content $file) -Replace ($old, $Version) | Set-Content $file
    }

    $FileName = "$destination1\$destination2.zip"
    if (Test-Path $FileName) {
        Write-Host "Removing $FileName and recreating"
        Remove-Item $FileName
    }
    if ($Zip) {
        Compress-Archive -Path $folderVer -DestinationPath $FileName
    }
    Write-Host 'Update Complete'
} else {
    Write-Host 'Update Complete'
}