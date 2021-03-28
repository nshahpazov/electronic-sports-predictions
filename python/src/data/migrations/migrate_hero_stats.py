import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import os
import json

load_dotenv(find_dotenv())

MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")

def combine_hero_stats(hero, i):
    return {
        "percentile": hero["xp_per_min"][i]["percentile"],
        "xp_per_min": hero["xp_per_min"][i]["value"],
        "kills_per_min": hero["kills_per_min"][i]["value"],
        "hero_damage_per_min": hero["hero_damage_per_min"][i]["value"],
        "last_hits_per_min": hero["last_hits_per_min"][i]["value"],
        "hero_healing_per_min": hero["hero_healing_per_min"][i]["value"],
        "tower_damage": hero["tower_damage"][i]["value"],
        "gold_per_min": hero["gold_per_min"][i]["value"],
        "hero_id": hero["hero_id"]
    }

if __name__ == "__main__":
    # database connections
    conn = sqlite3.connect('./datasets/db/dota.db')
    c = conn.cursor()

    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]
    benchmark = db.benchmark

    # load the data from mongo
    hero_stats_mongo_query = json.load(open('src/data/migrations/hero_stats_query.json'))
    hero_stats_collection = benchmark.aggregate(hero_stats_mongo_query)

    # transform the data into table format
    hero_stats = [combine_hero_stats(h, i) for h in hero_stats_collection for i in range(10)]

    # prepare the sql query
    hero_stats_keys = hero_stats[0].keys()
    cols_str = ", ".join(hero_stats_keys)
    place_holders = ",".join(["?"] * len(hero_stats_keys))
    hero_stats_rows = [tuple(hero_stat[k] for k in hero_stats_keys) for hero_stat in hero_stats]
    insert_query = 'INSERT INTO hero_stats(%s) VALUES(%s);' % (cols_str, place_holders)

    # execute the query and close the connection
    c.executemany(insert_query, hero_stats_rows);
    print('We have inserted', c.rowcount, 'records to the table.')

    conn.commit()
    conn.close()
