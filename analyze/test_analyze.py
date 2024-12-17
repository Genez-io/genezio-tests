
import argparse
import os
import subprocess
import tempfile
from git import Repo
import yaml
import tempfile
import shutil
import tempfile
import json
from difflib import unified_diff

# To add a new test case, add a new dictionary to the `repositories` list with the following keys:
# - url: The URL of the repository to clone
# - test_name: A unique name for the test case
# - expected_stdout: A list of expected JSON strings that should be printed to stdout by `genezio analyze`

# Note: Create an expected configuration file for each test case in the `expected_configuration_files` directory.
# The name of the file should be the same as the `test_name` with a `.yaml` extension.
# In each yaml file, the `name` field is ignored during comparison.

# List of repository URLs
repositories = [
    {
        "url": "https://github.com/andreia-oca/genezio-analyze",
        "test_name": "genezio_analyze",
        "expected_stdout": ['{"backend":[{"component":"serverless-http"}]}'],
    },
    {
        "url": "https://github.com/andreia-oca/genezio-analyze-express",
        "test_name": "genezio_analyze_express",
        "expected_stdout": ['{"backend":[{"component":"express"}]}'],
    },
    {
        "url": "https://github.com/andreia-oca/genezio-analyze-fastify",
        "test_name": "genezio_analyze_fastify",
        "expected_stdout": ['{"backend":[{"component":"fastify"}]}'],
    },
    {
        "url": "https://github.com/Genez-io/flask-getting-started",
        "test_name": "genezio_analyze_flask",
        "expected_stdout": ['{"backend":[{"component":"flask"}]}'],
    },
    {
        "url": "https://github.com/Genez-io/fastapi-getting-started",
        "test_name": "genezio_analyze_fastapi",
        "expected_stdout": ['{"backend":[{"component":"fastapi"}]}'],
    },
    {
        "url": "https://github.com/Genez-io/django-getting-started",
        "test_name": "genezio_analyze_django",
        "expected_stdout": ['{"backend":[{"component":"django"}]}'],
    },
    # Does not work - faulty entryfile because it's typescript
    # {
    #     "url": "https://github.com/andreia-oca/genezio-analyze-fullstack",
    #     "test_name": "genezio_analyze_fullstack",
    #     "expected_stdout": ['{"backend":[{"component":"serverless-http" ,"environment":[{"key": "OPENAI_API_KEY", "defaultValue": "your-key", "genezioProvisioned": "false"}] }],"frontend":[{"component":"vite"}], "services":[{"databases": ["mongo"]}] }'],
    # },
    {
        "url": "https://github.com/andreia-oca/genezio-analyze-nextjs",
        "test_name": "genezio_analyze_nextjs",
        "expected_stdout": ['{"ssr":[{"component":"next", "environment": [{"key": "OPENAI_API_KEY", "defaultValue": "****", "genezioProvisioned": false}, {"key": "AUTH_SECRET", "defaultValue": "****", "genezioProvisioned": false}, {"key": "BLOB_READ_WRITE_TOKEN", "defaultValue": "****", "genezioProvisioned": false}, {"key": "POSTGRES_URL", "defaultValue": "****", "genezioProvisioned": false}]}], "services": [{"databases": ["postgres"]}]}'],
    },
    {
        "url": "https://github.com/Genez-io/express-react-getting-started",
        "test_name": "express_react_getting_started",
        "expected_stdout": ['{"frontend":[{"component":"vite"}], "backend":[{"component":"express"}]}'],
    },
    {
        "url": "https://github.com/Genez-io/svelte-getting-started",
        "test_name": "svelte_getting_started",
        "expected_stdout": ['{"frontend":[{"component":"svelte"}]}'],
    },
    {
        "url": "https://github.com/Genez-io/react-getting-started",
        "test_name": "react_getting_started",
        "expected_stdout": ['{"frontend":[{"component":"vite"}]}'],
    },
    {
        "url": "https://github.com/Genez-io/nuxt-getting-started",
        "test_name": "nuxt_getting_started",
        "expected_stdout": ['{"ssr":[{"component":"nuxt"}]}'],
    },
    {
        "url": "https://github.com/vercel/ai-chatbot",
        "test_name": "ai_chatbot",
        "expected_stdout": ['{"ssr":[{"component":"next","environment":[{"key":"OPENAI_API_KEY","defaultValue":"****","genezioProvisioned":false},{"key":"AUTH_SECRET","defaultValue":"****","genezioProvisioned":false},{"key":"BLOB_READ_WRITE_TOKEN","defaultValue":"****","genezioProvisioned":false},{"key":"POSTGRES_URL","defaultValue":"****","genezioProvisioned":false}]}],"services":[{"databases":["postgres"]}]}']
    },
    {
        "url": "https://github.com/andreia-oca/genezio-analyze-socketio-chat-example",
        "test_name": "socketio_chat_example",
        "expected_stdout": ['{"services": [{"databases": ["mongo"]}], "backend": [{"component": "express"}]}'],
    },
    {
        "url": "https://github.com/andreia-oca/genezio-analyze-unimportable",
        "test_name": "genezio_analyze_unimportable",
        "expected_stdout": ['{"backend":[{"component":"other"}],"frontend":[{"component":"other"}]}'],
    },
    {
        "url": "https://github.com/andreia-oca/genezio-analyze-typesafe",
        "test_name": "genezio_analyze_typesafe",
        "expected_stdout": ['{"backend":[{"component":"genezio-typesafe"}],"frontend":[{"component":"vite"}]}'],
    },
    {
        "url": "https://github.com/Genez-io/nestjs-react-getting-started",
        "test_name": "nestjs_react_getting_started",
        "expected_stdout": ['{"frontend":[{"component":"vite"}],"backend":[{"component":"nestjs"}]}'],
    }
]

