import aiohttp
import asyncio
from pymongo import MongoClient
from multiprocessing import Pool
import os
from dotenv import find_dotenv, load_dotenv
import logging
import operator
import numpy as np

load_dotenv(find_dotenv())

# env constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
OPENDOTA_API_KEY = os.environ.get("OPEN_DOTA_API_KEY")

OPENDOTA_ACCOUNTS_URI  = "https://api.opendota.com/api/players/"

# this might change
PLAYER_COLLECTION_NAME = "players_test"

MIN_MATCH = 100

async def crawl_player(account_id, session):
    account_uri = OPENDOTA_ACCOUNTS_URI + str(account_id)
    params = {"api_key": OPENDOTA_API_KEY}

    player = {}
    try:
        async with session.get(account_uri, params=params) as account_response:
            if account_response.status == 200:
                account = await account_response.json()
                player["account_id"] = account_id

                for k, v in account.items():
                    player[k] = v
            else:
                logging.warning(account_response.status)

        # get wins and losses of that player
        async with session.get(account_uri + "/wl", params=params) as wl_res:
            if account_response.status == 200:
                win_lose = await wl_res.json()
                player["win_lose"] = win_lose
            else:
                logging.warning(wl_res.status)

        # get heroes this player has played with
        async with session.get(account_uri + "/heroes", params=params) as heroes_res:
            if heroes_res.status == 200:
                heroes = await heroes_res.json()
                player["heroes"] = heroes
            else:
                logging.warning(heroes_res.status)

        # get ratings
        async with session.get(account_uri + "/ratings", params=params) as ratings_res:
            if ratings_res.status == 200:
                ratings = await ratings_res.json()
                player["ratings"] = ratings
            else:
                logging.warning(ratings_res.status)

        # get rankings of that player
        async with session.get(account_uri + "/rankings", params=params) as rankings_res:
            if rankings_res.status == 200:
                heroes_rankings = await rankings_res.json()
                player["heroes_rankings"] = heroes_rankings
            else:
                logging.warning(rankings_res.status)

        return player

    except aiohttp.ClientConnectorError as e:
        logging.error('HTTP error', str(e))
        return None

def load_players_list(fin):
    player_list = []

    for i, line in enumerate(fin.readlines()):
        if i <= 2:
            continue
        if i % 1000 == 0:
            print(i)
        account_id, count = map(int, line.strip().split())

        player_list.append(account_id)
        if count < MIN_MATCH:
            break
    print('finish reading')

    return player_list

async def crawl_players(ids):
    # open a mongo database connection
    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]
    player_collection = db.players_test
    found_players = player_collection.find({}, {"account_id": 1, "_id": 0})

    # some of the ids from the file may be present in the database
    already_present_ids = [p["account_id"] for p in found_players if "account_id" in p]
    ids_to_crawl = np.setdiff1d(ids, already_present_ids)
    ids_to_crawl = ids_to_crawl[100:200].astype(int).tolist()

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(crawl_player(id, session)) for id in ids_to_crawl]
        responses = await asyncio.gather(*tasks)
        clean_responses = [res for res in responses if res != None]
        player_collection.insert_many(clean_responses)
        client.close()

if __name__ == "__main__":
    fin = open("./data/info.txt")
    player_ids = load_players_list(fin)

    fin.close()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(crawl_players(player_ids))
    loop.run_until_complete(future)
