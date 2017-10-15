from concurrent import futures
from concurrent.futures import Future
import threading

class Actor(object):
    def __init__(self, parent: 'Actor', executor: futures.Executor = None) -> None:
        self._executor = parent._executor if executor is None else executor
        self._parent = parent
        self._children = []
        self._resp_cond = None
        self._resp = None

    def send(self, message: 'Message', recipient: 'Actor') -> None:
        return recipient.receive(message, self)

    def receive(self, message: 'Message', sender: 'Actor') -> None:
        raise Exception("Abstract method! What the hell are you doing?")

    def ask(self, message: 'Message', recipient: 'Actor') -> 'Future[Message]':
        def _ask():
            return self.send(message, recipient)
        return self._executor.submit(_ask)

    def parent(self) -> 'Actor':
        return self._parent

    def children(self) -> 'List[Actor]':
        return self._children

    def add_child(self, child: 'Actor') -> None:
        self._children.append(child)
