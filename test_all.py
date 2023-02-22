from test_hello import test_hello
from test_todo_list import test_todo_list
from test_unauthenticated import test_unauthenticated
from test_webhooks import test_webhooks
import pathlib
import os

if __name__ == '__main__':
    test_path = pathlib.Path(__file__).parent.resolve()
    os.chdir(test_path)
    test_hello()
    os.chdir(test_path)
    test_todo_list()
    os.chdir(test_path)
    test_unauthenticated()
    os.chdir(test_path)
    test_webhooks()