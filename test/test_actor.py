from actor import Actor
from concurrent.futures import ThreadPoolExecutor
import pytest

class PrintActor(Actor):
    def receive(self, message, sender):
        print(message)

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

def test_send(test_executor, capsys):
    a = PrintActor(None, executor=test_executor)
    a.receive("stuff", None)
    out, _ = capsys.readouterr()
    assert out == "stuff\n"

def test_send_actor_to_actor(test_executor, capsys):
    print_actor = PrintActor(None, executor=test_executor)
    pass_along = PassAlongActor(print_actor, None, executor=test_executor)
    pass_along.receive("hello", None)
    out, _ = capsys.readouterr()
    assert out == "hello\n"

def test_ask(test_executor):
    for i in range(10000):
        echo_actor = EchoActor(None, executor=test_executor)
        ask_actor = AskActor(echo_actor, None, executor=test_executor)
        ask_actor.receive("test", None)
        assert ask_actor._message == "test"
