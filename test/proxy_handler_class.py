import socketserver
import http.server
import http.client
import urllib.parse

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        remote = http.client.HTTPSConnection(host=url.netloc, port=443, timeout=10)
        remote.request("GET", url=url.path)
        response = remote.getresponse()

        self.send_response(response.status)
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()

        self.wfile.write(response.read())

    def do_POST(self):
        url = urllib.parse.urlsplit(self.path)
        remote = http.client.HTTPSConnection(host=url.netloc, port=443, timeout=5)
        remote.request("POST", url=url.path)
        response = remote.getresponse()
        print(self.path)

        self.send_response(response.status)
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()

        self.wfile.write(response.read())

    def do_CONNECT(self):
        # Obtener el host y el puerto del CONNECT request
        host, port = self.path.split(':')
        port = int(port)

        # Establecer la conexión con el servidor remoto
        remote = http.client.HTTPSConnection(host, port, timeout=5)
        remote.connect()

        # Enviar la respuesta al cliente (navegador)
        self.send_response(200, 'Connection established')
        self.end_headers()

        # Configurar el reenvío de datos entre el cliente y el servidor
        self.connection.sendall(b'HTTP/1.1 200 Connection established\r\n\r\n')
        self.connection = remote.sock

        # Leer datos del cliente y reenviar al servidor
        while True:
            data = self.connection.recv(4096)
            if not data:
                break
            self.connection.sendall(data)

def run_proxy_server():
    port = 9090
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), ProxyHandler) as server:
        print(f"Proxy en funcionamiento en el puerto {port}")
        server.serve_forever()

run_proxy_server()
