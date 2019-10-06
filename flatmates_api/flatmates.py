"""
Provides linkedin api-related code
"""
import random
import logging
from time import sleep
import json
from bs4 import BeautifulSoup

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

    def search(self, query, max_depth=-1, _listings=[]):
        res = self.client.session.post(
            f"{self.client.API_BASE_URL}/search.json",
            json={"search": query},
            headers={"Content-Type": "application/json;charset=UTF-8"},
        )
        listing_results = res.json()
        _listings.extend(listing_results["listings"])

        next_page = listing_results["nextPage"]
        if next_page is None:
            return _listings

        query["page"] = next_page
        return self.search(query, max_depth, _listings)

    def get_listing_metadata(self, listing_ids):
        res = self.client.session.post(
            f"{self.client.API_BASE_URL}/listings_metadata.json",
            json={"ids": listing_ids},
            headers={"Content-Type": "application/json;charset=UTF-8"},
        )

        return res.json()["listings"]

