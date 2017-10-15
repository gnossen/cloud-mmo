from actor import Actor
from concurrent.futures import ThreadPoolExecutor
import pytest

class EchoActor(Actor):
    def receive(self, message, sender):
        print(message)

@pytest.fixture(scope="module")
def test_executor():
    return ThreadPoolExecutor(max_workers=4)

def test_send(test_executor, capsys):
    a = EchoActor(None, executor=test_executor)
    a.receive("stuff", None)
    out, err = capsys.readouterr()
    assert out == "stuff\n"
