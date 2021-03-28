import aiohttp
import asyncio
from pymongo import MongoClient
from multiprocessing import Pool
import os
from dotenv import find_dotenv, load_dotenv
import logging
import operator
import numpy as np
import sqlite3
import json

load_dotenv(find_dotenv())

# env constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
OPENDOTA_API_KEY = os.environ.get("OPEN_DOTA_API_KEY")

DISTRIBUTIONS_URI  = "https://api.opendota.com/api/distributions"

def save_distribution(table, mmr_distribution):
    conn = sqlite3.connect('./datasets/db/dota.db')
    c = conn.cursor()

    args_str = ", ".join(mmr_distribution[0].keys())
    insert_query = 'INSERT INTO %s(%s) VALUES(?, ?, ?, ?);' % (table, args_str)

    c.executemany(insert_query, [tuple(d[k] for k in d.keys()) for d in mmr_distribution])
    print('We have inserted', c.rowcount, 'records to the table.')

    conn.commit()
    conn.close()

async def get_and_store_distributions():
    params = {"api_key": OPENDOTA_API_KEY}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(DISTRIBUTIONS_URI, params=params) as distribution_response:
                if distribution_response.status == 200:
                    distribution = await distribution_response.json()

                    save_distribution("mmr_distribution", distribution["mmr"]["rows"])
                    save_distribution("rank_distribution", distribution["ranks"]["rows"])
                else:
                    logging.warning(account_response.status)

        return mmr_distribution

    except aiohttp.ClientConnectorError as e:
        logging.error('HTTP error', str(e))
        return None


if __name__ == "__main__":

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(get_and_store_distributions())

    # do it from the local file so that the same data as in the paper is used
    mmr_distr_file = open('datasets/external/mmr_distribution.json')
    mmr_distribution = json.load(mmr_distr_file)

    save_distribution("mmr_distribution", mmr_distribution)
