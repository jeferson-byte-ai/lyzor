from .base_connector import BaseConnector
import asyncio

class TeamsConnector(BaseConnector):
    async def connect(self):
        print("Connecting to TeamsConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to TeamsConnector")

    async def disconnect(self):
        print("Disconnecting from TeamsConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from TeamsConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining TeamsConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to TeamsConnector channel {channel_id}: {message}")
