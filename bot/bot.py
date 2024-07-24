import json
import time
from bot.candle_manager import CandleManager
from bot.technicals_manager import get_trade_decision
from bot.trade_manager import TradeManager

from models.settings import Settings
from infrastructure.log_wrapper import LogWrapper
from api.oanda_api import OandaApi
from constants import defs



class Bot:

    def __init__(self):
        self.load_settings()
        self.setup_main_logs()

        self.api = OandaApi()
        self.setup_trade_manager()

    def load_settings(self):
        with open("./bot/bot_settings.json", "r") as f:
            data = json.loads(f.read())
            self.settings = Settings(data)

    def setup_main_logs(self):
        self.logs = {}
        self.logs[defs.MAIN_LOG] = LogWrapper(defs.MAIN_LOG)
        self.logs[defs.MAIN_LOG].log_message(f"Bot started with {self.settings}")
        self.logs[defs.ERROR_LOG] = LogWrapper(defs.ERROR_LOG)
        self.logs[defs.ERROR_LOG].log_message("Bot started")

    # def log_message(self, msg, key):
    #     self.logs[key].logger.debug(msg)

    # def log_table(self, table, key):
    #     self.logs[key].logger.debug(table)
        
    # def log_to_main(self, msg):
    #     self.log_message(msg, defs.MAIN_LOG)

    # def log_to_error(self, msg):
    #     self.log_message(msg, defs.ERROR_LOG)

    def setup_trade_manager(self):
        self.manager = TradeManager(self.api, self.logs)

        # Set up instrument logs
        for k in self.manager.trade_settings.keys():
            self.logs[defs.MAIN_LOG].log_message(f"{k}: {self.manager.trade_settings[k]}")
            self.logs[k] = LogWrapper(k)
            self.logs[k].log_message(f"{k}: {self.manager.trade_settings[k]}")  

    def run(self):
        while True:
            DEBUG = True
            if DEBUG:
                self.manager.refresh_state()
            else:
                try:
                    self.manager.refresh_state()
                except Exception as error:
                    self.logs[defs.ERROR_LOG].log_message(f"CRASH: {error}")
                    break
            time.sleep(self.settings.sleep)
    

