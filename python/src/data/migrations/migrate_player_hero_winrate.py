import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
SQLITE_DATABASE_URL = os.environ.get("SQLITE_DATABASE_URL")


WIN_RATE_KEYS = [
  "account_id",
  "hero_id",
  "last_played",
  "games",
  "win",
  "with_games",
  "with_win",
  "against_games",
  "against_win"
]

def to_row(wr) -> tuple:
    default = {
        "account_id": -1,
        "hero_id": -1,
        "last_played": -1,
        "games": 0,
        "win": 0,
        "with_games": 0,
        "with_win": 0,
        "against_games": 0,
        "against_win": 0
    }

    return tuple((default | wr)[k] for k in WIN_RATE_KEYS)

if __name__ == "__main__":
    # database connections
    conn = sqlite3.connect(SQLITE_DATABASE_URL)
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]
    player_collection = db.player

    # load the data from mongodb
    player_hero_winrates = player_collection.aggregate([{
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

    player_hero_winrate_rows = [to_row(wr) for wr in player_hero_winrates]

    # execute the query and close the connection
    print('We have inserted', c.rowcount, 'records to the match_player table.')


    # prepare the query
    cols_str = ", ".join(WIN_RATE_KEYS)
    insert_query = 'INSERT INTO player_hero_win_rate(%s) VALUES(?,?,?,?,?,?,?,?,?);' % cols_str

    # execute the query
    c.executemany(insert_query, player_hero_winrate_rows)
    print('We have inserted', c.rowcount, 'records to the table.')

    conn.commit()
    conn.close()
