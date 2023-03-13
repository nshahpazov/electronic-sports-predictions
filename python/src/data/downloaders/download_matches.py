import aiohttp
import asyncio
import logging

# import time
import pandas as pd
import os

OPENDOTA_API_KEY = os.environ.get("OPEN_DOTA_API_KEY")
DOTA_API_BASE_URL = "https://api.opendota.com/api"


async def get_match(match_id):
    params = {"api_key": OPENDOTA_API_KEY}
    try:
        async with aiohttp.ClientSession() as session:
            match_uri = f"{DOTA_API_BASE_URL}/matches/{match_id}"
            async with session.get(match_uri, params=params) as matches_response:
                # async with session.get(ratings_uri) as matches_response:
                if matches_response.status == 200:
                    match = await matches_response.json()
                    print(match)
                else:
                    logging.warning(matches_response.status)

    except aiohttp.ClientConnectorError as e:
        logging.error("HTTP error", str(e))
        return None


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    matches_df = pd.read_csv("./dota2/data/01_raw/professional_match_ids.csv")
    match_ids = matches_df["match_id"].values

    for match_id in match_ids:
        loop.run_until_complete(get_match(match_id))
        # time.sleep(1)
        break
