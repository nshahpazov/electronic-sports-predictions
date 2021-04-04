import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")

if __name__ == "__main__":
    # database connections
    conn = sqlite3.connect('./datasets/db/dota.db')
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]
    player_collection = db.player

    # load the data from mongodb
    player_heroes = player_collection.aggregate([{
        "$set": {
            "heroes.account_id": "$account_id"
        }
    }, {
        "$unwind": "$heroes"
    }, {
        "$replaceRoot": {
            "newRoot": "$heroes"
        }
    }, {"$project": {"_id": 0}}])

    # prepare the query
    winrate_str = ", ".join(player_collection.find_one()["heroes"][0].keys()) + ", account_id"
    insert_query = 'INSERT INTO player_hero_win_rate(%s) VALUES(?,?,?,?,?,?,?,?,?);' % winrate_str

    # execute the query
    c.executemany(insert_query, [tuple(d[k] for k in d.keys()) for d in player_heroes]);
    print('We have inserted', c.rowcount, 'records to the table.')

    conn.commit()
    conn.close()
