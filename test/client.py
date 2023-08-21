# import asyncio


# async def ProxyHandler():
#     reader, writer = await asyncio.open_connection(
#         '127.0.0.1', 
#         9999,
#         limit=1024,
#         ssl=None,
#         family=0,
#         proto=0,
#         flags=0,
#         sock=None,
#         local_addr=None,
#         # server_hostname="https://adan.com",
#         # ssl_handshake_timeout=0,
#         # ssl_shutdown_timeout=0,
#         happy_eyeballs_delay=0,
#         interleave=0
#         )
    
#     writer.write("Esta es una pinche prueba sobre esto".encode('UTF-8'))
#     await writer.drain()

#     data:str = await reader.read(-1)
#     print(reader.at_eof())
#     print(data.decode('UTF-8'))

#     writer.close()
#     await writer.wait_closed()


# asyncio.run(ProxyHandler())

import asyncio
import urllib.parse
import sys

async def print_http_headers(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        reader, writer = await asyncio.open_connection(
            url.hostname, 443, ssl=True)
    else:
        reader, writer = await asyncio.open_connection(
            url.hostname, 80)

    query = (
        f"HEAD {url.path or '/'} HTTP/1.0\r\n"
        f"Host: {url.hostname}\r\n"
        f"\r\n"
    )

    writer.write(query.encode('latin-1'))
    while True:
        line = await reader.readline()
        if not line:
            break

        line = line.decode('latin1').rstrip()
        if line:
            print(f'HTTP header> {line}')

    # Ignore the body, close the socket
    writer.close()
    await writer.wait_closed()

url = sys.argv[1]
asyncio.run(print_http_headers(url))