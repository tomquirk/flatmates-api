"""
Provides linkedin api-related code
"""
import random
import logging
from time import sleep
import json

from flatmates_api.client import Client

logger = logging.getLogger(__name__)


class Flatmates(object):
    """
    Class for accessing Flatmates API.
    """

    def __init__(
        self,
        username=None,
        password=None,
        sessionId=None,
        csrfToken=None,
        flatmatesSessionId=None,
    ):
        self.client = Client()
        if username and password:
            return self.client.authenticate(username, password)
        if sessionId and csrfToken and flatmatesSessionId:
            self.client.authenticate_session(
                _session=sessionId,
                csrf=csrfToken,
                _flatmates_session=flatmatesSessionId,
            )

        self.logger = logger

    def get_new_messages(self):
        res = self.client.session.get(
            f"{self.client.API_BASE_URL}/conversations/new_messages"
        )

        data = res.json()

        return data

    def send_message(self, listing_id, message):
        payload = {
            "listing": "PERSON",
            "listing_id": listing_id,
            "member_id": None,
            "message": message,
        }
        res = self.client.session.post(
            f"{self.client.API_BASE_URL}/conversations/create", data=payload
        )

        return res.status_code == 201

    def _build_query(
        self,
        location=None,  # west-end-4101
        available_from=None,  # 25-10-2019
        min_age=None,
        max_age=None,
        lgtb=False,
        no_kids=False,
        no_pets=False,
        non_smoker=False,
        min_price=-1,
        max_price=-1,
        room_type=None,
    ):
        query = [
            f"available-{available_from}" if available_from else None,
            "lgtb" if lgtb else None,
            "no_kids" if no_kids else None,
            "no_pets" if no_pets else None,
            "non_smoker" if non_smoker else None,
            "room_type" if room_type else None,
            f"min-{min_price}" if min_price else None,
            f"max-{max_price}" if max_price else None,
            f"max-{max_age}yrs" if max_age else None,
            f"max-{min_age}yrs" if min_age else None,
        ]
        location = location + "/" if location else ""
        return f"{location}{'+'.join([i for i in query if i])}"

    def search(
        self,
        location=None,
        available_from=None,
        min_age=None,
        max_age=None,
        lgtb=False,
        no_kids=False,
        no_pets=False,
        non_smoker=False,
        min_price=None,
        max_price=None,
        room_type=None,
        max_depth=-1,
        page=1,
        _listings=[],
    ):
        query = self._build_query(
            location=location,
            available_from=available_from,
            min_age=min_age,
            max_age=max_age,
            lgtb=lgtb,
            no_kids=no_kids,
            no_pets=no_pets,
            non_smoker=non_smoker,
            min_price=min_price,
            max_price=max_price,
            room_type=room_type,
        )
        url = f"{self.client.API_BASE_URL}/people/{query}?page={page}"

        res = self.client.session.get(url)
        res = res.json()
        _listings.extend(res["listings"])

        next_page = res["nextPage"]
        if next_page is None:
            return _listings

        if max_depth > 0 and page == max_depth:
            return _listings
        return self.search(
            location=location,
            available_from=available_from,
            min_age=min_age,
            max_age=max_age,
            lgtb=lgtb,
            no_kids=no_kids,
            no_pets=no_pets,
            non_smoker=non_smoker,
            min_price=min_price,
            max_price=max_price,
            room_type=room_type,
            max_depth=max_depth,
            page=next_page,
            _listings=_listings,
        )

    def get_listing_metadata(self, listing_ids):
        res = self.client.session.post(
            f"{self.client.API_BASE_URL}/listings_metadata.json",
            json={"ids": listing_ids},
            headers={"Content-Type": "application/json;charset=UTF-8"},
        )

        return res.json()["listings"]

