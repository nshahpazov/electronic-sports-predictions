import sqlite3
from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient
import json
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

    # load the mongo query file
    rankings_query_file = open('./src/data/migrations/queries/rankings_aggregate_query.json')
    rankings_mongo_aggregate_query = json.load(rankings_query_file)

    # load the data from mongodb
    rankings = db.player.aggregate(rankings_mongo_aggregate_query)

    # transform the data into table format
    ranking_keys = list(db.player.find_one()["heroes_rankings"][0].keys()) + ["account_id"]

    # prepare the sql query
    cols_str = ", ".join(ranking_keys)
    place_holders = ",".join(["?"] * len(ranking_keys))
    insert_query = "INSERT INTO player_heroes_ranking(%s) VALUES(%s);" % (cols_str, place_holders)

    ranking_rows = [tuple(r[k] for k in ranking_keys) for r in rankings if "account_id" in r]

    # execute the query and close the connection
    c.executemany(insert_query, ranking_rows)
    print('We have inserted', c.rowcount, 'records to the table player_heroes_ranking.')

    conn.commit()
    conn.close()
