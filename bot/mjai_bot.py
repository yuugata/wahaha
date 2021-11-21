""" 
 mjai_bot.py

 Usage : python -m bot.mjai_bot

"""

import json
import asyncio
import random
from mjlegal.mjai_player_loader import MjaiPlayerLoader
from mjlegal.mjai_possible_action import MjaiPossibleActionGenerator


class MjaiBot :
    def reset(self) : 
        self.mjaiPlayerLoader = MjaiPlayerLoader()
        self.mjaiPossibleActionGenerator = MjaiPossibleActionGenerator()

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

            # Notify an event from mjai server
            self.mjaiPlayerLoader.action_receive(event)
            
            # Get possible moves
            possible_actions = self.mjaiPossibleActionGenerator.possible_mjai_action(self.mjaiPlayerLoader.game, event)
            
            # Choice a random move
            move = random.choice(possible_actions)
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
