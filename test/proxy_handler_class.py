# /usr/bin/python3
'''
hectorio23

Cabe recalcar que esto esta en fase de desarrollo, Se necesita
aun aplicar suficiente testeo para comprobar que no haya `bugs`
o comportamiento no programado.
Este servidor basico no puede realizar peticiones HTTPS, aun no 
esta implementado.
'''

import socketserver
import http.server
import http.client

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    '''This Class creates and heandle the Navigator request

        As su can read, this class is the worker who `intercept` the navigator
        request and send the request for it and send again the response to the 
        navigator.
        It's important to get a good privacity now for the internet, for that, more later 
        I will implement some functinalities who allowed to us to change the request headers.

    '''
    def do_GET(self):
        '''Tries to send the response'''
        try:
            # Conectarse al servidor remoto
            remote = http.client.HTTPConnection(self.path)
            remote.request("GET", self.path)
            response = remote.getresponse()

            # Enviar la respuesta al cliente (navegador)
            self.send_response(response.status)
            for header, value in response.getheaders():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response.read())
            print("Peticion enviada")
        except Exception as e:
            '''Send the error if there is'''
            self.send_error(500, f"Error: {e}")
    
    def do_CONNECT(self):
        print(self.path)
        remote = http.client.HTTPConnection(self.path)
        remote.request("GET", self.path)
        response = remote.getresponse()

        self.send_response(response.status)
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.send_response(response.code)
        self.end_headers()
        self.wfile.write(b"Hola bro XD")


def run_proxy_server():
    '''Creates the server and listen in the following port'''
    port = 9090  
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), ProxyHandler) as server:
        print(f"Proxy en funcionamiento en el puerto {port}")
        server.serve_forever()


run_proxy_server()