import subprocess
import json
from .MosquittoUserController import MosquittoUserController

class MosquittoController:
    def __init__(self, email):
        self.user_controller = MosquittoUserController(email)

    def create_mosquitto_user(self, username, password):
        # Attempt to create the user in the database first
        try:
            self.user_controller.create_user(username, password)
        except Exception as e:
            return json.dumps({'status': 'failure', 'message': str(e)})
        
       
        # If successful, execute the shell command to create the user in Mosquitto
        command = [
            "docker", "exec", "mosquitto.myservice.com",
            "/bin/bash", "/mosquitto/data/createUser.sh", username, password
        ]

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return json.dumps({'status_code': 200, 'status': 'success', 'message': f"User {username} created successfully in Mosquitto."})
            else:
                return json.dumps({'status_code': 500, 'status': 'failure', 'message': f"Failed to create Mosquitto user {username}: {result.stderr}"})
        except subprocess.CalledProcessError as e:
            return json.dumps({'status_code': 500, 'status': 'error', 'message': f"An error occurred: {str(e)}"})


    def delete_mosquitto_user(self, username):
    # Attempt to delete the user in the database first
        try:
            print("Deleting user in database...")
            self.user_controller.delete_user(username)
        except Exception as e:
            return json.dumps({'status_code': 400, 'status': 'error', 'message': str(e)})

        # If successful, execute the shell command to delete the user in Mosquitto
        command = [
            "docker", "exec", "mosquitto.myservice.com",
            "/bin/bash", "/mosquitto/data/delclient.sh", username
        ]

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return json.dumps({'status_code': 200, 'status': 'success', 'message': f"User {username} deleted successfully in Mosquitto."})
            else:
                return json.dumps({'status_code': 500, 'status': 'failure', 'message': f"Failed to delete Mosquitto user {username}: {result.stderr}"})
        except subprocess.CalledProcessError as e:
            return json.dumps({'status_code': 500, 'status': 'error', 'message': f"An error occurred: {str(e)}"})


    def add_topic(self, username, acl, topic):
        # First, add the topic in the database using MosquittoUserController
        db_result = self.user_controller.add_topic(username, acl, topic)
        if "successfully" not in db_result:
            return json.dumps({'status_code': 400, 'status': 'failure', 'message': db_result})

        # If successful, execute the shell command to update Mosquitto configuration
        command = [
            "docker", "exec", "mosquitto.myservice.com",
            "/bin/bash", "/mosquitto/data/addTopic.sh", username, acl, topic
        ]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return json.dumps({'status_code': 200, 'status': 'success', 'message': "Topic added successfully and Mosquitto configuration updated."})
            else:
                return json.dumps({'status_code': 500, 'status': 'failure', 'message': f"Failed to update Mosquitto configuration: {result.stderr}"})
        except subprocess.CalledProcessError as e:
            return json.dumps({'status_code': 500, 'status': 'error', 'message': f"Failed to update Mosquitto configuration: {e.stderr}"})


    def remove_topic(self, username, acl, topic):
        # First, remove the topic in the database using MosquittoUserController
        db_result = self.user_controller.remove_topic(username, acl, topic)
        if "successfully" not in db_result:
            return json.dumps({'status_code': 400, 'status': 'failure', 'message': db_result})

        # If successful, execute the shell command to update Mosquitto configuration
        command = [
            "docker", "exec", "mosquitto.myservice.com",
            "/bin/bash", "/mosquitto/data/removeTop.sh", username, acl, topic
        ]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return json.dumps({'status_code': 200, 'status': 'success', 'message': "Topic removed successfully and Mosquitto configuration updated."})
            else:
                return json.dumps({'status_code': 500, 'status': 'failure', 'message': f"Failed to remove Mosquitto topic: {result.stderr}"})
        except subprocess.CalledProcessError as e:
            return json.dumps({'status_code': 500, 'status': 'error', 'message': f"Failed to update Mosquitto configuration: {e.stderr}"})

        
    def change_password(self, username, new_password):
        db_result = self.user_controller.change_password(username, new_password)
        if "successfully" not in db_result:
            return json.dumps({'status_code': 400, 'status': 'failure', 'message': db_result})

        command = [
            "docker", "exec", "mosquitto.myservice.com",
            "/bin/bash", "/mosquitto/data/passchange.sh", username, new_password
        ]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return json.dumps({'status_code': 200, 'status': 'success', 'message': "Password updated successfully in Mosquitto configuration."})
            else:
                return json.dumps({'status_code': 500, 'status': 'failure', 'message': f"Failed to update password in Mosquitto: {result.stderr}"})
        except subprocess.CalledProcessError as e:
            return json.dumps({'status_code': 500, 'status': 'error', 'message': f"Failed to update password in Mosquitto: {e.stderr}"})

    def get_user_data(self):
        user_data = self.user_controller.get_users_by_email()
        return json.dumps({'status_code': 200, 'status': 'success', 'data': user_data})

    def get_topic_data(self):
        topic_data = self.user_controller.get_topics_by_email()
        return json.dumps({'status_code': 200, 'status': 'success', 'data': topic_data})

    def get_usernames_data(self):
        usernames = self.user_controller.get_usernames()
        return json.dumps({'status_code': 200, 'status': 'success', 'data': usernames})