import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

# constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")

MATCH_PLAYER_KEYS = [
    "match_id", "account_id", "player_slot", "hero_id", "gold", "hero_healing", "gold_per_min",
    "deaths", "hero_damage", "scaled_hero_damage", "last_hits", "denies", "assists", "level",
    "scaled_hero_healing", "tower_damage", "xp_per_min", "kills", "scaled_tower_damage"
]

def to_row(player):
    return tuple(({"mmr_std_dev": None, "mmr_n": None } | player)[k] for k in PLAYER_KEYS)

if __name__ == "__main__":
    # database connections
    conn = sqlite3.connect('./datasets/db/dota.db')
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
    }])

    # prepare the sql query
    cols_str = ", ".join(MATCH_PLAYER_KEYS)
    place_holders = ",".join(["?"] * len(MATCH_PLAYER_KEYS))
    insert_query = "INSERT INTO match_player(%s) VALUES(%s);" % (cols_str, place_holders)

    match_player_rows = [player for player in match_players]

    # execute the query and close the connection
    c.executemany(insert_query, match_player_rows)
    print('We have inserted', c.rowcount, 'records to the players table.')

    conn.commit()
    conn.close()