from .base_connector import BaseConnector
import asyncio

class SteamConnector(BaseConnector):
    async def connect(self):
        print("Connecting to SteamConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to SteamConnector")

    async def disconnect(self):
        print("Disconnecting from SteamConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from SteamConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining SteamConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to SteamConnector channel {channel_id}: {message}")
