from api.oanda_api import OandaApi
from infrastructure.instrument_collection import InstrumentCollection
import time

from models.candle_timing import CandleTiming
from bot.trade_risk_calculator import get_trade_units
import constants.defs as defs

def lm(msg, pair):
    print(msg, pair)

if __name__ == '__main__':
    api = OandaApi()    
    ic = InstrumentCollection()
    ic.LoadInstruments()

    print(get_trade_units(api, ic, "GBP_JPY", defs.BUY, 0.4, 60, lm))
    
