from .base_connector import BaseConnector
import asyncio

class BadooConnector(BaseConnector):
    async def connect(self):
        print("Connecting to BadooConnector...")
        await asyncio.sleep(1)
        self.connected = True
        print("Connected to BadooConnector")

    async def disconnect(self):
        print("Disconnecting from BadooConnector...")
        await asyncio.sleep(1)
        self.connected = False
        print("Disconnected from BadooConnector")

    async def join_meeting(self, meeting_link: str):
        if not self.connected:
            await self.connect()
        print(f"Joining BadooConnector meeting: {meeting_link}")

    async def send_message(self, channel_id: str, message: str):
        if not self.connected:
            await self.connect()
        print(f"Sending message to BadooConnector channel {channel_id}: {message}")
