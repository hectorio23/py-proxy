import socketserver
import http.client
import http.server
import ssl

class ServerHandler:
    ...

class ProxyHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.PORT = 8080
            cls.ADDRESS  = '127.0.0.1'
            cls.actived = False
        return cls._instance
    
    def run_server(self):
        with socketserver.TCPServer((self.PORT, self.ADDRESS), ServerHandler) as server:
            print(f"Serving on ({ self.ADDRESS } { self.PORT })")
            cls.actived = True
            server.serve_forever()
        

if __name__ == '__main__':
    ...