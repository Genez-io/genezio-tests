import sys
def handler(event):
    return {
        "statusCode": 200,
        "body": f"{sys.version}"
    }
