import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os

load_dotenv(find_dotenv())

MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")

def merge_hero_stats(hero, i):
    return {
        "percentile": hero["xp_per_min"][i]["percentile"],
        "hero_id": hero["hero_id"]
    } | {k: hero[k][i]["value"] for k in hero.keys() if k != "hero_id"}

if __name__ == "__main__":

    # database connections
    conn = sqlite3.connect('./datasets/db/dota.db')
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]

    # load the data from mongodb
    hero_stats_collection = db.benchmark.aggregate([{
        "$set": {
        "result.hero_id": "$hero_id"
        }
    },{
        "$replaceRoot": {
        "newRoot": "$result"
        }
    }])

    # transform the data into table format
    hero_stats = [merge_hero_stats(h, i) for h in hero_stats_collection for i in range(10)]

    # prepare the sql query
    hero_stats_keys = hero_stats[0].keys()
    cols_str = ", ".join(hero_stats_keys)
    place_holders = ",".join(["?"] * len(hero_stats_keys))
    hero_stats_rows = [tuple(hero_stat[k] for k in hero_stats_keys) for hero_stat in hero_stats]
    insert_query = 'INSERT INTO hero_stats(%s) VALUES(%s);' % (cols_str, place_holders)

    # execute the query and close the connection
    c.executemany(insert_query, hero_stats_rows);
    print('We have inserted', c.rowcount, 'records to the table.')

    # TODO: next: persist players info
    # TODO: prepare the player_hero_attr data with SQL

    conn.commit()
    conn.close()
