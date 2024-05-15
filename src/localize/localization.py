from functions import *

class localization:
    def __init__(self, recording):
        self.recording = recording

    def locate(self):
        locations = locate(self.recording).flatten()
        locations = (locations[0], locations[1])
        return locations

localize = localization(load(3, -1))
print(localize.locate())