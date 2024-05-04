import subprocess

def run_command(command):
    """ Runs a shell command and returns the output as a list of lines. """
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return []

def get_roles():
    """ Retrieves a dictionary of roles and their ACLs. """
    roles_output = run_command("mosquitto_ctrl -u admin -P 'adminpass' dynsec listRoles")
    roles = {}
    for role in roles_output:
        if role and role != "Role":  # Ignore header or empty lines
            details = run_command(f"mosquitto_ctrl -u admin -P 'adminpass' dynsec getRole {role}")
            acl_list = [line.strip() for line in details if 'allow' in line]
            roles[role] = acl_list
    return roles

def get_clients():
    """ Retrieves clients and associates roles and topics from roles. """
    clients_output = run_command("mosquitto_ctrl -u admin -P 'adminpass' dynsec listClients")
    roles = get_roles()
    print("Username        | Role            | Topics & ACLs")
    print("---------------------------------------------------")
    for client in clients_output:
        if client and client != "admin":  # Assuming you want to exclude the admin user from the listing
            # Assuming role name follows a predictable pattern (clientName + 'Role')
            role_name = client + 'Role'
            acls = roles.get(role_name, [])
            acls_str = ", ".join(acls)
            print(f"{client:<16} | {role_name:<16} | {acls_str}")
        elif client == "admin":  # Just a printout for adminNinja without ACLs, for example
            print(f"{client:<16} | Admin role      | No ACLs displayed")

if __name__ == "__main__":
    get_clients()
