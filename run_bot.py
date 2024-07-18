from bot.bot import Bot
from infrastructure.instrument_collection import InstrumentCollection

if __name__ == "__main__":
    ic = InstrumentCollection()
    ic.LoadInstruments()
    b = Bot()
    b.run()