SELL = -1
BUY = 1
NONE = 0

ERROR_LOG = "error"
MAIN_LOG = "main"

# INSTR_KEYS = ['type', 'displayName', 'pipLocation', 'displayPrecision', 'tradeUnitsPrecision',
#               'minimumTradeSize', 'maximumTrailingStopDistance', 'minimumTrailingStopDistance',
#               'maximumPositionSize', 'maximumOrderUnits', 'marginRate', 'guaranteedStopLossOrderMode']

INSTR_KEYS = dict(
        type=None,
        displayName=None,
        pipLocation=None,
        displayPrecision=None,
        tradeUnitsPrecision=None,
        minimumTradeSize=float,
        maximumTrailingStopDistance=float,
        minimumTrailingStopDistance=float,
        maximumPositionSize=float,
        maximumOrderUnits=float,
        marginRate=float
    
)