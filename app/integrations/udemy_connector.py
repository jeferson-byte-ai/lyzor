from .base_connector import BaseConnector
import asyncio

class UdemyConnector(BaseConnector):
    async def connect(self):
        print("Connecting to UdemyConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to UdemyConnector")

    async def disconnect(self):
        print("Disconnecting from UdemyConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from UdemyConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining UdemyConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to UdemyConnector channel {channel_id}: {message}")
