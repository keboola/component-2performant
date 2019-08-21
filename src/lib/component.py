import datetime
import logging
import sys
from lib.client import client2Performant
from lib.result import resultWriter
from kbc.env_handler import KBCEnvHandler


USERNAME_KEY = 'username'
PASSWORD_KEY = '#password'
MONTHS_KEY = 'monthsBack'
INCREMENTAL_KEY = 'incremental'

MANDATORY_PARAMS = [USERNAME_KEY, PASSWORD_KEY, MONTHS_KEY]


class Component(KBCEnvHandler):

    def __init__(self):

        KBCEnvHandler.__init__(self, MANDATORY_PARAMS)
        self.validate_config(MANDATORY_PARAMS)

        self.paramUsername = self.cfg_params[USERNAME_KEY]
        self.paramPassword = self.cfg_params[PASSWORD_KEY]
        self.paramMonths = self.cfg_params[MONTHS_KEY]
        self.paramIncremental = self.cfg_params[INCREMENTAL_KEY]

        if isinstance(self.paramMonths, int) is False:

            logging.error("Parameter \"monthsBack\" must be an integer!")
            sys.exit(1)

        elif int(self.paramMonths) <= 0:

            logging.error("Parameter \"monthsBack\" must be a positive integer!")
            sys.exit(1)

        if isinstance(self.paramIncremental, bool) is False:

            logging.error("Parameter \"incremental\" must be a boolean!")
            sys.exit(1)

        self.client = client2Performant(
            username=self.paramUsername, password=self.paramPassword)
        self.writer = resultWriter(self.data_path, incrementalLoad=self.paramIncremental)
        self.varMonthRange = self._generateDateRange(self.paramMonths - 1)

    @staticmethod
    def monthdelta(date, delta):
        m, y = (date.month+delta) % 12, date.year + \
            ((date.month)+delta-1) // 12

        if not m:
            m = 12
        d = min(date.day, [31,
                           29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m-1])
        return date.replace(day=d, month=m, year=y).strftime('%Y%m')

    def _generateDateRange(self, timeDelta):

        now = datetime.datetime.utcnow()
        for i in range(0, timeDelta + 1):

            yield Component.monthdelta(now, -i)

    def run(self):

        for month in self.varMonthRange:

            logging.info("Downloading data for %s..." % month)

            pagedResults = self.client.getPagedCommissions(month)
            flattenedResults = [self.writer.flattenJSON(r) for r in pagedResults]
            self.writer.writerCommissions.writerows(flattenedResults)

            logging.info("Data extraction for %s finished successfully!" % month)
