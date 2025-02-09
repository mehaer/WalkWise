import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")  # Store in .env file
client = MongoClient(MONGO_URI)
db = client.walkwise  # Your database
audio_collection = db.audio_files  # Collection for audio metadata

if __name__ == "__main__":
    # Verifiy the connection
    try:
        # Run a test command
        print("🔄 Connecting to MongoDB Atlas...")
        db.command("ping")  # Ping MongoDB to check connection
        print("✅ MongoDB Atlas connection successful!")

        # Insert a test document
        test_data = {"test": "MongoDB connection is working!"}
        inserted_id = audio_collection.insert_one(test_data).inserted_id
        print(f"📝 Test document inserted with ID: {inserted_id}")

        # # Retrieve the test document
        # retrieved_data = audio_collection.find_one({"_id": inserted_id})
        # print("📄 Retrieved Data:", retrieved_data)

        # Cleanup: Delete the test document
        # audio_collection.delete_one({"_id": inserted_id})
        # print("🗑 Test document deleted. Connection verified successfully!")

    except Exception as e:
        print("❌ MongoDB Connection Failed:", e)