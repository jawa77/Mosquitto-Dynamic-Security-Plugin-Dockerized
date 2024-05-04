import pymongo
import time


class MosquittoUserController:
    def __init__(self, email):
        self.email = email
        self.client = pymongo.MongoClient("connectiom string here")
        self.db = self.client.service_mosquitto
        self.userDB = self.db.userdb
        self.serviceManager = self.db.servicemanager
        self.topicDB=self.db.topicDB

    def create_user(self, username, password):
       
        # Check if the username already exists in the userDB
        if self.user_exists(username):
            raise Exception("User already exists")

        # Check if the user limit has been exceeded or if the document doesn't exist
        service_data = self.serviceManager.find_one({"email": self.email})
        if not service_data:
            # Create default service manager document if it does not exist
            self.serviceManager.insert_one({
                "email": self.email,
                "username": username,  # assuming username is the same as email
                "user_limit": 3,
                "topic_limit": 6,
                "usercount": 0,
                "topiccount": 0
            })
            service_data = self.serviceManager.find_one({"email": self.email})

  

        if service_data["usercount"] >= service_data["user_limit"]:
            raise Exception("User limit exceeded")

        # Add user to the userDB
        user_data = {
            "name": username,
            "email": self.email,
            "created_at": time.time(),
            "password": password
        }
        self.userDB.insert_one(user_data)
   

        # Increment the user count in the service manager
        self.serviceManager.update_one(
            {"email": self.email},
            {"$inc": {"usercount": 1}}
        )
       
        return "User created successfully."

    def user_exists(self, username):
        # Check if a user exists in the userDB
        return bool(self.userDB.find_one({"name": username}))

    def is_user_limit_exceeded(self):
        # Check if the user count exceeds the limit in the service manager
        service_data = self.serviceManager.find_one({"email": self.email})
        if not service_data:
            return False  # No entry means no limit exceeded
        return service_data["usercount"] >= service_data["user_limit"]

    def is_topic_limit_exceeded(self):
        # Check if the user count exceeds the limit in the service manager
        service_data = self.serviceManager.find_one({"email": self.email})
        print(service_data['topiccount'],service_data['topic_limit'])
        if not service_data:
            print("here")
            return 404  # No entry means no limit exceeded
        return service_data["topiccount"] >= service_data["topic_limit"]

    def delete_user(self, username):
        # Check if the user exists
        if not self.user_exists(username):
            raise Exception("User does not exist")

        # Delete user's topics from topicdb and decrement topic count
        topic_delete_result = self.topicDB.delete_many({"username": username, "email": self.email})
        if topic_delete_result.deleted_count > 0:
            # Decrement the topic count in the service manager for each deleted topic
            self.serviceManager.update_one(
                {"email": self.email},
                {"$inc": {"topiccount": -topic_delete_result.deleted_count}}
            )

        # Delete the user from userDB
        delete_result = self.userDB.delete_one({"name": username, "email": self.email})
        if delete_result.deleted_count == 0:
            raise Exception("No user found with the specified username and email.")

        # Decrement the user count in the service manager
        update_result = self.serviceManager.update_one(
            {"email": self.email},
            {"$inc": {"usercount": -1}}  # Correct MongoDB syntax for decrementing
        )
        if update_result.matched_count == 0:
            raise Exception("Failed to update user count: No service manager record found for this email.")
        
        print("newscript")

        return "User and related topics deleted successfully."

    def topic_exists(self, username, topic, acl):
        return bool(self.topicDB.find_one({
            "username": username,
            "topic": topic,
            "acl": acl
        }))

    def add_topic(self, username, acl, topic):
        # Check service limits first
        service_data = self.serviceManager.find_one({"email": self.email})
        if not service_data:
            return "No service data found"

        current_topic_count = service_data.get('topiccount', 0)
        topic_limit = service_data.get('topic_limit', float('inf'))
        if current_topic_count >= topic_limit:
            return "Topic limit exceeded"

        if not self.user_exists(username):
            return "User does not exist. Please create the user first before adding topics."

        existing_topic = self.topicDB.find_one({"username": username, "topic": topic})

        if existing_topic:
            current_acl = existing_topic['acl']
            # Determine if an update to 'both' is necessary
            if acl == 'both' or current_acl == 'both':
                if current_acl != 'both':  # Update needed only if current ACL is not already 'both'
                    self.topicDB.update_one(
                        {"_id": existing_topic['_id']},
                        {"$set": {"acl": 'both'}}
                    )
                    return "ACL for topic updated to both successfully"
                return "No update needed; the topic already has full ACL."
            elif acl != current_acl:
                # This case handles when existing ACL is 'pub' or 'sub' and a different one is added
                self.topicDB.update_one(
                    {"_id": existing_topic['_id']},
                    {"$set": {"acl": 'both'}}
                )
                return "ACL for topic updated to both successfully"

        # Insert the new topic if no existing topic is found
        new_topic = {
            "username": username,
            "email": self.email,
            "topic": topic,
            "acl": acl,
            "created_at": time.time()
        }
        self.topicDB.insert_one(new_topic)
        self.serviceManager.update_one(
            {"email": self.email},
            {"$inc": {"topiccount": 1}}
        )

        return "Topic added to database successfully."
               
    def remove_topic(self, username, acl_type, topic_name):
        # Check if the topic exists with the correct ACL type
        topic_data = self.topicDB.find_one({
            "username": username,
            "email": self.email,
            "topic": topic_name,  
            "acl": acl_type   
        })

        if not topic_data:
            return "Topic does not exist or ACL configuration does not match."

        # Remove the topic from the database
        self.topicDB.delete_one({
            "username": username,
            "email": self.email,
            "topic": topic_name,
            "acl": acl_type
        })

        self.serviceManager.update_one(
        {"email": self.email},
        {"$inc": {"topiccount": -1}})

        return "Topic removed successfully from database."

    def check_user(self, username):
        # Check both username and email
        user = self.userDB.find_one({"name": username, "email": self.email})
        return user is not None
    
    def change_password(self, username, new_password):
        if not self.check_user(username):
            return "User does not exist with provided username and email."

        # Update the password in the database
        result = self.userDB.update_one(
            {"name": username, "email": self.email},
            {"$set": {"password": new_password}}
        )

        if result.modified_count == 0:
            return "Password update failed. No changes were made."
        
        return "Password successfully updated in database."
    
    def get_users_by_email(self):
            # Fetch all user documents from userDB where the email matches
            # Only retrieve the name and password fields
            users_cursor = self.userDB.find({"email": self.email}, {"name": 1, "password": 1, "_id": 0})
            users = list(users_cursor)

            return users


    def get_topics_by_email(self):
        # Fetch all topic documents from topicDB where the email matches
        # Only retrieve the username, topic, and acl fields
        topics_cursor = self.topicDB.find({"email": self.email}, {"username": 1, "topic": 1, "acl": 1, "_id": 0})
        topics = list(topics_cursor)

        return topics
    
    def get_usernames(self):
        # Fetch all documents from userDB where the email matches
        # Only retrieve the username field
        user_cursor = self.userDB.find({"email": self.email}, {"name": 1, "_id": 0})
        usernames = [user['name'] for user in user_cursor]  # Extract names from the cursor and create a list

        return usernames