import json

config_file = 'config.json'


class PathFinder:
    def __init__(self):
        self.load()

    def load(self):
        try:
            with open(config_file, 'r') as f:
                allpaths = json.load(f)
        except:
            allpaths = {}

        for k, v in allpaths.items():
            self.__setattr__(k, v)

    def save(self):
        allpaths = {}
        for k, v in self.__dict__.items():
            allpaths[k] = v

        with open(config_file, 'w') as f:
            json.dump(allpaths, f)

        self.load()

