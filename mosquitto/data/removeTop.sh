#!/bin/bash

# Check for necessary number of arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <username> <aclType> <topic>"
    echo "aclType should be 'pub', 'sub', or 'both'"
    exit 1
fi

USERNAME="$1"
ACL_TYPE="$2"
TOPIC="$3"
ROLE_NAME="${USERNAME}Role"  # Construct role name from username

# Define admin credentials (adjust as necessary)
ADMIN_USER="admin"
ADMIN_PASS='adminpassword'

# Function to remove publish ACL
remove_publish() {
    mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec removeRoleACL "$ROLE_NAME" publishClientSend "$TOPIC"
}

# Function to remove subscribe ACL
remove_subscribe() {
    mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec removeRoleACL "$ROLE_NAME" subscribeLiteral "$TOPIC"
}

# Decide based on aclType argument
case "$ACL_TYPE" in
    pub)
        remove_publish
        ;;
    sub)
        remove_subscribe
        ;;
    both)
        remove_publish
        remove_subscribe
        ;;
    *)
        echo "Invalid ACL type: $ACL_TYPE"
        echo "Use 'pub', 'sub', or 'both'"
        exit 1
        ;;
esac

echo "ACL removal complete for $TOPIC in $ROLE_NAME."

