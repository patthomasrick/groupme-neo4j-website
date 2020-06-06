# Patrick Thomas

import requests
import json

GROUPME_API_BASE_URL = "https://api.groupme.com/v3"


class GroupMe:
    def __init__(self, api_token: str):
        self.__api_token = api_token

    def get_group(self) -> int:
        return self.__group_id

    def set_group(self, group_id):
        self.__group_id = int(group_id)

    def get_groups_index(self) -> list:
        url = f"{GROUPME_API_BASE_URL}/groups"
        page = 1
        groups = []

        while True:
            get = requests.get(
                url=url, params={"token": self.__api_token, "page": page},
            )
            if get.status_code != 200:
                break
            response = json.loads(get.text)
            if response["response"] == []:
                break
            groups.extend(response["response"])
            page += 1
        return groups

    def get_latest_message(self):
        get = requests.get(
            url=f"{GROUPME_API_BASE_URL}/groups/{self.__group_id}/messages",
            params={"token": self.__api_token, "limit": 1},
        )
        if get.status_code == 200:
            response = json.loads(get.text)
            return response["response"]["messages"][0]
        else:
            return None

    def get_messages(self, limit: int = 100, before_id: int = None):
        params = {}
        if before_id is None:
            params = {"token": self.__api_token, "limit": limit}
        else:
            params = {"token": self.__api_token, "limit": limit, "before_id": before_id}

        get = requests.get(
            url=f"{GROUPME_API_BASE_URL}/groups/{self.__group_id}/messages",
            params=params,
        )
        if get.status_code == 200:
            response = json.loads(get.text)
            return response["response"]["messages"]
        else:
            return None
