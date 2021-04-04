import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
SQLITE_DATABASE_URL = os.environ.get("SQLITE_DATABASE_URL")

if __name__ == "__main__":

    # database connections
    conn = sqlite3.connect(SQLITE_DATABASE_URL)
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]

    # load the data from mongodb
    ratings = db.player.aggregate([{
        "$set": { "ratings.account_id": "$account_id" }
    }, {
        "$unwind": "$ratings"
    }, {
        "$replaceRoot": { "newRoot": "$ratings" }
    }])

    # transform the data into table format
    rating_keys = list(db.player.find_one()["ratings"][0].keys()) + ["account_id"]

    # prepare the sql query
    cols_str = ", ".join(rating_keys)
    place_holders = ",".join(["?"] * len(rating_keys))
    insert_query = "INSERT INTO player_match_rating(%s) VALUES(%s);" % (cols_str, place_holders)

    rating_rows = [tuple(r[k] for k in rating_keys) for r in ratings if "account_id" in r]

    # execute the query and close the connection
    c.executemany(insert_query, rating_rows)
    print('We have inserted', c.rowcount, 'records to the table.')

    conn.commit()
    conn.close()
