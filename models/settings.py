class Settings:

    def __init__(self, settings_dict):
        for key, value in settings_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        return str(vars(self))