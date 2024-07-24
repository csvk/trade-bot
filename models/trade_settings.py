class TradeSettings:

    def __init__(self, ob, pair):
        self.hedge_pips = ob['hedge_pips']
        self.tp_pips = ob['tp_pips']
        self.capacity = ob['capacity']
        self.keep = ob['keep']

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def settings_to_str(cls, settings):
        ret_str = "Trade Settings:\n"
        for k, v in settings.items():
            ret_str += f"{k}: {v}\n"

        return ret_str