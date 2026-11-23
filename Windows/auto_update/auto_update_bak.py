import ctypes
import subprocess
import sys
from pathlib import Path

# Adjust to where you extracted HP Image Assistant
HPIA = Path(r"C:\HPIA\HPImageAssistant.exe")
HPIA_REPORTS = Path(r"C:\HPIA\Reports")
HPIA_DOWNLOADS = Path(r"C:\HPIA\Downloads")


def is_admin() -> bool:
    return bool(ctypes.windll.shell32.IsUserAnAdmin())


def run(cmd: list[str], label: str) -> int:
    print(f"\n=== {label} ===")
    result = subprocess.run(cmd)
    print(f"{label} finished with exit code {result.returncode}")
    return result.returncode


def powershell(command: str, label: str) -> int:
    return run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
        label,
    )


def windows_update():
    powershell(
        "Set-PSRepository -Name PSGallery -InstallationPolicy Trusted; "
        "if (-not (Get-Module -ListAvailable PSWindowsUpdate)) "
        "{ Install-Module PSWindowsUpdate -Force -Scope AllUsers }; "
        "Import-Module PSWindowsUpdate; "
        "Get-WindowsUpdate -MicrosoftUpdate -AcceptAll -Install -IgnoreReboot",
        "Windows Update",
    )


def store_update():
    run(
        ["winget", "upgrade", "--all", "--source", "msstore",
         "--accept-package-agreements", "--accept-source-agreements",
         "--silent"],
        "Microsoft Store apps",
    )


def hp_update():
    if not HPIA.exists():
        print("HP Image Assistant not found, skipping HP updates.")
        return
    HPIA_REPORTS.mkdir(parents=True, exist_ok=True)
    HPIA_DOWNLOADS.mkdir(parents=True, exist_ok=True)
    run(
        [str(HPIA), "/Operation:Analyze", "/Action:Install",
         "/Category:All", "/Selection:All", "/Silent",
         f"/ReportFolder:{HPIA_REPORTS}",
         f"/SoftpaqDownloadFolder:{HPIA_DOWNLOADS}"],
        "HP drivers/BIOS",
    )


def main():
    if not is_admin():
        # Relaunch elevated
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(f'"{a}"' for a in sys.argv), None, 1
        )
        return

    windows_update()
    store_update()
    hp_update()
    print("\nAll done. A reboot may be required.")


if __name__ == "__main__":
    main()