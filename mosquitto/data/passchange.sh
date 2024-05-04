#!/bin/bash

# Check for necessary number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <newPassword>"
    exit 1
fi

# Admin credentials for mosquitto_ctrl
ADMIN_USER="admin"
ADMIN_PASS='adminpassword'

# Client username and new password provided as arguments
CLIENT_USER="$1"
NEW_PASSWORD="$2"

# Change the client's password using mosquitto_ctrl
mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setClientPassword "$CLIENT_USER" "$NEW_PASSWORD"

# Check for success
if [ $? -eq 0 ]; then
    echo "Password for client '$CLIENT_USER' changed successfully."
else
    echo "Failed to change password for client '$CLIENT_USER'."
fi
