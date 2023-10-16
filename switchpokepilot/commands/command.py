from switchpokepilot.controller.controller import Controller


class Command:
    def __init__(self, controller: Controller):
        self.is_running = False
        self.controller = controller

    def preprocess(self):
        self.is_running = True

    def process(self):
        raise NotImplementedError

    def postprocess(self):
        self.is_running = False
