import subprocess
import sys
import uuid

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
    mailbox = input("Provide mailbox: ")
    return mailbox

def get_users():
    users = input("Provide list of users (space separated): ").split(" ")
    return users

def main():
    ps = PowerShellSession()

    ps.run("Connect-ExchangeOnline -DisableWAM")

    mailbox = get_mailbox()
    users = get_users()

    for user in users:
        ps.run(f"Add-MailboxPermission -Identity {mailbox} -User {user} -AccessRights FullAccess -InheritanceType All")
        ps.run(f"Add-RecipientPermission -Identity {mailbox} -Trustee {user} -AccessRights SendAs -Confirm:$false")

    print("Done!")

    ps.run("Disconnect-ExchangeOnline -Confirm:$false")
    ps.close()

    sys.exit(0)


if __name__ == "__main__":
    main()