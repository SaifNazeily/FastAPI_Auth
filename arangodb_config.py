from arango import ArangoClient

class ArangoDB:
    def __init__(self):
        client = ArangoClient(hosts='http://localhost:8529')
        self.db = client.db('user_info', username='root', password='yourpassword')

    # Create a new user
    def create_user(self, user_data):
        users_collection = self.db.collection('fastapi_collection')
        users_collection.insert(user_data)

    # Get a user by username
    def get_user(self, username):
        users_collection = self.db.collection('fastapi_collection')
        cursor = users_collection.find({'username': username})
        return next(cursor, None)

    # Update the verified status of a user
    def update_user_verified(self, username):
        users_collection = self.db.collection('fastapi_collection')
        user = self.get_user(username)
        if user:
            users_collection.update({'_key': user['_key'], 'verified': True})

    # Delete a user by username
    def delete_user(self, username):
        users_collection = self.db.collection('fastapi_collection')
        user = self.get_user(username)
        if user:
            users_collection.delete({'_key': user['_key']})
