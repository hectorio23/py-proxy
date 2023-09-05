# /usr/bin/python3
import socketserver
import http.server
import asyncio

class ServerHandler(http.server.BaseHTTPRequestHandler):
    ''' ServerHandler   
    This is a class that has some methods that allows to the
    server Proxy to handle the request headers to be carefully 
    there out
    '''
    def do_GET():
        url_parts = urllib.parse.urlsplit(self.path)
        print(url_parts)

def ProxyHandler():
    '''
    This function creates a TCP Server that will get the 
    navigator posts and handles it
    '''
    PORT = 8080
    HOST = '127.0.0.1'

    # Open one TCP Server 
    with socketserver.ThreadingTCPServer((HOST, PORT), ServerHandler) as server:
        # Create the server and it is listening 
        print(f"Server servin on ({ HOST }, { PORT })")
        server.serve_forever()



# Run the main Coro
ProxyHandler()