from concurrent import futures
from concurrent.futures import Future
import threading

class Actor(object):
    def __init__(self, parent: 'Actor', executor: futures.Executor = None) -> None:
        self._executor = parent._executor if executor is None else executor
        self._parent = parent
        if parent is not None:
            parent.add_child(self)
        self._children = []
        self._resp_cond = None
        self._resp = None

    def send(self, message: 'Message', recipient: 'Actor') -> None:
        return recipient.receive(message, self)

    def hoist(self, message: 'Message') -> None:
        if self._parent is None:
            msg = "{} has no parent. Cannot hoist message '{}'.".format(self, message)
            raise RuntimeError(msg)
        return self._parent.receive(message, self)

    def receive(self, message: 'Message', sender: 'Actor') -> 'Any':
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

    def await(self, fut: 'Future'):
        return self._executor.submit(fut)
