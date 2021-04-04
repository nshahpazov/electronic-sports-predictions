import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

# constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
SQLITE_DATABASE_URL = os.environ.get("SQLITE_DATABASE_URL")

MATCH_PLAYER_KEYS = [
    "match_id",
    "account_id",
    "player_slot",
    "hero_id",
    "gold",
    "deaths",
    "hero_damage",
    "last_hits",
    "denies",
    "tower_damage",
    "xp_per_min",
    "kills",
    "hero_healing",
    "assists",
    "gold_per_min",
    "level"
]

def to_row(player):
    default = {
        "gold": None,
        "hero_healing": None,
        "hero_damage": None,
        "tower_damage": None
    }

    return tuple((default | player)[k] for k in MATCH_PLAYER_KEYS)

if __name__ == "__main__":
    # database connections
    conn = sqlite3.connect(SQLITE_DATABASE_URL)
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]

    # load the data from mongodb
    match_players = db.matches.aggregate([{
        "$set": {"players.match_id": "$match_id"}
    }, {"$unwind": "$players"}, {
        "$replaceRoot": { "newRoot": "$players" }
    }, {
        "$project": {match_player_key: 1 for match_player_key in MATCH_PLAYER_KEYS}
    }
    # ,
    # {"$limit": 10000}
    ])

    # prepare the sql query
    cols_str = ", ".join(MATCH_PLAYER_KEYS)
    place_holders = ",".join(["?"] * len(MATCH_PLAYER_KEYS))
    insert_query = "INSERT INTO match_player(%s) VALUES(%s);" % (cols_str, place_holders)

    match_player_rows = [to_row(player) for player in match_players]

    # execute the query and close the connection
    c.executemany(insert_query, match_player_rows)
    print('We have inserted', c.rowcount, 'records to the match_player table.')

    conn.commit()
    conn.close()
