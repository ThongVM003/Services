# read input and send to websocket

import asyncio
import websockets
import json
from rich import print
from rich.console import Console

console = Console()


async def send():
    uri = "ws://180.148.0.215:8001/events"
    async for websocket in websockets.connect(uri):
        try:
            while True:
                msg = input("Enter message: ")
                data = {"message": msg}
                await websocket.send(json.dumps(data))

        except websockets.ConnectionClosed:
            console.print("Connection closed")
            continue


asyncio.get_event_loop().run_until_complete(send())
asyncio.get_event_loop().run_forever()
