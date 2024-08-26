import requests
import time
import random
import os
import concurrent.futures
from genezio import genezio_deploy, genezio_login, genezio_delete
from dotenv import load_dotenv


load_dotenv()

def call_function_with_timeouts(base_url):
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

def call_function(base_url):
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

def call_function_with_some_js_errors(base_url):
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

def run_functions_in_parallel(base_url):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(call_function_with_timeouts, base_url),
            executor.submit(call_function_with_some_js_errors, base_url)
        ]
        
        for future in concurrent.futures.as_completed(futures):
            if future.exception() is not None:
                raise future.exception()  

def call_function_with_fails(base_url):
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

def test_parallel_calls():
    print("Starting parallel calls test...")
    token = os.environ.get('GENEZIO_TOKEN')
    genezio_login(token)
    os.chdir("./projects/express-parallel-calls-template/")
    deploy_result = genezio_deploy(False) 
    base_url = deploy_result.web_urls[0] + "/hello/";
    assert deploy_result.return_code == 0, "genezio deploy returned non-zero exit code"
    assert deploy_result.project_url != "", "genezio deploy returned empty project url"  

    print("GOOD WHEATHER FUNCTION")
    call_function(base_url=base_url)

    print("FUNCTION WITH FAILS")
    call_function_with_fails(base_url=base_url)

    
    run_functions_in_parallel(base_url=base_url);
    os.chdir("../")

    print("Prepared to delete project...")
    genezio_delete(deploy_result.project_id)
    print("ALL TESTS PASSED")      

if __name__ == '__main__':
    test_parallel_calls()    
          