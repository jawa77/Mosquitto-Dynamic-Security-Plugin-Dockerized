# Mosquitto Dynamic Security Plugin Dockerized

## Overview

This repository provides a Dockerized version of the Mosquitto MQTT broker with a dynamic security plugin for flexible authentication and authorization. It simplifies deployment and management using Docker Compose, making it ideal for secure MQTT messaging in various industries.

## Installation and Usage

1. **Clone the Repository:**

```
git clone https://github.com/jawa77/Mosquitto-Dynamic-Security-Plugin-Dockerized.git
cd Mosquitto-Dynamic-Security-Plugin-Dockerized
```

2. **Install Required Tools:**

Install `mosquitto_ctrl` and other necessary tools.

3. **Initialize Dynamic Security Plugin:**

```
mosquitto_ctrl dynsec init /mosquitto/config/dynamic-security.json admin
```

Follow the prompts to set up the admin user password.

4. **Update Configuration Files:**

- Replace `<admin_username>` and `<admin_password>` with appropriate values in `mosquitto/config/*` and `mosquitto/data/*` files.
- Update paths in `mosquitto/config/mosquitto.conf` file.

5. **Change Ports in `docker-compose.yml`:**

Update the ports according to your requirements.

6. **Start Containers using Docker Compose:**

```
docker-compose up -d
```


One container will run after this step.

7. **Automation Script:**

Execute the automation script for user management:

```
bash automation_script.sh
```

This script performs various actions like creating users, deleting users, adding topics, removing topics, and changing passwords.

## Automation Script Commands

- **Create User:**
```
docker exec -it container-id /mosquitto/data/createUser.sh username password
```

- **Delete User:**
```
docker exec -it mosquitto.myservice.com /bin/bash /mosquitto/data/delclient.sh username
```

- **Add Topic:**
```
docker exec -it mosquitto.myservice.com /bin/bash /mosquitto/data/addTopic.sh username acl topic
```

- **Remove Topic:**
```
docker exec -it mosquitto.myservice.com /bin/bash /mosquitto/data/removeTop.sh username acl topic
```

- **Change Password:**
```
docker exec -it mosquitto.myservice.com /bin/bash /mosquitto/data/passchange.sh username new_password
```

## Python Controller

For advanced automation and integration with web and app platforms, refer to the Python controller scripts in the `controller` folder.

## Benefits of Mosquitto Dynamic Security

- Enhanced security through dynamic authentication and authorization mechanisms.
- Easy deployment and scalability with Docker Compose.
- Customizable user management through automation scripts.
- Seamless integration with web and app platforms for efficient MQTT messaging.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Contact

For any inquiries or feedback, please contact [your-email@example.com](mailto:your-email@example.com).



