import motor.motor_asyncio

from src.bot.config import MONGO_USER, MONGO_USER_PASSWORD, MONGO_DB


def get_mongo_client():
    conn_str = f"mongodb+srv://{MONGO_USER}:{MONGO_USER_PASSWORD}@cluster0.eefnp.mongodb.net/{MONGO_DB}?retryWrites=true&w=majority"
    client = motor.motor_asyncio.AsyncIOMotorClient(
        conn_str, serverSelectionTimeoutMS=5000)
    return client
