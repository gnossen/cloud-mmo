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

class DamageMessage:
    def __init__(self, bounds):
        self.bounds = bounds

class InflictDamageMessage(DamageMessage):
    def to_take_msg(self):
        return TakeDamageMessage(self.bounds)

class TakeDamageMessage(DamageMessage):
    pass