def clone_repository(repo_url, target_dir):
    """Clones a repository into the specified target directory."""
    Repo.clone_from(repo_url, target_dir, depth=1)
    # print(f"Cloned {repo_url} successfully")

def run_genezio_analyze(repo_dir):
    """Runs `genezio analyze` in the given repository directory and captures the output."""
    # CI should be set to true to avoid interactive prompts
    os.environ['CI'] = 'true'
    result = subprocess.run(
        ['genezio', 'analyze', '--logLevel', 'info', '--format', 'json'],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    return result

def assert_no_errors(result):
    """Asserts that no errors were returned by the `genezio analyze` command."""
    assert result.returncode == 0, f"Error: {result.stderr}"


def assert_stdout(result, expected_stdout):
    """Asserts that stdout contains expected JSON content."""
    try:
        actual_stdout_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise AssertionError("Failed to parse stdout as JSON. Invalid JSON format:\n" + result.stdout)

    # Loop through each expected JSON item to ensure it exists in actual JSON output
    for expected_item in expected_stdout:
        expected_json = json.loads(expected_item)  # Parse each expected output as JSON
        assert actual_stdout_json == expected_json, (
            f"Mismatch in expected and actual JSON output.\nExpected: {expected_json}\nActual: {actual_stdout_json}"
        )

def compare_yaml_files(generated_yaml, expected_yaml):
    """Compares the generated genezio.yaml with the expected one, ignoring the `name` and `frontend.subdomain` fields."""
    # Check if the expected YAML file is empty
    with open(expected_yaml, 'r') as expected_file:
        expected_data = yaml.safe_load(expected_file) or {}

    # If expected YAML is empty, check if generated YAML is either empty or non-existent
    if not expected_data:
        if not os.path.exists(generated_yaml):
            return  # Both are considered 'empty', so no further comparison is needed
        with open(generated_yaml, 'r') as generated_file:
            generated_data = yaml.safe_load(generated_file) or {}
        if not generated_data:
            return  # Both are empty, so no mismatch
        else:
            # If generated YAML is not empty, raise an assertion error
            raise AssertionError("Expected genezio.yaml is empty, but generated genezio.yaml is not empty.")

    if not os.path.exists(generated_yaml):
        raise AssertionError("Generated genezio.yaml is not found or empty, but expected genezio.yaml is not empty.")

    with open(generated_yaml, 'r') as generated_file, open(expected_yaml, 'r') as expected_file:
        generated_data = yaml.safe_load(generated_file)
        expected_data = yaml.safe_load(expected_file)

    # Remove the `name` field
    generated_data.pop('name', None)
    expected_data.pop('name', None)

    # Remove `frontend.subdomain` if it exists
    if 'frontend' in generated_data:
        generated_data['frontend'].pop('subdomain', None)
    if 'frontend' in expected_data:
        expected_data['frontend'].pop('subdomain', None)

    # Check if there is any difference between the modified data
    if generated_data != expected_data:
        # Convert dictionaries back to formatted YAML strings for comparison
        generated_yaml_str = yaml.dump(generated_data, sort_keys=True)
        expected_yaml_str = yaml.dump(expected_data, sort_keys=True)

        # Generate a unified diff between the expected and generated YAML
        diff = '\n'.join(unified_diff(
            expected_yaml_str.splitlines(),
            generated_yaml_str.splitlines(),
            fromfile='expected_genezio.yaml',
            tofile='generated_genezio.yaml',
            lineterm=''
        ))

        # Raise an assertion error with the diff
        raise AssertionError(f"Mismatch in generated and expected genezio.yaml files:\n{diff}")

def run_test(repo_info):
    repo_url = repo_info["url"]
    test_name = repo_info["test_name"]
    expected_stdout = repo_info["expected_stdout"]
    expected_yaml_path = os.path.join('./expected_configuration_files', f'{test_name}.yaml')

    system_temp_dir = tempfile.gettempdir()
    temp_dir = tempfile.mkdtemp(dir=system_temp_dir)

    try:
        # Clone the repository into temp_dir
        clone_repository(repo_url, temp_dir)

        # Ensure repository is cloned successfully
        if not os.listdir(temp_dir):
            print(f"Error: Repository cloning failed or directory {temp_dir} is empty.")
            raise AssertionError

        # Path to genezio.yaml in the cloned directory
        genezio_yaml_path = os.path.join(temp_dir, "genezio.yaml")

        # Remove `genezio.yaml` if it exists
        if os.path.exists(genezio_yaml_path):
            os.remove(genezio_yaml_path)

        # Run genezio analyze and capture the result
        result = run_genezio_analyze(temp_dir)

        # Assertions
        assert_no_errors(result)
        assert_stdout(result, expected_stdout)

        # Compare generated and expected genezio.yaml
        compare_yaml_files(genezio_yaml_path, expected_yaml_path)

        print(f"================\n{test_name} - test passed!\n================\n")
    except Exception as e:
        print(f"================\n{test_name} - test failed!\n{e}\n================\n")
        return False
    finally:
        # Clean up temp_dir
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    return True

def main():
    failed_tests = []

    # Parse the command-line argument for test name
    parser = argparse.ArgumentParser(description="Run specific a test case")
    parser.add_argument("test_name", nargs="?", help="Name of the test to run")
    args = parser.parse_args()

    if args.test_name:
        # Use filter to find the repository matching the test name
        filtered_repos = list(filter(lambda r: r["test_name"] == args.test_name, repositories))
        if filtered_repos:
            repo_info = filtered_repos[0]
            if not run_test(repo_info):
                failed_tests.append(args.test_name)
        else:
            print(f"Test name '{args.test_name}' not found in the repository list.")
            return
    else:
        # Run all tests
        for repo_info in repositories:
            test_name = repo_info["test_name"]
            if not run_test(repo_info):
                failed_tests.append(test_name)

    if failed_tests:
        print("The following test(s) failed:", failed_tests)
        exit(1)
    else:
        print("All tests passed successfully.")

if __name__ == "__main__":
    main()
