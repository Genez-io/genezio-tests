import requests
def handler(event):
    print("Function was invoked with event: {}".format(event))
    response = requests.get("http://ip-api.com/json")
    if response.status_code == 200:
        return {
            "statusCode": response.status_code,
            "body": response.json()
        }
    else:
        return {
            "statusCode": response.status_code,
            "body": "Error"
        }