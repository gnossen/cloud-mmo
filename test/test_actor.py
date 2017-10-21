from actor import Actor
from concurrent.futures import ThreadPoolExecutor
import pytest

class PrintActor(Actor):
    def __init__(self, parent, executor=None):
        self._message = None
        super().__init__(parent, executor)

    def receive(self, message, sender):
        self._message = message

class PassAlongActor(Actor):
    def __init__(self, target, parent, executor):
        self._target = target
        super().__init__(parent, executor)

    def receive(self, message, sender):
        self.send(message, self._target)

class EchoActor(Actor):
    def receive(self, message, sender):
        return message

class AskActor(Actor):
    def __init__(self, target, parent, executor):
        self._target = target
        self_message = None
        super().__init__(parent, executor)

    def receive(self, message, sender):
        resp = self.ask(message, self._target)
        self._message = resp.result()

@pytest.fixture(scope="module")
def test_executor():
    return ThreadPoolExecutor(max_workers=4)

def test_receive(test_executor, capsys):
    a = PrintActor(None, executor=test_executor)
    a.receive("stuff", None)
    assert a._message == "stuff"

def test_send(test_executor, capsys):
    print_actor = PrintActor(None, executor=test_executor)
    pass_along = PassAlongActor(print_actor, None, executor=test_executor)
    pass_along.receive("hello", None)
    assert print_actor._message == "hello"

def test_ask(test_executor):
    for i in range(10000):
        echo_actor = EchoActor(None, executor=test_executor)
        ask_actor = AskActor(echo_actor, None, executor=test_executor)
        ask_actor.receive("test", None)
        assert ask_actor._message == "test"

class PropagationMessage:
    pass

class ParentActor(Actor):
    def __init__(self, child_cls, executor):
        super().__init__(None, executor)
        self._child_actor = child_cls(self)
        self._message = None

    def receive(self, message, sender):
        if isinstance(message, PropagationMessage):
            self.send(message, self._child_actor)
        else:
            self._message = message

def test_add_child(test_executor):
    parent = ParentActor(PrintActor, test_executor)
    assert len(parent._children) == 1
    assert isinstance(parent._children[0], PrintActor)

class HoistActor(Actor):
    def receive(self, msg, sender):
        if isinstance(msg, PropagationMessage):
            self.hoist("Got it!")

def test_hoist_message(test_executor):
    parent = ParentActor(HoistActor, test_executor)
    parent.receive(PropagationMessage(), None)
    assert parent._message == "Got it!"
