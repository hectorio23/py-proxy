# /usr/bin/python3
import socketserver
import http.server
import urllib.parse
import http.client

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

    # def do_CONNECT(self):
    #     self.handle_request("CONNECT")

    def handle_request(self, method):
        # Parsear la URL de destino
        url_parts = urllib.parse.urlsplit(self.path)
        host = url_parts.netloc
        path = url_parts.path
        # Crear una conexión al servidor de destino
        conn = http.client.HTTPConnection(host)
        conn.request(method, path, body=self.rfile.read(int(self.headers.get('Content-Length', 0))), headers=self.headers)
        # Obtener la respuesta del servidor de destino
        response = conn.getresponse()
        # Leer el contenido de la respuesta
        data = response.read()
        # Modificar los encabezados de respuesta para que el navegador reconozca al proxy
        self.send_response(response.status)
        self.send_header("Proxy-Agent", "MiProxy")
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()
        # Enviar la respuesta al navegador
        self.wfile.write(data)

def ProxyHandler():
    '''
    This function creates a TCP Server that will get the 
    navigator posts and handles it
    '''
    PORT = 9099
    HOST = '127.0.0.1'

    # Open one TCP Server
    with socketserver.ThreadingTCPServer((HOST, PORT), ServerHandler) as server:
        print(f"Server serving on ({HOST}, {PORT})")
        server.serve_forever()

if __name__ == '__main__':
    ProxyHandler()
