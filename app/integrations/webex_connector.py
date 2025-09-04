from .base_connector import BaseConnector
import asyncio

class WebexConnector(BaseConnector):
    async def connect(self):
        print("Connecting to WebexConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to WebexConnector")

    async def disconnect(self):
        print("Disconnecting from WebexConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from WebexConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining WebexConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to WebexConnector channel {channel_id}: {message}")
