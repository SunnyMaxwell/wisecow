import requests
import logging
from datetime import datetime
import time
import argparse

logging.basicConfig(filemode='./wisecow_Dummy_test/app_health.log', level=logging.INFO)

def check_application_health(url, expected_status_code):
    try:
        responce = requests.get(url)
        if responce.status_code == expected_status_code:
            logging.info(f"{datetime.now()}: Application is UP. Status Code: {responce.status_code} \n")
            return None
            
        else:
            logging.error(f"{datetime.now()}: Application is Down. Status Code: {responce.status_code} \n")
            return(f"ALERT: Application is Down")
    except Exception as e:
        logging.error(f"{datetime.now()}: Application check failed: \n {e} \n")
        return(f"Error: Please Check the Error, Something went wrong")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Application Health Checker')
    parser.add_argument('--url', type=str, default='https://google.com', help='The URL of the application to check')
    parser.add_argument('--status_code', type=int, default=200, help='The expected status code')
    parser.add_argument('--interval', type=int, default=60, help='The check interval in seconds')

    args = parser.parse_args()
    while True:
        application_status = check_application_health(args.url, args.status_code)
        if application_status:
            print(application_status)
        time.sleep(args.interval)