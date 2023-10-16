class Command:
    def __init__(self, name: str):
        self.should_running: bool = False
        self.name: str = name

    def preprocess(self):
        self.should_running = True

    def process(self):
        raise NotImplementedError

    def postprocess(self):
        self.should_running = False
