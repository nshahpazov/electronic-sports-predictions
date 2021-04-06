import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

# constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
SQLITE_DATABASE_URL = os.environ.get("SQLITE_DATABASE_URL")

MATCH_KEYS = [
    "barracks_status_dire",
    "match_id",
    "duration",
    "radiant_win",
    "tower_status_dire",
    "tower_status_radiant",
    "human_players",
    "start_time",
    "game_mode"
]

if __name__ == "__main__":
    # database connections
    conn = sqlite3.connect(SQLITE_DATABASE_URL)
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]

    # load the data from mongodb
    matches = db.matches.find({}, { k: 1 for k in MATCH_KEYS })

    # prepare the sql query
    cols_str = ", ".join(MATCH_KEYS)
    place_holders = ",".join(["?"] * len(MATCH_KEYS))
    insert_query = "INSERT INTO match(%s) VALUES(%s);" % (cols_str, place_holders)

    match_player_rows = [tuple(match[k] for k in MATCH_KEYS) for match in matches]

    # execute the query and close the connection
    c.executemany(insert_query, match_player_rows)
    print('We have inserted', c.rowcount, 'records to the match table.')

    conn.commit()
    conn.close()
