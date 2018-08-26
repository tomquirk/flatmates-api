import requests
import pickle
import logging

import flatmates_api.settings as settings

logger = logging.getLogger(__name__)


class Client(object):
    """
    Class to act as a client for the Flatmates API.
    """

    # Settings for general Linkedin API calls
    API_BASE_URL = "https://flatmates.com.au"
    REQUEST_HEADERS = {
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/66.0.3359.181 Safari/537.36",
            ]
        ),
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://flatmates.com.au",
        "Referer": "https://flatmates.com.au"
    }

    def __init__(self, debug=False):
        self.session = requests.Session()
        self.session.headers.update(Client.REQUEST_HEADERS)

        self.logger = logger
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

    def _set_session_cookies(self, cookiejar):
        """
        Set cookies of the current session and save them to a file.
        """
        self.session.cookies = cookiejar
        with open(settings.COOKIE_FILE_PATH, "wb") as f:
            pickle.dump(cookiejar, f)

    def authenticate(self, username, password):
        """
        Authenticate with Flatmates.

        Return a session object that is authenticated.
        """

        self.session.headers.update({
            'X-CSRF-Token': 'yFNJ1f9LFhZAzxuIZvqIKL8gJ6Vg0eZkKJBwkTbBv8y1TJcJhrQfZAv+cIm1ydHSRFjlV8SnKqHU4HPdjZD+1Q==',
            # 'X-NewRelic-ID': 'VQUHUFdAAAQHUVNVBwQ='
        })
        self.session.cookies.set('_session', 'ImR1eFBKQUFWOW9TQUNZNXJ3SkJCRkNHMSI%3D--e39afde46a5c362a7b44735f6628156dc0d6f037')
        self.session.cookies.set('_flatmates_session', '1dea9e80af860956d88a763d18237127')
        # self.session.cookies.set('mid', '7646306593737134223')