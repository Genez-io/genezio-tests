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
def test_parallel_calls():
    # print("Starting parallel calls test...")
    # token = os.environ.get('GENEZIO_TOKEN')
    # genezio_login(token)
    # os.chdir("./projects/express-test-template/")
    # deploy_result = genezio_deploy(False) 
    # print(deploy_result.stdout_all_links[0][0])
    # print("mama")
    # base_url = deploy_result.stdout_all_links[0][0] + "/hello/";
    base_url = "https://2a60caac-bcc5-4a96-b26c-622835db548f.dev-fkt.cloud.genez.io/hello/"
    # assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    # assert deploy_result.project_url != "", "genezio deploy returned empty project url"

    def call_function():
        def send_request(random_number):
            
            url = f"{base_url}{random_number}"
            response = requests.get(url)
            print(f"Called URL: {url}, Status Code: {response.status_code}, Response: {response.text}")
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, for URL: {url}"
            assert response.text == str(random_number), f"Expected response text {random_number}, got {response.text}, for URL: {url}"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for _ in range(10):
                random_number = random.randint(1, 100) * 2
                futures.append(executor.submit(send_request, random_number))
            concurrent.futures.wait(futures)
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except AssertionError as e:
                    print(f"Assertion failed: {e}")
                    raise 
                except Exception as e:
                    print(f"An error occurred: {e}")
                    raise    

    def call_function_with_fails():
        def send_request(random_number):
            url = f"{base_url}{random_number}"
            print(random_number)
            response = requests.get(url)
            print(f"Called URL: {url}, Status Code: {response.status_code}, Response: {response.text}")
            if random_number % 2 == 1:
                assert response.status_code == 404, f"Expected status code 404, got {response.status_code}, for URL: {url}"
            else:
                assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, for URL: {url}"
                assert response.text == str(random_number), f"Expected response text {random_number}, got {response.text}, for URL: {url}"
            time.sleep(0.01)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for _ in range(10):
                random_number = random.randint(1, 100)
                futures.append(executor.submit(send_request, random_number))
            concurrent.futures.wait(futures)

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except AssertionError as e:
                    print(f"Assertion failed: {e}")
                    raise 
                except Exception as e:
                    print(f"An error occurred: {e}")
                    raise  
    def call_function_with_timeouts():
        def send_request(random_number):

            url = f"{base_url}timeout/{random_number}"
            print(random_number)
            response = requests.get(url)
            print(f"Called URL: {url}, Status Code: {response.status_code}, Response: {response.text}")
            if random_number % 2 == 1:
                assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, for URL: {url}"
                assert response.text == str(random_number), f"Expected response text {random_number}, got {response.text}, for URL: {url}"
            time.sleep(0.01)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for _ in range(10):
                random_number = random.randint(1, 100)
                futures.append(executor.submit(send_request, random_number))
            concurrent.futures.wait(futures)

        for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except AssertionError as e:
                    print(f"Assertion failed: {e}")
                    raise 
                except Exception as e:
                    print(f"An error occurred: {e}") 
                    raise   

    def call_function_with_some_js_errors():
        def send_request(random_number):

            url = f"{base_url}error/{random_number}"
            print(random_number)
            response = requests.get(url)
            print(f"Called URL: {url}, Status Code: {response.status_code}, Response: {response.text}")

            if random_number % 3 != 0:
                assert response.status_code == 200, f"Expected status code 200, got {response.status_code}, for URL: {url}"
                assert response.text == str(random_number), f"Expected response text {random_number}, got {response.text}, for URL: {url}"
            else:
                assert response.status_code != 200, f"Expected status code not 200, got {response.status_code}, for URL: {url}"
            time.sleep(0.01)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for _ in range(10):
                random_number = random.randint(1, 100)
                futures.append(executor.submit(send_request, random_number))
            concurrent.futures.wait(futures) 

        for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except AssertionError as e:
                    raise 
                except Exception as e:
                    print(f"An error occurred: {e}") 
                    raise   
    print("GOOD WHEATHER FUNCTION")
    call_function()

    print("FUNCTION WITH FAILS")
    call_function_with_fails()

    def run_functions_in_parallel():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(call_function_with_timeouts),
                executor.submit(call_function_with_some_js_errors)
            ]
            
            for future in concurrent.futures.as_completed(futures):
                if future.exception() is not None:
                    raise future.exception()

         

    run_functions_in_parallel();
    # call_function_with_some_js_errors()
    # call_function_with_timeouts()
    print("ALL TESTS PASSED")      

if __name__ == '__main__':
    test_parallel_calls()    
          