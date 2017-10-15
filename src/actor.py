from concurrent import futures
from concurrent.futures import Future
import asyncio

class Actor(object):
    def __init__(self, parent: 'Actor', executor: futures.Executor = None) -> None:
        self._executor = parent._executor if executor is None else executor
        self._parent = parent
        self._children = []
        self._resp_event = None
        self._resp = None

    def send(self, message: 'Message', recipient: 'Actor') -> None:
        recipient.receive(message, self)

    def respond(self, message: 'Message', recipient: 'Actor') -> None:
        recipient.__receive_response(message, self)

    def __receive_response(self, message: 'Message', responder: 'Actor') -> None:
        assert self._resp_event is not None
        self._resp = message
        self._resp_event.set()

    def receive(self, message: 'Message', sender: 'Actor') -> None:
        raise Exception("Abstract method! What the hell are you doing?")

    def ask(self, message: 'Message', recipient: 'Actor') -> 'Future[Message]':
        def _ask():
            assert self._resp_event is None
            self._resp_event = asyncio.Event()
            self.send(message, recipient)
            self._resp_event.wait()
            resp = self._resp
            self._resp = None
            return resp
        return self._executor.submit(_ask)

    def parent(self) -> 'Actor':
        return self._parent

    def children(self) -> 'List[Actor]':
        return self._children

    def add_child(self, child: 'Actor') -> None:
        self._children.append(child)
