from pymongo import MongoClient


class ManageDB:
    def __init__(self, db_name="chatbot_db", collection_name="conversations"):
        """Initialize MongoDB connection."""
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_conversation(self, conversation):
        """Save a conversation to the database."""
        self.collection.insert_one({"conversation": conversation})

    def load_conversations(self):
        """Load all previous conversations from the database."""
        return list(self.collection.find())

    def clear_conversations(self):
        """Clear all conversations from the database."""
        self.collection.delete_many({})