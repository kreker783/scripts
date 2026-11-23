# Set-CalendarProcessing -Identity "GCC.Room.Blue@lyreco.onmicrosoft.com" -ResourceDelegates mwloch@lyreco.com,mbarska@lyreco.com -BookInPolicy mwloch@lyreco.com,mbarska@lyreco.com,bnejfert@lyreco.com

# Connect-ExchangeOnline
#
# $InputCsv  = "$PSScriptRoot\users.csv"
# $OutputCsv = "$PSScriptRoot\users_uid.csv"
#
# #Get-User -Identity username | Select-Object -ExpandProperty UserPrincipalName
#
# $users = Get-Content -Path $InputCsv
#
# foreach ($row in $users) {
#     $user_email = $row
#     try {
#         $upn = Get-User -Identity $user_email | Select-Object -ExpandProperty UserPrincipalName
#         $upn -replace "@lyreco\.com$", "" |  Out-File -FilePath $OutputCsv -Append
#     } catch {
#         "$user_email - ERROR: $_" | Out-File -FilePath $OutputCsv -Append
#     }
# }
#
#
# Disconnect-ExchangeOnline

import subprocess
import sys
import uuid

# Creates one persistent Exchange Online session until scripts ens
# As a result there is no need in repeated MFA
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


def get_room():
    mailbox = input("Enter room you want to modify: ")
    if mailbox == '':
        print("Please enter a room")
        get_room()
    return mailbox

def get_user():
    user = input("Enter user: ")
    if user == '':
        print("Please enter a user")
        get_user()
    return user

def get_action():
    possible_actions = {
        1: "Get users",
        2: "Add user",
        3: "Remove user",
    }
    print(f"What action do you want to do?: ")
    print("1. Get users")
    print("2. Add user")
    print("3. Remove user")

    try:
        action = int(input("Enter action: "))
    except ValueError:
        print("Please enter a valid action")
        get_action()

    if action not in possible_actions.keys():
        print("Invalid action")
        get_action()

    return possible_actions[action], action

def get_confirmation(room, user, action):
    print(f"\nProvided info: ")
    print(f"Room: {room}")
    print(f"User: {user}")
    print(f"Action: {action}")
    response = input("Do you wish to proceed? (y/n): ")
    if response == 'y':
        return True
    else:
        return False

def check_if_exist(ps, *args):
    error_message = "HttpStatusCode=404"
    for a in args:
        if error_message in ps.run(f"Get-EXOMailbox -Identity {a}"):
            print(f"{a} does not exists. Wrong name")
            sys.exit()

    print(f"All data are correct")
    return True

# Get list of users able to approve or decline room booking
def get_users(ps, room):
    users = ps.run(f"(Get-CalendarProcessing -Identity '{room}').resourcedelegates")
    return users.split()

def main():
    ps = PowerShellSession()

    ps.run("Connect-ExchangeOnline -DisableWAM")

    # room = get_room()
    # user = get_user()
    # action = get_action()
    # confirmation = get_confirmation(room, user, action)
    #
    # if confirmation:
    #     check_if_exist(ps, room, user, action)
    # else:
    #     sys.exit()

    users = get_users(ps, "GCC.Room.Blue@lyreco.onmicrosoft.com")


    ps.run("Disconnect-ExchangeOnline")
    ps.close()


if __name__ == "__main__":
    main()