from api.oanda_api import OandaApi
from infrastructure.instrument_collection import InstrumentCollection

if __name__ == '__main__':
    api = OandaApi()    
    ic = InstrumentCollection()
    # ic.LoadInstruments(api, refresh=True)
    ic.LoadInstruments()
    ic.PrintInstruments()
    
    