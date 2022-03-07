async def create_user_handler(db, telegram_id):
    new_user = await db["user"].insert_one({"telegram_id": telegram_id, "stocks": []})
    user = await db["user"].find_one({"_id": new_user.inserted_id})
    return user


async def fetch_one_user_handler(db, telegram_id):
    user = await db["user"].find_one({"telegram_id": telegram_id})
    return user


async def add_user_stocks_handler(db, telegram_id, stocks):
    added = await db["user"].update_one({"telegram_id": telegram_id},
                                        {"$push": {"stocks": {"$each": stocks}}})
    return added


async def delete_user_stocks_handler(db, telegram_id, stocks):
    deleted = await db["user"].update_one({"telegram_id": telegram_id},
                                          {"$pull": {"stocks": {"$in": stocks}}})
    return deleted
