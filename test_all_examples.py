import os

import test_example_repo as run

def test_all_examples():
	rootPath = os.getcwd()
	run.test_example_repo("typescript", "crud-app", rootPath)
	run.test_example_repo("typescript", "getting-started", rootPath)
	run.test_example_repo("typescript", "hello-world", rootPath)
	run.test_example_repo("typescript", "multiversx", rootPath)
	run.test_example_repo("typescript", "quiz-app-prisma", rootPath)
	run.test_example_repo("typescript", "shopping-cart", rootPath)
	run.test_example_repo("typescript", "todo-list-angular", rootPath)
	run.test_example_repo("typescript", "todo-list-flutter", rootPath)
	run.test_example_repo("typescript", "todo-list", rootPath)
	run.test_example_repo("typescript", "webhook", rootPath)


if __name__ == '__main__':
	test_all_examples()