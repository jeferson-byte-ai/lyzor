from .base_connector import BaseConnector
import asyncio

class GTARPConnector(BaseConnector):
    async def connect(self):
        print("Connecting to GTARPConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to GTARPConnector")

    async def disconnect(self):
        print("Disconnecting from GTARPConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from GTARPConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining GTARPConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to GTARPConnector channel {channel_id}: {message}")
