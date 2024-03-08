import os

import test_example_repo as run


def test_all_examples():
    root_path = os.getcwd()
    examples = [
        {"language": "typescript", "app": "crud-app"},
        {"language": "typescript", "app": "getting-started"},
        {"language": "typescript", "app": "hello-world"},
        {"language": "typescript", "app": "multiversx"},
        {"language": "typescript", "app": "quiz-app-prisma"},
        {"language": "typescript", "app": "shopping-cart"},
        {"language": "typescript", "app": "todo-list"},
        {"language": "typescript", "app": "todo-list-angular"},
        {"language": "typescript", "app": "todo-list-flutter"},
        {"language": "typescript", "app": "webhook"},
        {"language": "javascript", "app": "blockchain"},
        {"language": "javascript", "app": "chatgpt-project"},
        {"language": "javascript", "app": "cron"},
        {"language": "javascript", "app": "getting-started"},
        {"language": "javascript", "app": "hello-world"},
        {"language": "javascript", "app": "html-example"},
        {"language": "javascript", "app": "stripe-js"},
        {"language": "javascript", "app": "todo-list"},
        {"language": "javascript", "app": "todo-list-sql"},
        {"language": "javascript", "app": "todo-list-vue"},
        {"language": "javascript", "app": "webhook"},
        {"language": "kotlin", "app": "getting-started"},
        {"language": "dart", "app": "chat-with-yoda-chatgpt"},
        {"language": "dart", "app": "getting-started"},
        {"language": "dart", "app": "todo-list-react-typescript"},
        {"language": "swift", "app": "todo-list"},
    ]

    for example in examples:
        run.test_example_repo(example["language"], example["app"], root_path)


if __name__ == '__main__':
    test_all_examples()
