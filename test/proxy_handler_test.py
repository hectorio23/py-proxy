import subprocess
import requests
import asyncio

async def ServerHandler(reader, writer):
    '''This function handles the I/O of the proxy server'''
    data = await reader.read(1024)
    url = data.decode('utf-8')  # Decodifica el mensaje para obtener la URL

    # Try to request to the URL and the result tries to response 
    # write it on a HTML file
    # Then, open de navigator of your choice
    # In this phase this project is developing on a Linux Computer 
     
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open("./response.html", "w") as file:
            file.write(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
    
    finally:
        subprocess.run("brave response.html", shell=True)

    writer.write(b"Conexion finalizada")
    await writer.drain()

    # Close the connection with the client
    writer.close()
    await writer.wait_closed()

async def ProxyHandler():
    '''This function creates a server that is listening on the port 8080'''
    server = await asyncio.start_server(
        ServerHandler,
        host="127.0.0.1",
        port=8080
    ) 

    # Shows the IP and the port of the server
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    # Keep the server listening on the port 8080
    async with server:
        await server.serve_forever()

asyncio.run(ProxyHandler())
