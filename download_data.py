from api.oanda_api import OandaApi
from infrastructure.instrument_collection import InstrumentCollection as ic
from infrastructure.collect_data import run_collection

curr_list = ["AUD", "CAD", "JPY", "USD", "EUR", "GBP", "NZD", "CHF"]
# granularity = ["S1", "M1", "M5", "H1", "H4"]
granularity = ["H4"]

start = "2021-01-07T00:00:00Z"
end = "2021-01-31T00:00:00Z"

api = OandaApi()
run_collection(ic, api, curr_list, granularity, start=start, end=end)