from .base_connector import BaseConnector
import asyncio

class TrovoConnector(BaseConnector):
    async def connect(self):
        print("Connecting to TrovoConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to TrovoConnector")

    async def disconnect(self):
        print("Disconnecting from TrovoConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from TrovoConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining TrovoConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to TrovoConnector channel {channel_id}: {message}")
