#!/bin/bash

# Constants for admin credentials
ADMIN_USER="admin"
ADMIN_PASS='adminpassword'

# Utility to call Mosquitto Control Tool
MOSQUITTO_CTRL="mosquitto_ctrl -u $ADMIN_USER -P $ADMIN_PASS dynsec"

# Function to check if a client exists
function check_client_exists {
    local username=$1
    echo "Checking if client $username exists..."
    if $MOSQUITTO_CTRL listClients | grep -q "$username"; then
        echo "Client $username exists."
        return 0
    else
        echo "Error: Client $username does not exist. Please create the client first."
        exit 1
    fi
}

# Function to add a topic to a role
function add_topic_to_role {
    local username=$1
    local acl_type=$2
    local topic=$3
    local role_name="${username}Role"

    # Check if role exists and create if not
    if ! $MOSQUITTO_CTRL getRole $role_name | grep -q '"rolename"'; then
        echo "Creating role $role_name..."
        $MOSQUITTO_CTRL createRole $role_name
    else
        echo "Role $role_name already exists."
    fi

    # Add publish ACL if requested
    if [[ "$acl_type" == "pub" || "$acl_type" == "both" ]]; then
        echo "Adding publish ACL for $topic to $role_name..."
        $MOSQUITTO_CTRL addRoleACL $role_name publishClientSend $topic allow
    fi

    # Add subscribe ACL if requested
    if [[ "$acl_type" == "sub" || "$acl_type" == "both" ]]; then
        echo "Adding subscribe ACL for $topic to $role_name..."
        $MOSQUITTO_CTRL addRoleACL $role_name subscribeLiteral $topic allow
    fi

    # Assign role to client if not already assigned
    echo "Assigning role $role_name to $username..."
    $MOSQUITTO_CTRL addClientRole $username $role_name 1
}

# Main script execution
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <username> <acl (pub|sub|both)> <topic>"
    exit 1
fi

username=$1
acl_type=$2
topic=$3

# Ensure client exists
check_client_exists $username

# Add topic with appropriate ACLs
add_topic_to_role $username $acl_type $topic

echo "Completed modifications for $username."
