from test_hello import test_hello
from test_todo_list import test_todo_list
from test_unauthenticated import test_unauthenticated
from test_webhooks import test_webhooks
from test_binary_dependency import test_binary_dependency
from test_new_project import test_new_project
from test_create_list_delete import test_create_list_delete
from test_todo_list_ts import test_todo_list_ts
from test_python_sdk import test_python_sdk
from test_swift_sdk import test_swift_sdk
from test_js_sdk import test_js_sdk
from test_ts_sdk import test_ts_sdk
from test_dart import test_dart
from test_typescript_flutter_sdk import test_typescript_flutter_sdk
from test_lambda_handler_errors import test_lambda_handler_errors

import pathlib
import os

if __name__ == '__main__':
    test_path = pathlib.Path(__file__).parent.resolve()
    os.chdir(test_path)
    test_hello()
    os.chdir(test_path)
    test_todo_list()
    os.chdir(test_path)
    test_todo_list_ts()
    os.chdir(test_path)
    test_js_sdk()
    os.chdir(test_path)
    test_ts_sdk()
    os.chdir(test_path)
    test_python_sdk()
    os.chdir(test_path)
    test_swift_sdk()
    os.chdir(test_path)
    test_unauthenticated()
    os.chdir(test_path)
    test_webhooks()
    os.chdir(test_path)
    test_binary_dependency()
    os.chdir(test_path)
    test_new_project()
    os.chdir(test_path)
    test_create_list_delete()
    os.chdir(test_path)
    test_dart()
    os.chdir(test_path)
    test_typescript_flutter_sdk()
    os.chdir(test_path)
    test_lambda_handler_errors()
