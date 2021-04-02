import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

# constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")

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

def to_row(match):
    default = {
        "gold": None,
        "hero_healing": None,
        "hero_damage": None,
        "tower_damage": None
    }

    return tuple((match)[k] for k in MATCH_KEYS)

if __name__ == "__main__":
    # database connections
    conn = sqlite3.connect('./datasets/db/dota.db')
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]

    # load the data from mongodb
    matches = db.matches.find({}, { k: 1 for k in MATCH_KEYS })

    # prepare the sql query
    cols_str = ", ".join(MATCH_KEYS)
    place_holders = ",".join(["?"] * len(MATCH_KEYS))
    insert_query = "INSERT INTO match(%s) VALUES(%s);" % (cols_str, place_holders)

    match_player_rows = [to_row(match) for match in matches]

    # execute the query and close the connection
    c.executemany(insert_query, match_player_rows)
    print('We have inserted', c.rowcount, 'records to the match table.')

    conn.commit()
    conn.close()
