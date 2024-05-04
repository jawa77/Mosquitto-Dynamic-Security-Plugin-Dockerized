#!/bin/bash

# Predefined admin credentials
ADMIN_USER="admin"
ADMIN_PASS='adminpassword' # Using single quotes in bash to handle special characters

# New client username and password from command line arguments
CLIENT_USER="$1"
CLIENT_PASS="$2"

# Check for necessary number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <NewClientUsername> <NewClientPassword>"
    exit 1
fi

# Function to check if the client already exists
function client_exists {
    mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec listClients | grep -q "$CLIENT_USER"
    return $?
}

# Check if client already exists
if client_exists; then
    echo "Error: Client '$CLIENT_USER' already exists."
    exit 1
else
    echo "Client '$CLIENT_USER' does not exist. Creating now..."
fi

# Use expect to automate the interaction
expect <<EOF
set timeout 1
spawn mosquitto_ctrl -u "$ADMIN_USER" -P {$ADMIN_PASS} dynsec createClient "$CLIENT_USER"
expect "Enter new password for $CLIENT_USER:"
send "$CLIENT_PASS\r"
expect "Reenter password for $CLIENT_USER:"
send "$CLIENT_PASS\r"
expect eof
EOF

echo "Client '$CLIENT_USER' created successfully."
