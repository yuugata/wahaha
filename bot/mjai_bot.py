""" 
 mjai_bot.py

 Usage : python -m bot.mjai_bot

"""

import json
import asyncio
from ai.client import Client

class MjaiBot :
    def reset(self) : 
        self.client = Client()
        self.client.setup()

    async def open(self, server = "localhost", port = 11600) :
        self.server = server 
        self.port = port
        self.reader, self.writer = await asyncio.open_connection(self.server, self.port)
        self.reset()

    async def send(self, data) :
        send_str = json.dumps(data) + '\n'
        self.writer.write(send_str.encode())
        await self.writer.drain()

    async def receive(self) :
        data = await self.reader.readline()
        data_str = data.decode()
        receive_json = json.loads(data_str)
        return receive_json

    async def run(self) :
        while True :
            # Receive an event from mjai server
            event = await self.receive()
            print("<- ", event)

            # ai client
            self.client.update_state(event)
            move = self.client.choose_action()
            print("-> ", move)

            # Send a move to mjai server
            await self.send(move)

            # End of game
            if event["type"] == "end_game" :
                break

async def main() :
    mjai = MjaiBot()
    await mjai.open()
    await mjai.run()
    exit(0)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    asyncio.get_event_loop().run_forever()
