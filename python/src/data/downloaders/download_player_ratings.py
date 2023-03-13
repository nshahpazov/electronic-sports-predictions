import aiohttp
import asyncio
import os
from dotenv import find_dotenv, load_dotenv
import logging
import sqlite3
import time
import numpy as np

load_dotenv(find_dotenv())

# env constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
OPENDOTA_API_KEY = os.environ.get("OPEN_DOTA_API_KEY")

SELECT_ACCOUNT_IDS = "SELECT DISTINCT account_id FROM match_player;"
SELECT_ACCOUNT_IDS_PRESENT = "SELECT DISTINCT account_id FROM player_match_rating_v2;"
PLAYERS_URI  = "https://api.opendota.com/api/players"
RATINGS_TABLE = 'player_match_rating_v2'


def query_unique_account_ids():
    no_ratings_ids = np.load("./no_ratings_ids.npy")
    conn = sqlite3.connect('./datasets/db/dota.db')
    cursor = conn.cursor()

    cursor.execute(SELECT_ACCOUNT_IDS)

    account_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute(SELECT_ACCOUNT_IDS_PRESENT)
    present_ids = [row[0] for row in cursor.fetchall()]

    conn.commit()
    conn.close()

    return np.setdiff1d(account_ids, np.union1d(present_ids, no_ratings_ids))

def store_player_ratings(ratings):
    conn = sqlite3.connect('./datasets/db/dota.db')
    c = conn.cursor()

    # prepare the query
    if len(ratings) == 0:
        print("No rows to insert!")
        return
    args_str = ", ".join(ratings[0].keys())
    insert_query = 'INSERT INTO %s(%s) VALUES(?, ?, ?, ?, ?);' % (RATINGS_TABLE, args_str)
    ratings_values = [tuple(v for v in r.values()) for r in ratings]

    # execute the query
    c.executemany(insert_query, ratings_values)
    print('We have inserted', c.rowcount, 'records to the table.')

    conn.commit()
    conn.close()


async def get_and_store_player_ratings(account_id):
    params = {"api_key": OPENDOTA_API_KEY}
    try:
        async with aiohttp.ClientSession() as session:
            ratings_uri = f"{PLAYERS_URI}/{account_id}/ratings"

            async with session.get(ratings_uri, params=params) as ratings_response_response:
            # async with session.get(ratings_uri) as ratings_response_response:
                if ratings_response_response.status == 200:
                    ratings = await ratings_response_response.json()
                    if len(ratings) == 0:
                        no_ratings_ids = np.load("./no_ratings_ids.npy")
                        no_ratings_ids = np.append(no_ratings_ids, account_id)
                        np.save("./no_ratings_ids", no_ratings_ids)
                    store_player_ratings(ratings)
                else:
                    logging.warning(ratings_response_response.status)

    except aiohttp.ClientConnectorError as e:
        logging.error('HTTP error', str(e))
        return None


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    account_ids = query_unique_account_ids()
    for account_id in account_ids:
        loop.run_until_complete(get_and_store_player_ratings(account_id))

        # time.sleep(1)
