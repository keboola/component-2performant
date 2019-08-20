import logging
import json
import os
import sys
from kbc.client_base import HttpClientBase

BASE_URL = 'https://api.2performant.com/'


class client2Performant(HttpClientBase):

    def __init__(self, username, password):

        self.paramUsername = username
        self.paramPassword = password

        _def_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        HttpClientBase.__init__(self, base_url=BASE_URL, default_http_header=_def_headers,
                                status_forcelist=(502, 504), max_retries=10)

        self._login()

    def _login(self):

        _body = {
            "user": {
                "email": self.paramUsername,
                "password": self.paramPassword
            }
        }

        _urlLogin = os.path.join(self.base_url, 'users/sign_in.json')
        _reqLogin = self.post_raw(_urlLogin, data=json.dumps(_body))

        if _reqLogin.status_code == 200:

            self.varAccessToken = _reqLogin.headers['access-token']
            self.varClient = _reqLogin.headers['client']
            self.varUID = _reqLogin.headers['uid']

            logging.info("Credentials obtained.")

        else:

            logging.error("Could not login and obtain an access token.")
            logging.error("Response received: %s - %s." %
                          (_reqLogin.status_code, _reqLogin.reason))

            sys.exit(1)

    def _getCommissions(self, page, dateFilter):

        _headers = {
            "access-token": self.varAccessToken,
            "uid": self.varUID,
            "client": self.varClient
        }

        _params = {
            "page": page,
            "filter[date]": dateFilter
        }

        _urlCommissions = os.path.join(
            self.base_url, 'advertiser/programs/default/commissions')
        _reqCommissions = self.get_raw(
            _urlCommissions, headers=_headers, params=_params)

        if _reqCommissions.status_code == 200:

            return _reqCommissions.json()['commissions']

        else:

            logging.error("Unhandled exception. Received %s - %s." %
                          (_reqCommissions.status_code, _reqCommissions.json()))
            sys.exit(100)

    def getPagedCommissions(self, dateFilter):

        allCommissions = []
        reachedEnd = False
        reqPage = 0

        while not reachedEnd:

            reqPage += 1
            _respCommissions = self._getCommissions(reqPage, dateFilter)

            if len(_respCommissions) == 0:

                reachedEnd = True

            else:

                allCommissions += _respCommissions

        return allCommissions
