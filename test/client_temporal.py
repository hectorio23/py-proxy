# /usr/bin/python3
import requests

def make_request():
    PROXY_URL = 'http://127.0.0.1:8085'
    URL = 'https://doc.python.org'


    response = requests.get(URL, proxies={"http": PROXY_URL, "https": PROXY_URL})

    print("Proxy Response Code:", response.status_code)
    print("Proxy Response Body:", response.text)
    print("Proxy Response Body:", response.headers)

if __name__ == "__main__":
    make_request()