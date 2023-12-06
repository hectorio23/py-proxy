# /usr/bin/python3

import http.client

client = http.client.HTTPConnection(
    host="127.0.0.1",
    port=3747,
    source_address=("localhost",4854)
)

print(client.connect())