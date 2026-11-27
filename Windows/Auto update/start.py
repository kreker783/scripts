
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"

TOOLS = {
    "1": ("Update the system", "auto_update.py")
}


def clear_screen():
    import os
    os.system("cls")


def run_tool(script):
    script_path = SCRIPTS / script

    if not script_path.is_file():
        print(f"\nScript not found: {script}")
        input("\nPress Enter to continue...")
        return

    print(f"\nStarting {script}...\n")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT)
    )

    print(f"\nTool finished (exit code: {result.returncode})")
    input("\nPress Enter to return to menu...")


def main():
    while True:
        # clear_screen()

        run_tool


if __name__ == "__main__":
    main()
