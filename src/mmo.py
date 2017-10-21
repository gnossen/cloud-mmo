import time
from concurrent.futures import ThreadPoolExecutor
from message import *
from root_actor import RootActor

class timed_loop:
    def __init__(self, fps):
        self._fps = fps

    def __call__(self, f):
        desired_period = 1.0 / self._fps
        frame_duration = 0.0
        start_time = time.time()
        while True:
            frame_start = time.time()
            elapsed_time = frame_start - start_time
            f(elapsed_time, frame_duration)
            frame_duration = time.time() - frame_start
            time.sleep(max(0, desired_period - elapsed_time))

executor = ThreadPoolExecutor(max_workers=4)
root_actor = RootActor(executor)

@timed_loop(60.0)
def main(elapsed_time, frame_duration):
    root_actor.receive(UpdateMessage(elapsed_time, frame_duration), None)
    root_actor.receive(BlitMessage(None), None)

main()
