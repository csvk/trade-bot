
from sys import exit
import json
from random import choice
from api.oanda_api import OandaApi
from bot.trade_risk_calculator import get_trade_units

from models.settings import Settings
from models.trade_decision import TradeDecision
from infrastructure.log_wrapper import LogWrapper
from constants import defs


class TradeManager:
    
    def __init__(self, api: OandaApi, logs: LogWrapper):
        self.api = api
        self.logs = logs

        self.load_settings()
        self.get_last_transaction_id()

    def load_settings(self):
        with open("./bot/instr_settings.json", "r") as f:
            instr_settings = json.loads(f.read())

        api_settings = self.get_instrument_settings(instr_settings.keys())
        self.trade_settings = { k: Settings(
             Settings.merge(instr_settings[k], 
                            Settings.typecast(api_settings[k], defs.INSTR_KEYS))) for k in instr_settings.keys()}

    def get_instrument_settings(self, instruments):
        return self.api.get_instrument_settings(instruments)
    
    def get_last_transaction_id(self):
        ok, last_transaction_id = self.api.get_last_transaction_id()

        if not ok:
            self.logs[defs.ERROR_LOG].log_message("CRASH: Init Failed: Unable to get last transaction id")
            exit(1)
        else:
            self.last_transaction_id = last_transaction_id
        return ok

    def process_trades(self):
        self.refresh_state()
        self.balance_on_close()
        self.balance_just_in_case()
        self.fresh_entry()        
    
    def refresh_state(self, init=False):
        ok, changes, state, last_transaction_id = self.api.get_state_changes(self.last_transaction_id)

        if changes is None or state is None or last_transaction_id is None:
            self.log_message(f"ERROR: Error in refreshing state", defs.ERROR_LOG)
            if changes is None:
                self.log_message(f"changes: {changes}", defs.ERROR_LOG)
            if state is None:
                self.log_message(f"state: {state}", defs.ERROR_LOG)
            if last_transaction_id is None:
                self.log_message(f"last_transaction_id: {last_transaction_id}", defs.ERROR_LOG)           

        else:
            self.changes, self.state = changes, state
            if init or last_transaction_id != self.last_transaction_id or 1:
                self.last_transaction_id = last_transaction_id
                self.refresh_instrument_states()
                self.log_instrument_states(init)
    
    def refresh_instrument_states(self):
        self.instrument_states = dict()
        for position in self.state['positions']:
            self.instrument_states[position['instrument']] = dict(
                instrument=position['instrument'],
                long_position=0,
                long_order=0,
                long_total=0,
                short_total=0,
                short_position=0,
                short_order=0
            )

        open_trades = self.api.get_open_trades()
        for trade in open_trades:
            instrument = trade['instrument']
            units = int(trade['currentUnits'])
            if units > 0:
                self.instrument_states[instrument]['long_position'] = \
                    self.instrument_states[instrument]['long_position'] + units
                self.instrument_states[instrument]['long_total'] = \
                    self.instrument_states[instrument]['long_total'] + units
            else:
                self.instrument_states[instrument]['short_position'] = \
                    self.instrument_states[instrument]['short_position'] - units
                self.instrument_states[instrument]['short_total'] = \
                    self.instrument_states[instrument]['short_total'] - units
        
        pending_orders = self.api.get_pending_orders()
        for order in pending_orders:
            instrument = order['instrument']
            units = int(order['units'])
            if units > 0:
                self.instrument_states[instrument]['long_order'] = \
                    self.instrument_states[instrument]['long_order'] + units
                self.instrument_states[instrument]['long_total'] = \
                    self.instrument_states[instrument]['long_total'] + units
            else:
                self.instrument_states[instrument]['short_order'] = \
                    self.instrument_states[instrument]['short_order'] - units
                self.instrument_states[instrument]['short_total'] = \
                    self.instrument_states[instrument]['short_total'] - units

    def log_instrument_states(self, init):
        header = ['instrument', 'long_open', 'long_pending', 'total_long', 'total_short', 'short_open', 'short_pending']
        for instrument in self.trade_settings.keys():
            found = False
            change_types = ['ordersCreated','ordersCancelled', 'ordersFilled', 'ordersTriggered', 'tradesOpened',
                            'tradesReduced', 'tradesClosed']
            for change_type in change_types:
                for change in self.changes[change_type]:
                    if 'instrument' in change and change['instrument'] == instrument:
                        self.logs[instrument].log_message(f"REFRESH: Last transaction id: {self.last_transaction_id}")
                        data = [list(self.instrument_states[instrument].values())]
                        self.logs[instrument].log_table(header, data)    
                        found = True
                    if found:
                        break
                if found:
                    break 

        if init:
            for instrument, state in self.instrument_states.items():
                self.logs[instrument].log_message(f"REFRESH: Last transaction id: {self.last_transaction_id}")
                data = [list(state.values())]
                self.logs[instrument].log_table(header, data)               
    
    # def is_changed(self, instrument):
    #     if  len(self.changes["ordersCreated"]) + len(self.changes["ordersCancelled"]) + \
    #         len(self.changes["ordersFilled"]) + len(self.changes["ordersTriggered"]) + \
    #         len(self.changes["tradesOpened"]) + len(self.changes["tradesReduced"]) + \
    #         len(self.changes["tradesClosed"]) + len(self.changes["positions"]) + \
    #         len(self.changes["transactions"]) == 0:
    #         return False
    #     else:
    #         return True
    
    def fresh_entry(self):
        for instrument in self.trade_settings.keys():
            if self.instrument_states[instrument]['long_position'] \
                + self.instrument_states[instrument]['short_position'] == 0:

                #####################
                # Enter new trade in direction of last profitable trade at capacity
                # Consider trade direction on init or no recent profitable trade
                #####################

                for change in self.changes['tradesClosed']:
                    if 'instrument' in change and change['instrument'] == instrument:
                        units = self.trade_settings[instrument].tradeUnitsPrecision(
                            change['initialUnits']
                        )
                    else:
                        units = self.trade_settings[instrument].tradeUnitsPrecision(
                            choice([defs.BUY, defs.SELL]) * self.trade_settings[instrument]['capacity']
                        )

                







                #####################
                # Cancel pending orders
                #####################

                #####################
                # Create opposite stop order to balance
                #####################      
                pass
    
    def balance_on_close(self):
        for instrument in self.trade_settings.keys():
            ###########################
            # if trade closed on profit
            ###########################

                #####################
                # reduce farthest trade
                #####################

                #####################
                # re-enter in same direction at capacity
                #####################

                #####################
                # Create opposite stop order to balance
                #####################      
                pass
        
    def balance_just_in_case(self):
        for instrument in self.trade_settings.keys():
            ###########################
            # if instrument not balanced
            ###########################

                #####################
                # if within trigger price from last entry
                #####################

                    #####################
                    # Create opposite stop order to balance
                    #####################    

                #####################
                # else
                #####################
                
                    #####################
                    # balance at market
                    #####################
                pass
                

    def check_balanced_state(self):
        pass
        

    def trade_is_open(self, pair, api: OandaApi):

        open_trades = api.get_open_trades()

        for ot in open_trades:
            if ot.instrument == pair:
                return ot

        return None


    def place_trade(self, trade_decision: TradeDecision, api: OandaApi, log_message, log_error, trade_risk):

        ot = self.trade_is_open(trade_decision.pair, api)

        if ot is not None:
            log_message(f"Failed to place trade {trade_decision}, already open: {ot}", trade_decision.pair)
            return None

        trade_units = get_trade_units(api, trade_decision.pair, trade_decision.signal, 
                                trade_decision.loss, trade_risk, log_message)

        trade_id = api.place_trade(
            trade_decision.pair, 
            trade_units,
            trade_decision.signal,
            trade_decision.sl,
            trade_decision.tp
        )

        if trade_id is None:
            log_error(f"ERROR placing {trade_decision}")
            log_message(f"ERROR placing {trade_decision}", trade_decision.pair)
        else:
            log_message(f"placed trade_id:{trade_id} for {trade_decision}", trade_decision.pair)


