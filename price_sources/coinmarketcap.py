import requests
import time
from datetime import datetime, tzinfo, timedelta
from dateutil import parser
from string import Template

import json

from beancount.core.number import D
from beancount.prices import source
from beancount.utils.date_utils import parse_date_liberally

ZERO = timedelta(0)
BASE_URL_TEMPLATE_WITHOUT_TIME = Template("https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD&slug=$ticker")
BASE_URL_TEMPLATE_WITH_TIME = Template("https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD&slug=$ticker&time_end=$time_end&time_start=$time_start")
CURRENCY = "USD"
TIME_DELAY = 15

class UTCtzinfo(tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTCtzinfo()

class CoinmarketcapError(ValueError):
    "An error from the Coinmarketcap API."

class Source(source.Source):
    def _get_price_for_date(self, ticker, date=None):
        time.sleep(TIME_DELAY)

        if date == None:
            url = BASE_URL_TEMPLATE_WITHOUT_TIME.substitute(ticker=ticker)
        else:
            # Somehow it expects a 3 day timespan in the query
            time_start = int((date - timedelta(days=1)).timestamp())
            time_end = int((date + timedelta(days=2)).timestamp())
            url = BASE_URL_TEMPLATE_WITH_TIME.substitute(time_start=time_start, time_end=time_end, ticker=ticker)


        try:
            content = requests.get(url).content
            parsed_content = json.loads(content)            
            quotes = parsed_content['data']['quotes']

            if date == None:
                # If no date, pick the latest
                quote = max(quotes, key = lambda x: parser.isoparse(x['time_open']))
            else:
                quote = list(filter(lambda x: parser.isoparse(x['time_open']) == date, quotes))
                assert len(quote) == 1
                quote = quote[0]

            date = parser.isoparse(quote['quote']['USD']['timestamp'])
            price = D(quote['quote']['USD']['close'])

            return source.SourcePrice(price, date, CURRENCY)
        except KeyError as e:
            raise CoinmarketcapError("Exception {}, Invalid response from Coinmarketcap: {}".format(e, repr(content)))
        except AttributeError as e:
            raise CoinmarketcapError("Exception {}, Invalid response from Coinmarketcap: {}".format(e, repr(content)))

    def get_latest_price(self, ticker):
        return self._get_price_for_date(ticker, None)

    def get_historical_price(self, ticker, time):
        # Convert to UTC
        time = datetime(time.year, time.month, time.day, tzinfo=utc)
        return self._get_price_for_date(ticker, time)