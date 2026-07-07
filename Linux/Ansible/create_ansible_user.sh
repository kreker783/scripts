#!/bin/bash
set -euo pipefail # Stop if error

USERNAME="ansible"

useradd -m -s /bin/bash "$USERNAME"
echo "User '$USERNAME' created."

echo "Set a password for '$USERNAME':"
passwd "$USERNAME"

usermod -aG sudo "$USERNAME"
echo "Added '$USERNAME' to group sudo"

#passwordless sudo from playbook
SUDOERS_FILE="/etc/sudoers.d/${USERNAME}"
echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > "$SUDOERS_FILE"
chmod 440 "$SUDOERS_FILE"

visudo -cf "$SUDOERS_FILE"

echo
echo "Done. '$USERNAME' now has passwordless sudo access."
