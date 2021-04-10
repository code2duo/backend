import json
import asyncio
from typing import Optional

from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from django.contrib.auth.models import AnonymousUser

from ..models import Profile, Contest


class MatchMakingConsumer(AsyncConsumer):
    """
    Canvas Consumer

    @status_codes:
        200 - OK
        400 - NOT LEVEL SET
        401 - AUTHENTICATION ERROR
    """

    async def find_team(self):
        """
        Utility function to find teams for matchmaking
        """

        while self.connected:
            await asyncio.sleep(10)
            profile = self.get_searching_user()
            if profile is not None:
                break
        if self.connected:
            # TODO remaining changes to prevent race condition
            await self.send_json(content={

            }, close=True)

    async def websocket_connect(self, event):
        """
        Websocket Connect
        """
        # needs to accept the socket connection to allow sending data
        await self.accept()

        user = self.scope["user"]
        if user == AnonymousUser():
            # if invalid token is sent then we return and ERROR saying Invalid User
            await self.unauthenticated()
        else:
            profile = user.profile
            match_type = self.scope["url_route"]["kwargs"]["match_type"]
            if profile.level is None:
                await self.no_level_set()
            elif match_type not in ("1v1", "2v2"):
                await self.missing_match_type()
            else:
                self.connected = True
                await self.update_profile_status(profile, True)
                asyncio.create_task(self.find_team)

    async def websocket_disconnect(self, event):
        """
        Websocket Disconnect
        """

        self.connected = False
        await self.update_profile_status(self.scope["user"].profile, True)

        raise StopConsumer()

    async def update_profile_status(self, profile: Profile, val: bool) -> None:
        """
        Updates Profile Stats
        """
        profile.is_searching = val

        await self.__save_profile_stats(profile)

    @database_sync_to_async
    def __save_profile_stats(self, profile: Profile):
        """
        Saves Room Object after updating
        """
        profile.save(
            update_fields=[
                "is_searching",
            ]
        )

    @database_sync_to_async
    def get_searching_user(self) -> Optional[Profile]:
        """
        Returns Profile Object
        """
        try:
            return Profile.objects.get(is_searching=True)
        except Profile.DoesNotExist:
            return None

    async def send_json(self, content, code=200, status="OK", close=False):
        """
        Encode the given content as JSON and send it to the client.
        """

        await self.send(
            text_data=await self.encode_json(
                {"status": status, "message": content, "code": code}
            ),
            close=close,
        )

    async def unauthenticated(self):
        """
        Handles Unauthenticated Connections
        """

        await self.send_json(
            content="Invalid User",
            code=401,
            close=True,
        )

    async def no_level_set(self):
        """
        Handles case where profile has no level set
        """

        await self.send_json(
            content="Level not set",
            code=400,
            close=True,
        )

    async def missing_match_type(self):
        """
        Handles case where
        """

        await self.send_json(
            content="Match Type Mismatch",
            code=403,
            close=True,
        )

    async def accept(self):
        """
        Accepts an incoming socket
        """
        await super().send({"type": "websocket.accept"})

    async def send(self, text_data=None, bytes_data=None, close=False):
        """
        Sends a reply back down the WebSocket
        """
        if text_data is not None:
            await super().send({"type": "websocket.send", "text": text_data})
        elif bytes_data is not None:
            await super().send({"type": "websocket.send", "bytes": bytes_data})
        else:
            raise ValueError("You must pass one of bytes_data or text_data")
        if close:
            await self.close(close)

    async def close(self, code=None):
        """
        Closes the WebSocket from the server end
        """
        if code is not None and code is not True:
            await super().send({"type": "websocket.close", "code": code})
        else:
            await super().send({"type": "websocket.close"})

    @classmethod
    async def decode_json(cls, text_data):
        """
        Serializers string to JSON
        """
        return json.loads(text_data)

    @classmethod
    async def encode_json(cls, content):
        """
        Serializers JSON to string
        """
        return json.dumps(content)
