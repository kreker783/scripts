import ctypes
import os
import subprocess

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def windows_update():
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "Set-PSRepository -Name PSGallery -InstallationPolicy Trusted; "
            "if (-not (Get-Module -ListAvailable PSWindowsUpdate)) "
            "{ Install-Module PSWindowsUpdate -Force -Scope AllUsers }; "
            "Import-Module PSWindowsUpdate; "
            "Get-WindowsUpdate -MicrosoftUpdate -AcceptAll -Install -IgnoreReboot",
        ]
    )

def store_update():
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "Get-CimInstance -Namespace 'Root\\cimv2\\mdm\\dmmap' "
            "-ClassName 'MDM_EnterpriseModernAppManagement_AppManagement01' "
            "| Invoke-CimMethod -MethodName UpdateScanMethod",
        ]
    )

def hp_update():
    path_to_hpia = os.path.dirname(os.path.abspath(__file__)) + "\\..\\runtime\\hpia.exe"
    if not os.path.exists(path_to_hpia):
        print(f"HP Image Assistant not found at {path_to_hpia}. Skipping HP update.")
        exit(1)

    subprocess.run(
        [
            path_to_hpia,
            "/Operation:Analyze",
            "/Action:Install",
            "/Selection:All",
            "/Category:All",
            "/Silent",
            "/Noninteractive",
        ]
    )

def main():
    if not is_admin():
        print("This script must be run as an administrator.")
        return
    windows_update()
    store_update()
    # hp_update()

if __name__ == "__main__":
    main()