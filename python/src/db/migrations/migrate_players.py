import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

# constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
SQLITE_DATABASE_URL = os.environ.get("SQLITE_DATABASE_URL")

PLAYER_KEYS = [
    "account_id", "win", "competitive_rank", "mmr_estimate",
    "lose", "solo_competitive_rank", "mmr_std_dev", "mmr_n"
]

def to_row(player):
    return tuple(({"mmr_std_dev": None, "mmr_n": None } | player)[k] for k in PLAYER_KEYS)


if __name__ == "__main__":
    # database connections
    conn = sqlite3.connect(SQLITE_DATABASE_URL)
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]

    # load the data from mongodb
    players = db.player.aggregate([{
        "$set": {
            "mmr_estimate": "$mmr_estimate.estimate",
            "mmr_std_dev": "$mmr_estimate.stdDev",
            "mmr_n": "$mmr_estimate.n"
        }
    }, {
        "$project": { "heroes": 0, "profile": 0, "heroes_rankings": 0, "_id": 0, "ratings": 0 }
    }, {
        "$project": {
            "account_id": 1,
            "competitive_rank": 1,
            "solo_competitive_rank": 1,
            "mmr_estimate": 1,
            "mmr_std_dev": 1,
            "mmr_n": 1,
            "win": { "$ifNull": [ "$win_lose.win", "$win" ] },
            "lose": { "$ifNull": [ "$win_lose.lose", "$lose" ] }
        }
    }])

    # prepare the sql query
    cols_str = ", ".join(PLAYER_KEYS)
    place_holders = ",".join(["?"] * len(PLAYER_KEYS))
    insert_query = "INSERT INTO player(%s) VALUES(%s);" % (cols_str, place_holders)

    player_rows = [to_row(player) for player in players if "account_id" in player]

    # execute the query and close the connection
    c.executemany(insert_query, player_rows)
    print('We have inserted', c.rowcount, 'records to the players table.')

    conn.commit()
    conn.close()
