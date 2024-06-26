import requests
import time
import logging
import asyncio
import aiohttp
import os
import pandas as pd
from tqdm import tqdm
from typing import List, Union, Tuple, Dict, Coroutine, Iterator, Optional

from external_data_retrieval.detectors.unique_detector import (
    UniqueJewelDetector,
    UniqueJewelleryDetector,
    UniqueArmourDetector,
    UniqueWeaponDetector,
    UniqueDetector,
)

pd.options.mode.chained_assignment = None  # default='warn'

BASEURL = os.getenv("DOMAIN")
MANUAL_NEXT_CHANGE_ID = os.getenv("MANUAL_NEXT_CHANGE_ID")
NEXT_CHANGE_ID = os.getenv("NEXT_CHANGE_ID")
OATH_ACC_TOKEN_CONTACT_EMAIL = os.getenv("OATH_ACC_TOKEN_CONTACT_EMAIL")

class APIHandler:
    headers = {
        f"User-Agent": "OAuth pathofmodifiers/0.1.0 (contact: {OATH_ACC_TOKEN_CONTACT_EMAIL}) StrictMode"
    }

    if "localhost" not in BASEURL:
        base_pom_api_url = f"https://{BASEURL}"
    else:
        base_pom_api_url = "http://src-backend-1"

    def __init__(
        self,
        url: str,
        auth_token: str,
        *,
        logger_parent: logging.Logger,
        n_wanted_items: int = 100,
        n_unique_wanted_items: int = 5,
        item_detectors: List[Union[UniqueDetector]] = [
            UniqueJewelDetector(),
            UniqueJewelleryDetector(),
            UniqueArmourDetector(),
            UniqueWeaponDetector(),
        ],
    ) -> None:
        """
        Parameters:
            :param url: (str) A string containing POE public stash api url.
            :param auth_token: (str) A string containing OAuth2 auth token.
            :param n_wanted_items: (int) The number of items the program should search for before quitting.
            :param n_unique_wanted_items: (int) The number of different type of items the program should search for before quitin.
            :param item_detectors: (List[ItemDetector]) A list of `ItemDetector` instances.
        """
        self.url = url
        self.auth_token = auth_token
        self.headers["Authorization"] = "Bearer " + auth_token

        self.item_detectors = item_detectors

        self.n_found_items = 0
        self.n_wanted_items = n_wanted_items

        self.n_unique_items_found = 0
        self.n_unique_wanted_items = n_unique_wanted_items

        self.logger = logger_parent.getChild("API_handler")

        self.time_for_last_ratelimit = None

    @property
    def recently_ratelimited(self) -> bool:
        """
        To avoid continously running into the rate limit, we want to track
        if we have recently been rate limited. Currently "recently" refers
        to 180 seconds. If we have been recently ratelimited, you can choose
        to act differently, such as adding artificial delay.
        """
        if self.time_for_last_ratelimit is None:
            return False
        elif time.perf_counter() - self.time_for_last_ratelimit > 180:
            return False
        else:
            return True

    def _json_to_df(self, stashes: List) -> pd.DataFrame:
        df_temp = pd.json_normalize(stashes)
        df_temp = df_temp.explode(["items"])
        df_temp = df_temp.loc[~df_temp["items"].isnull()]
        df_temp.drop("items", axis=1, inplace=True)
        df_temp.rename(columns={"id": "stashId"}, inplace=True)

        df = pd.json_normalize(stashes, record_path=["items"])
        df["stash_index"] = df_temp.index

        df_temp.index = df.index
        df[df_temp.columns.to_list()] = df_temp
        df.rename(columns={"id": "gameItemId"}, inplace=True)

        return df

    def _df_to_json(self, df: pd.DataFrame, stashes: List) -> List:
        """
        DEPRICATED
        """
        wanted_stashes = []
        for stash_index in df["stash_index"].unique():
            wanted_stash = stashes[stash_index]
            wanted_items = df.loc[df["stash_index"] == stash_index]
            wanted_stash["items"] = wanted_items.to_dict()
            wanted_stashes.append(wanted_stash)

        return wanted_stashes

    def _check_stashes(self, stashes: List) -> pd.DataFrame:
        """
        Parameters:
            :param stashes: (list) A list of stash objects
        """
        df_wanted = pd.DataFrame()
        n_new_items = 0
        n_total_unique_items = 0

        df = self._json_to_df(stashes)

        # The stashes are fed to all item detectors, slowly being filtered down
        try:
            for item_detector in self.item_detectors:
                (
                    df_filtered,
                    item_count,
                    n_unique_found_items,
                    df_leftover,
                ) = item_detector.iterate_stashes(df)

                df_wanted = pd.concat((df_wanted, df_filtered))
                n_new_items += item_count
                n_total_unique_items += n_unique_found_items

                df = df_leftover.copy(deep=True)
        except Exception as e:
            self.logger.critical(
                f"While checking stashes (detector: {item_detector}), the exception below occured:"
            )
            self.logger.critical(e)
            raise e

        # Updates progress bars
        self.n_found_items += n_new_items
        self.item_count_pbar.update(n_new_items)

        self.unique_items_count_pbar.update(
            n_total_unique_items
            - self.n_unique_items_found  # Updates with the difference of current unique items found and previously found
        )
        self.n_unique_items_found = n_total_unique_items

        return df_wanted

    def _get_latest_change_id(self) -> str:
        response = requests.get(
            "https://www.pathofexile.com/api/trade/data/change-ids",
            headers={"User-Agent": self.headers["User-Agent"]},
        )
        response.raise_for_status()
        response_json = response.json()
        next_change_id = response_json["psapi"]

        if (
            MANUAL_NEXT_CHANGE_ID
        ):  # For testing purposes, set manual next_change_id
            next_change_id = NEXT_CHANGE_ID

        return next_change_id

    def _initialize_stream(self) -> Tuple[str, List]:
        """
        Makes an initial, synchronous, API call.
        """
        next_change_id = self._get_latest_change_id()

        response = requests.get(
            self.url, headers=self.headers, params={"id": next_change_id}
        )
        if response.status_code >= 300:
            if response.status_code == 429:
                # https://www.pathofexile.com/developer/docs/index#ratelimits
                # Rate limits are dynamic
                headers = response.headers
                retry_after = int(headers["Retry-After"])
                time.sleep(retry_after + 1)
                return self._initialize_stream(next_change_id=next_change_id)

            response.raise_for_status()
        response_json = response.json()

        stashes = response_json["stashes"]
        if stashes:
            next_change_id = response_json["next_change_id"]
            self.iteration_pbar.update()

        return next_change_id, stashes

    async def _start_next_request(
        self, session: aiohttp.ClientSession, next_change_id: str
    ) -> Coroutine:

        async with session.get(self.url, params={"id": next_change_id}) as response:
            if response.status >= 300:
                if response.status == 429:
                    # https://www.pathofexile.com/developer/docs/index#ratelimits
                    # Rate limits are dynamic
                    headers = response.headers
                    retry_after = int(headers["Retry-After"])
                    self.time_for_last_ratelimit = time.perf_counter()
                    await asyncio.sleep(retry_after + 1)
                    return await self._start_next_request(session, next_change_id)

                else:
                    response.raise_for_status()
            response_json = await response.json()
            next_change_id = response_json["next_change_id"]
            stashes = response_json["stashes"]
            return next_change_id, stashes

    async def _follow_stream(self) -> pd.DataFrame:
        """
        Follows the API stream until conditions are met
        """
        next_change_id, new_stashes = self._initialize_stream()
        df = pd.DataFrame()

        iteration = 2
        session = aiohttp.ClientSession(headers=self.headers)
        while (
            self.n_found_items < self.n_wanted_items
            or self.n_unique_items_found < self.n_unique_wanted_items
        ):
            if self.recently_ratelimited:
                # Adds artificial delay if we have recently been ratelimited
                time.sleep(1)

            future = asyncio.ensure_future(
                self._start_next_request(session, next_change_id=next_change_id)
            )

            if not new_stashes:
                time.sleep(
                    120
                )  # Waits 120 seconds before continuing to pursue the stream
            else:
                df_wanted = self._check_stashes(stashes=new_stashes)
                df = pd.concat((df, df_wanted))

                self.iteration_pbar.update()
                iteration += 1

            task_response = await asyncio.gather(future)
            next_change_id, new_stashes = task_response[0]

        df_wanted = self._check_stashes(stashes=new_stashes)
        df = pd.concat((df, df_wanted))

        self.iteration_pbar.update()
        await session.close()

        return df

    def dump_stream(self, track_progress: bool = True) -> Iterator[pd.DataFrame]:
        """
        The method which begins making API calls and fetching data.

        Parameters:
            :track_progress: (bool) Defaults to True. Currently has no function
        """
        # Intializes progressbar context managers
        with (
            tqdm(desc="Iterations", position=0) as self.iteration_pbar,
            tqdm(
                total=self.n_wanted_items,
                desc="    Items found",
                unit="item",
                position=1,
            ) as self.item_count_pbar,
            tqdm(
                total=self.n_unique_wanted_items,
                desc="    Unique items found",
                unit="item",
                position=2,
            ) as self.unique_items_count_pbar,
        ):
            try:
                while True:
                    df = asyncio.run(self._follow_stream())

                    # Ready for next iteration
                    self.n_found_items = 0
                    self.n_unique_items_found = 0
                    yield df.reset_index()
                    self.item_count_pbar.reset()
            except Exception as e:
                raise e
            finally:
                self.iteration_pbar.close()
                self.item_count_pbar.close()
                self.unique_items_count_pbar.close()
