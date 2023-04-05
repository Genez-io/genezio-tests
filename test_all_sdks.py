from test_js_sdk import test_js_sdk
from test_ts_sdk import test_ts_sdk
from test_swift_sdk import test_swift_sdk
from test_python_sdk import test_python_sdk
from test_dart_sdk import test_dart_sdk

import pathlib
import os

if __name__ == '__main__':
    test_path = pathlib.Path(__file__).parent.resolve()
    os.chdir(test_path)
    test_js_sdk()
    os.chdir(test_path)
    test_ts_sdk()
    os.chdir(test_path)
    test_swift_sdk()
    os.chdir(test_path)
    test_python_sdk()
    os.chdir(test_path)
    test_dart_sdk()
