from test_dart_to_python import test_dart_to_python
from test_dart_typescript_sdk import test_dart_typescript_sdk
from test_frontend import test_frontend
from test_hello import test_hello
from test_todo_list import test_todo_list
from test_ts_to_python import test_ts_to_python_sdk
from test_unauthenticated import test_unauthenticated
from test_webhooks import test_webhooks
from test_binary_dependency import test_binary_dependency
from test_genezio_misc_cmds import test_genezio_misc_cmds
from test_create_list_delete import test_create_list_delete
from test_todo_list_ts import test_todo_list_ts
from test_python_sdk import test_python_sdk
from test_swift_sdk import test_swift_sdk
from test_js_sdk import test_js_sdk
from test_ts_sdk import test_ts_sdk
from test_dart import test_dart
from test_typescript_flutter_sdk import test_typescript_flutter_sdk
from test_lambda_handler_errors import test_lambda_handler_errors
from test_runtime_binary_dependency import test_runtime_linux_binary_dependency
from test_runtime_cron import test_runtime_linux_cron
from test_runtime_hello import test_runtime_linux_hello
from test_runtime_todo_list import test_runtime_linux_todo_list
from test_runtime_webhooks import test_runtime_linux_webhooks

import pathlib
import os

if __name__ == '__main__':
	test_path = pathlib.Path(__file__).parent.resolve()
	tests_to_run = [
		# test_webhooks,
		# test_python_sdk,
		# test_binary_dependency,# !!! nu merge
		# test_genezio_misc_cmds,
		# test_create_list_delete,
		# test_swift_sdk,
		# test_todo_list_ts,
		# test_lambda_handler_errors, # !!! nu merge
		# test_dart_typescript_sdk,
		# test_ts_to_python_sdk, # !!! nu creaza bine sdkul
		# test_dart,
		# test_todo_list,# !!! nu merge acceasi eroare ca la lambda
		# test_dart_to_python,
		# test_frontend,
		# test_typescript_flutter_sdk,
		# test_ts_sdk,
		# test_unauthenticated, !!! nu merge
		# test_js_sdk,
		# test_hello, # !!! la fel ca la lambda
		test_runtime_linux_binary_dependency,
		test_runtime_linux_hello,
		test_runtime_linux_todo_list,
		test_runtime_linux_webhooks,
		test_runtime_linux_cron
	]

	# Run all tests
	os.chdir(test_path)
	for test in tests_to_run:
		test()
		os.chdir(test_path)

	print("Test passed!")
