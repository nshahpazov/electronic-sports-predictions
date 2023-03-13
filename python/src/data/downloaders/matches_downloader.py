"""
Main module for downloading different matches
"""


class MatchesDownloader:
    """
    Extract matches data from the API using only players having visible MMR
    """


import aiohttp
import asyncio
from dotenv import find_dotenv, load_dotenv
import logging
import sqlite3
import pandas as pd
import os
from abc import ABC
from typing import Dict


load_dotenv(find_dotenv())

# env constants
MONGO_DATABASE_URL = os.environ.get("MONGO_DATABASE_URL")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME")
OPENDOTA_API_KEY = os.environ.get("OPEN_DOTA_API_KEY")

SELECT_ACCOUNT_IDS = "SELECT DISTINCT account_id FROM match_player;"
SELECT_ACCOUNT_IDS_PRESENT = "SELECT DISTINCT account_id FROM player_match_rating_v2;"
TEAMS_URI = "https://api.opendota.com/api/teams"
MATCHES_TABLE_V2 = "player_match_rating_v2"


class Downloader(ABC):
    def __init__(self, url: str) -> None:
        self.url = url
        self.params = {"api_key": OPENDOTA_API_KEY}
        pass

    def fetch(self) -> Dict:
        pass


class MatchDownloader(Downloader):
    def __init__(self, url: str) -> None:
        super().__init__(url)

    async def fetch(self, match_id: int):
        async with aiohttp.ClientSession() as session:
            match_url = f"/matches/{match_id}"

            async with session.get(match_url, params=self.params) as match_response:
                if match_response.status == 200:
                    match = await match_response.json()
                    print(match)
                else:
                    logging.warning(match_response.status)


def store_player_ratings(ratings):
    conn = sqlite3.connect("./datasets/db/dota.db")
    c = conn.cursor()

    # prepare the query
    if len(ratings) == 0:
        print("No rows to insert!")
        return
    args_str = ", ".join(ratings[0].keys())
    insert_query = "INSERT INTO %s(%s) VALUES(?, ?, ?, ?, ?);" % (RATINGS_TABLE, args_str)
    ratings_values = [tuple(v for v in r.values()) for r in ratings]

    # execute the query
    c.executemany(insert_query, ratings_values)
    print("We have inserted", c.rowcount, "records to the table.")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    teams_df = pd.read_json("./datasets/raw/teams_21_sep_2021.json")
    team_ids = teams_df.team_id.values()

    for team_id in s:
        loop.run_until_complete(get_matches(team_id))

    #     # time.sleep(1)
