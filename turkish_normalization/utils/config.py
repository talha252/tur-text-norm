from collections import UserDict

class Config(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in kwargs.items():
            if isinstance(v, dict):
                self[k] = Config(**v)
        
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        self[name] = value
