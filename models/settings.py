class Settings:

    def __init__(self, settings_dict):
        for key, value in settings_dict.items():
            setattr(self, key, value)

    def __repr__(self):
        return str(vars(self))
    
    @classmethod
    def merge(cls, dict1, dict2):
        merged_dict = dict1.copy()
        for key, value in dict2.items():
            if key in merged_dict:
                merged_dict[key].update(value)  # Update the nested dictionary
            else:
                merged_dict[key] = value  # Add the new key-value pair
        return merged_dict
    
    @classmethod
    def typecast(cls, dict1, type_dict):
        return {k: dict1[k] if v is None else v(dict1[k]) for k, v in type_dict.items()}
        
