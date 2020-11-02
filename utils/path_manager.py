import json


project_config_file = 'project_config.json'

class PathFinder:
    def __init__(self):
        self.load()

    def get_file(self):
        with open(project_config_file, 'r') as f:
            project_config = json.load(f)
        current = project_config.get('current', '')
        assert len(current), "Current project not set"

        self.config_file = f'data/{current}/config.json'

    def load(self):
        self.get_file()
        try:
            with open(self.config_file, 'r') as f:
                allpaths = json.load(f)
        except Exception as e:
            allpaths = {}

        for k, v in allpaths.items():
            self.__setattr__(k, v)

    def save(self):
        self.get_file()
        allpaths = {}
        for k, v in self.__dict__.items():
            allpaths[k] = v

        with open(self.config_file, 'w') as f:
            json.dump(allpaths, f)

        self.load()

