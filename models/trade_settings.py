class TradeSettings:

    def __init__(self, ob, pair):
        self.n_ma = ob['n_ma']
        self.n_std = ob['n_std']
        self.maxspread = ob['maxspread']
        self.mingain = ob['mingain']
        self.riskreward = ob['riskreward']

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def settings_to_str(cls, settings):
        ret_str = "Trade Settings:\n"
        for k, v in settings.items():
            ret_str += f"{k}: {v}\n"

        return ret_str