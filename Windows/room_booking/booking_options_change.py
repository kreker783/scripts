import subprocess
import sys
import uuid

from Scripts.Windows.add_users_to_shared_mailbox.add_users_to_shared_mailbox import get_users

class PowerShellSession:
    def __init__(self):
        self.proc = subprocess.Popen(
            ["pwsh", "-NoLogo", "-NoExit", "-Command", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # merge errors into stdout for simplicity
            text=True,
            bufsize=1,
        )

    def run(self, command: str) -> str:
        marker = f"__END_{uuid.uuid4().hex}__"
        self.proc.stdin.write(command + "\n")
        self.proc.stdin.write(f'Write-Output "{marker}"\n')
        self.proc.stdin.flush()

        output_lines = []
        for line in self.proc.stdout:
            if line.strip() == marker:
                break
            output_lines.append(line)
        return "".join(output_lines)

    def close(self):
        try:
            self.proc.stdin.write("exit\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        self.proc.wait()

def get_mailbox():
    mailbox = input("Provide room mailbox: ")
    return mailbox

def get_action():
    action = input("What do you want to do? (enable/disable) for booking: ")
    return action

def main():
    ps = PowerShellSession()

    ps.run("Connect-ExchangeOnline -DisableWAM")

    mailbox = get_mailbox()
    action = get_action()

    if action == "enable":
        ps.run(f"Set-CalendarProcessing -Identity {mailbox} -AutomateProcessing AutoAccept -AllBookInPolicy $true")
    elif action == "disable":
        ps.run(f"Set-CalendarProcessing -Identity {mailbox} -AutomateProcessing AutoAccept -AllBookInPolicy $false")
    else:
        print("Invalid action. Please choose 'enable' or 'disable'.")
        ps.close()
        sys.exit(1)

    print("Done!")

    ps.run("Disconnect-ExchangeOnline -Confirm:$false")
    ps.close()

    sys.exit(0)


if __name__ == "__main__":
    main()