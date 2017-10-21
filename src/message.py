class UpdateMessage:
    def __init__(self, elapsed_time, frame_duration):
        self.elapsed_time = elapsed_time
        self.frame_duration = frame_duration

class BlitMessage:
    def __init__(self, camera):
        self.camera = camera

class KeyEventMessage:
    def __init__(self, event):
        self.event = event
