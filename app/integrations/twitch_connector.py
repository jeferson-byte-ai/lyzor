from .base_connector import BaseConnector
import asyncio

class TwitchConnector(BaseConnector):
    async def connect(self):
        print("Connecting to TwitchConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to TwitchConnector")

    async def disconnect(self):
        print("Disconnecting from TwitchConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from TwitchConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining TwitchConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to TwitchConnector channel {channel_id}: {message}")
