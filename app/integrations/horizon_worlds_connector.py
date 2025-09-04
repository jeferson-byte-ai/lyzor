from .base_connector import BaseConnector
import asyncio

class HorizonWorldsConnector(BaseConnector):
    async def connect(self):
        print("Connecting to HorizonWorldsConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to HorizonWorldsConnector")

    async def disconnect(self):
        print("Disconnecting from HorizonWorldsConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from HorizonWorldsConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining HorizonWorldsConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to HorizonWorldsConnector channel {channel_id}: {message}")
