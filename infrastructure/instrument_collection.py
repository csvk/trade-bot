import json
from models.instrument import Instrument
from api.oanda_api import OandaApi

class InstrumentCollection:
    PATH = "./data/"
    FILENAME = "instruments.json"
    API_KEYS = ['name', 'type', 'displayName', 'pipLocation', 'displayPrecision', 'tradeUnitsPrecision', 
                'minimumTradeSize', 'maximumTrailingStopDistance', 'minimumTrailingStopDistance',
                'maximumPositionSize', 'maximumOrderUnits', 'marginRate', 'guaranteedStopLossOrderMode']

    def __init__(self):
        self.instruments_dict = {}

    def DownloadInstruments(self, api: OandaApi):
        attempts = 0

        while attempts < 3:

            instruments = api.get_account_instruments()

            if instruments is not None:
                break

            attempts += 1

        if instruments is not None and len(instruments) != 0:
            self.CreateFile(instruments)
        else:
            raise 'Instruments download error'
        
    def LoadInstruments(self, api: OandaApi=None, refresh=False):
        if refresh:
            assert type(api) == OandaApi, 'Not valid OandaApi object'
            self.DownloadInstruments(api)

        self.instruments_dict = {}
        fileName = f"{self.PATH}/{self.FILENAME}"
        with open(fileName, "r") as f:
            data = json.loads(f.read())
            for k, v in data.items():
                self.instruments_dict[k] = Instrument.FromApiObject(v)

    def CreateFile(self, data):
        if data is None:
            print("Instrument file creation failed")
            return
        
        instruments_dict = {}
        for i in data:
            key = i['name']
            instruments_dict[key] = { k: i[k] for k in self.API_KEYS }

        fileName = f"{self.PATH}/{self.FILENAME}"
        with open(fileName, "w") as f:
            f.write(json.dumps(instruments_dict, indent=2))


    def PrintInstruments(self):
        [print(k,v) for k,v in self.instruments_dict.items()]
        print(len(self.instruments_dict.keys()), "instruments")

# instrumentCollection = InstrumentCollection()
