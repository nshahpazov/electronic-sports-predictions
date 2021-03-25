import aiohttp
import asyncio
from pymongo import MongoClient
from multiprocessing import Pool
import os
from dotenv import find_dotenv, load_dotenv
from copy import deepcopy
from progress.bar import Bar
import numpy as np

load_dotenv(find_dotenv())

# constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
OPEN_DOTA_API_KEY = os.environ.get("OPEN_DOTA_API_KEY")
OPENDOTA_ACCOUNTS_URI  = "https://api.opendota.com/api/players/"

MIN_MATCH = 100
NUM_PROCESS = 5


async def get_player(account_id):
    account_uri = OPENDOTA_ACCOUNTS_URI + str(account_id)
    client = MongoClient(MONGO_DATABASE_URL)
    db = client[MONGO_DATABASE_NAME]
    player_collection = db.players_test

    # break execution if the player is present in the database (uncomment later)
    # if player_collection.find_one({'account_id': account_id}) != None:
    #     client.close()
    #     return
    # example
    player = {}
    try:
        async with aiohttp.ClientSession() as session:
            # get general player(account) information
            async with session.get(account_uri + "?api_key=" + OPEN_DOTA_API_KEY) as account_response:
                if account_response.status == 200:
                    account = await account_response.json()
                    player["account_id"] = account_id

                    for k, v in account.items():
                        player[k] = v
                else:
                    print(account_response.status)

            # get wins and losses of that player
            async with session.get(account_uri + "/wl?api_key=" + OPEN_DOTA_API_KEY) as wl_res:
                if account_response.status == 200:
                    win_lose = await wl_res.json()
                    player["win_lose"] = win_lose
                else:
                    print(wl_res.status)

            # get heroes this player has played with
            async with session.get(account_uri + "/heroes?api_key=" + OPEN_DOTA_API_KEY) as heroes_res:
                if heroes_res.status == 200:
                    heroes = await heroes_res.json()
                    player["heroes"] = heroes
                else:
                    print(heroes_res.status)
            # get ratings
            async with session.get(account_uri + "/ratings?api_key=" + OPEN_DOTA_API_KEY) as ratings_res:
                if ratings_res.status == 200:
                    ratings = await ratings_res.json()
                    player["ratings"] = ratings
                else:
                    print(ratings_res.status)

            # get rankings of that player
            async with session.get(account_uri + "/rankings?api_key=" + OPEN_DOTA_API_KEY) as rankings_res:
                if rankings_res.status == 200:
                    heroes_rankings = await rankings_res.json()
                    player["heroes_rankings"] = heroes_rankings
                else:
                    print(rankings_res.status)

            player_collection.insert_one(player)

    except aiohttp.ClientConnectorError as e:
        print('HTTP error', str(e))

if __name__ == "__main__":
    fin = open("./data/info.txt")
    player_list = []
    print("starting ")
    client = MongoClient(MONGO_DATABASE_URL)
    db = client['test']

    player_collection = db.players_test

    for i, line in enumerate(fin.readlines()):
        if i <= 2:
            continue
        if i % 1000 == 0:
            print(i)
        account_id, count = map(int, line.strip().split())
        if player_collection.find_one({'account_id': account_id}) != None:
            continue
        player_list.append(account_id)
        if count < MIN_MATCH:
            break
    print('finish reading')
    client.close()

    # TODO: optimize that to run all the queries
    # https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
    loop = asyncio.get_event_loop()
    [loop.run_until_complete(get_player(id)) for id in player_list]

    # parts = np.array_split(player_list, 10)

    # for part in parts:
    #     bar = Bar('Processing', max=len(part))
    #     p = Pool(NUM_PROCESS)
    #     for _ in p.imap(get_player, part):
    #         bar.next()
    #     bar.finish()
    # fin.close()
