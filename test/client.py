# /usr/bin/python3
import asyncio

async def main():
    config = {
        "host": "127.0.0.1",
        "port": 8080
    }

    reader, writer = await asyncio.open_connection(**config)

    writer.write(b"https://github.com/")
    await writer.drain()

    data = await reader.read(-1)
    print(f"El mensage recibido por el server es: {data.decode('UTF-8')}")

    writer.close()
    await writer.wait_closed()

asyncio.run(main())