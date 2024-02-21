# Héctor Adán
# https://github.com/hectorio23
import socketserver
import http.server
import urllib.parse
import http.client
import json

with open('./config.json', 'r') as config_file:
    file = json.load(config_file)

class ServerHandler(http.server.BaseHTTPRequestHandler):
    ''' ServerHandler   
    This is a class that has some methods that allows to the
    server Proxy to handle the request headers to be carefully 
    there out
    '''
    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_CONNECT(self):
        self.handle_request("CONNECT")

    def handle_request(self, method):
        # Parsear la URL de destino
        url_parts = urllib.parse.urlsplit(self.path)
        host = url_parts.netloc
        path = url_parts.path
        # Crear una conexión al servidor de destino
        print(f"Connecting to host: { str(url_parts) }")
        print(self.path)
        print(method)

        if method == 'CONNECT':
            conn = http.client.HTTPSConnection(host, port=443)
            conn.request(method, path, headers=self.headers)


        else:
            conn = http.client.HTTPConnection(host)
            conn.request(method, path, body=self.rfile.read(
                int(self.headers.get('Content-Length', 0))), 
                headers=self.headers
            )
            
        # Obtener la respuesta del servidor de destino
        response = conn.getresponse()
        # Leer el contenido de la respuesta
        data = response.read()
        
        # Modificar los encabezados de respuesta para que el navegador reconozca al proxy
        self.send_response(response.status)
        self.send_header("Proxy-Agent", "MiProxy")
        self.send_header("User-Agent", "py-proxy")
        self.send_header("Server", "py-proxy")

        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()

        # Enviar la respuesta al navegador
        self.wfile.write(data)

class ProxyServer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.PORT = file['PORT']
            cls._instance.HOST = file['HOST']
        return cls._instance

    def run(self):
        with socketserver.ThreadingTCPServer((self.HOST, self.PORT), ServerHandler) as server:
            print(f"Server serving on ({self.HOST}, {self.PORT})")
            server.serve_forever()

if __name__ == '__main__':
    proxy_server = ProxyServer()
    proxy_server.run()
