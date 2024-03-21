import requests
import logging
import os
import pandas as pd
from typing import Iterator, Optional
from copy import deepcopy

from app.database.modifier_data_deposit.processing_modules import add_regex
from app.database.modifier_data_deposit.utils import remove_empty_fields

logging.basicConfig(
    filename="history.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)-8s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
TESTING = True
BASEURL = "http://localhost"  # TODO update when on virtual machine
CASCADING_UPDATE = False


class DataDepositer:
    def __init__(self) -> None:
        self.new_data_location = "new_data"
        self.url = BASEURL + "/api/api_v1/modifier/"
        self.update_disabled = not CASCADING_UPDATE

        self.logger = logging.getLogger(__name__)

    def _load_new_data(self) -> Iterator[pd.DataFrame]:
        for filename in os.listdir(self.new_data_location):
            filepath = os.path.join(self.new_data_location, filename)

            self.logger.info(f"Loading new data from '{filename}'.")
            df = pd.read_csv(filepath, dtype=str, comment="#")
            self.logger.info("Successfully loaded new data.")
            self.logger.info("Recording attached comments:")
            with open(filepath) as infile:
                for line in infile:
                    if "#" == line[0]:
                        self.logger.info(line.rstrip())
                    else:
                        self.logger.info("End of attached comments.")
                        break

            yield df

    def _get_current_modifiers(self) -> Optional[pd.DataFrame]:
        self.logger.info("Retrieving previously deposited data.")
        df = pd.read_json(self.url, dtype=str)
        if df.empty:
            self.logger.info("Found no previously deposited data.")
            return None
        else:
            self.logger.info("Successfully retrieved previously deposited data.")
            return df

    def _update_duplicates(
        self, duplicate_df: pd.DataFrame, current_modifiers_df: pd.DataFrame
    ) -> None:
        if self.update_disabled:
            return None
        self.logger.info("Checking if duplicates contain updated information.")

        current_duplicate_modifiers = current_modifiers_df.loc[
            current_modifiers_df["effect"].isin(duplicate_df["effect"])
        ]
        current_duplicate_modifiers.sort_values(by=["effect", "position"], inplace=True)
        duplicate_df.sort_values(by=["effect", "position"], inplace=True)

        update_url = self.url + "{}?position={}"

        for (_, row_cur), (_, row_new) in zip(
            current_duplicate_modifiers.iterrows(), duplicate_df.iterrows()
        ):
            if not pd.isna(row_new["static"]):
                continue

            if not pd.isna(row_new["textRolls"]):
                if row_cur["textRolls"] != row_new["textRolls"]:
                    self.logger.info("Found a modifier with new 'textRolls'.")
                    row_new = row_new.fillna("")  # requests can not handle na
                    data = row_new.to_dict()
                    data = remove_empty_fields([data])[0]
                    data["modifierId"] = row_cur["modifierId"]
                    data["position"] = row_cur["position"]
                    response = requests.put(
                        update_url.format(row_cur["modifierId"], row_cur["position"]),
                        json=data,
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                        },
                    )
                    response.raise_for_status()
            else:
                min_roll = row_cur["minRoll"]
                max_roll = row_cur["maxRoll"]

                new_min_roll = row_new["minRoll"]
                new_max_roll = row_new["maxRoll"]

                if float(min_roll) > float(new_min_roll):
                    self.logger.info("Found a modifier with a lower 'minRoll'.")
                else:
                    new_min_roll = min_roll

                if float(max_roll) < float(new_max_roll):
                    self.logger.info("Found a modifier with a higher 'maxRoll'.")
                else:
                    new_max_roll = max_roll

                row_new["minRoll"] = float(new_min_roll)
                row_new["maxRoll"] = float(new_max_roll)
                if min_roll != new_min_roll or max_roll != new_max_roll:
                    self.logger.info(
                        "Updating modifier to bring numerical roll range up-to-date."
                    )
                    row_new = row_new.fillna("")  # requests can not handle na
                    data = row_new.to_dict()
                    data = remove_empty_fields([data])[0]
                    data["modifierId"] = row_cur["modifierId"]
                    data["position"] = row_cur["position"]
                    response = requests.put(
                        update_url.format(row_cur["modifierId"], row_cur["position"]),
                        json=data,
                        headers={
                            "accept": "application/json",
                            "Content-Type": "application/json",
                        },
                    )
                    response.raise_for_status()

    def _remove_duplicates(self, new_modifiers_df: pd.DataFrame) -> pd.DataFrame:
        current_modifiers_df = self._get_current_modifiers()

        new_modifiers_df.drop_duplicates(inplace=True)

        if current_modifiers_df is None:
            self.logger.info("Skipping duplicate removing due to no previous data")
            return new_modifiers_df

        self.logger.info("Removing duplicate modifiers")
        duplicate_mask = new_modifiers_df["effect"].isin(current_modifiers_df["effect"])

        duplicate_df = new_modifiers_df.loc[duplicate_mask]
        self._update_duplicates(duplicate_df, current_modifiers_df)
        non_duplicate_df = new_modifiers_df.loc[~duplicate_mask]

        return non_duplicate_df

    def _process_new_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = add_regex(df, logger=self.logger)
        df = self._remove_duplicates(df)
        return df

    def _insert_data(self, df: pd.DataFrame) -> None:
        df = df.fillna("")  # requests can not handle na
        df_json = df.to_dict(
            "records"
        )  # Converts to a list of dicts, where each dict is a row
        df_json = remove_empty_fields(df_json)  # Removes empty fields element-wise
        self.logger.info("Inserting data into database.")
        response = requests.post(
            self.url,
            json=df_json,
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        response.raise_for_status()

        self.logger.info("Successfully inserted data into database.")

    def _delete_processed_data(self):
        for filename in os.listdir(self.new_data_location):
            filepath = os.path.join(self.new_data_location, filename)
            self.logger.info(f"Deleting '{filename}'")
            if TESTING:
                os.rename(filepath, filepath.replace("new_data", "deposited_data"))
            else:
                os.remove(filepath)
            self.logger.info(f"Deleted '{filename}'")

    def deposit_data(self) -> None:
        for df in self._load_new_data():
            df = self._process_new_data(df)
            self._insert_data(df)

        self._delete_processed_data()


def main():
    test = DataDepositer()
    test.deposit_data()
    return 0


main()