#!/bin/bash

# Variables
ADMIN_USER="admin"
ADMIN_PASS='adminpassword'  # Use single quotes to safely include special characters

# Client username is provided as the first argument
CLIENT_USER="$1"
ROLE_NAME="${CLIENT_USER}Role"

# Fetch current role details using mosquitto_ctrl
ROLE_DETAILS=$(mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec getRole "$ROLE_NAME")

# Use jq to parse the role details and extract topics
TOPICS=$(echo "$ROLE_DETAILS" | jq -r '.role.acls[].topic')

# Remove each ACL associated with the role
for TOPIC in $TOPICS; do
    mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec removeRoleACL "$ROLE_NAME" publishClientSend "$TOPIC"
    mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec removeRoleACL "$ROLE_NAME" subscribeLiteral "$TOPIC"
done

# Delete the role
mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec deleteRole "$ROLE_NAME"

# Delete the client
mosquitto_ctrl -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec deleteClient "$CLIENT_USER"
