import requests
import time
import asyncio
import random
import os
import concurrent.futures
from genezio import genezio_deploy, genezio_login, genezio_local, genezio_delete
from dotenv import load_dotenv


load_dotenv()

base_url = os.getenv("BASE_FUNCTION_URL")

def call_function():
    def send_request(random_number):
        url = f"{base_url}{random_number}"
        response = requests.get(url)
        print(f"Called URL: {url}, Status Code: {response.status_code}, Response: {response.text}")
        assert response.status_code == 200
        assert response.text == str(random_number)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(10):
            random_number = random.randint(1, 100) * 2
            futures.append(executor.submit(send_request, random_number))
        concurrent.futures.wait(futures)

def call_function_with_fails():
    def send_request(random_number):
        url = f"{base_url}{random_number}"
        print(random_number)
        response = requests.get(url)
        print(f"Called URL: {url}, Status Code: {response.status_code}, Response: {response.text}")
        if random_number % 2 == 1:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
            assert response.text == str(random_number)
        time.sleep(0.01)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(10):
            random_number = random.randint(1, 100)
            futures.append(executor.submit(send_request, random_number))
        concurrent.futures.wait(futures)
def call_function_with_timeouts():
    def send_request(random_number):

        url = f"{base_url}timeout/{random_number}"
        print(random_number)
        response = requests.get(url)
        print(f"Called URL: {url}, Status Code: {response.status_code}, Response: {response.text}")
        if random_number % 2 == 1:
            assert response.status_code == 200
            assert response.text == str(random_number)
        time.sleep(0.01)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(10):
            random_number = random.randint(1, 100)
            futures.append(executor.submit(send_request, random_number))
        concurrent.futures.wait(futures)

def call_function_with_some_js_errors():
    def send_request(random_number):

        url = f"{base_url}error/{random_number}"
        print(random_number)
        response = requests.get(url)
        print(f"Called URL: {url}, Status Code: {response.status_code}, Response: {response.text}")
        assert response.status_code == 200
        assert response.text == str(random_number)
        time.sleep(0.01)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(10):
            random_number = random.randint(1, 100)
            futures.append(executor.submit(send_request, random_number))
        concurrent.futures.wait(futures) 

def test_parallel_calls():
    print("Starting parallel calls test...")
    token = os.environ.get('GENEZIO_TOKEN')
    genezio_login(token)
    os.chdir("./projects/express-test-template/")
    deploy_result = genezio_deploy(False) 
    print(deploy_result.stdout_all_links[0][0])
    base_url = deploy_result.stdout_all_links[0][0]
    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    print("GOOD WHEATHER FUNCTION")
    call_function()

    print("FUNCTION WITH FAILS")
    call_function_with_fails()

    print("FUNCTION WITH TIMEOUTS")
    call_function_with_timeouts()

    print("FUNCTION WITH JS ERRORS")
    call_function_with_some_js_errors()

if __name__ == '__main__':
    test_parallel_calls()    
