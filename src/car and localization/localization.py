import functions

class localization:
    def __init__(self, recording):
        self.recording = recording

    def locate(self, recording):
        locations = functions.locate(self.recording).flatten()
        locations = (locations[0], locations[1])
        return locations