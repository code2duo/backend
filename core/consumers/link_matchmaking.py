import json
from random import choice
from typing import List, Optional

from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from django.contrib.auth.models import AnonymousUser
from django.db import models
from rest_framework import serializers

from core.models import Profile, Contest, Searching, MatchRoom, Question
from core.serializers import ContestSerializer


class MatchMakingConsumer(AsyncConsumer):
    """
    Match Making Consumer

    @status_codes:
        200 - OK
        401 - AUTHENTICATION ERROR
        403 - Room Full
    """

    async def websocket_connect(self, event):
        """
        Websocket Connect
        """
        # needs to accept the socket connection to allow sending data
        await self.accept()
        self.connected = False
        user = self.scope["user"]
        if user == AnonymousUser():
            # if invalid token is sent then we return and ERROR saying Invalid User
            await self.unauthenticated()
        else:
            profile = await self.get_profile()
            room_id = self.scope["url_route"]["kwargs"]["room_id"]
            flag = True
            contest_obj = None
            match_room_obj: MatchRoom = await self.get_match_room(room_id)
            if match_room_obj is None:
                flag = False
                await self.send_json(
                    status="ERROR",
                    content="Invalid Room ID",
                    code=400,
                    close=True,
                )
            elif match_room_obj.participant_1 and match_room_obj.participant_2:
                flag = False
                await self.send_json(
                    status="ERROR",
                    content="Room is already full",
                    code=403,
                    close=True,
                )
            elif match_room_obj.participant_1:
                match_room_obj = await self.add_or_remove_participant(match_room_obj, profile, 2)
                contest_obj = await self.create_contest(room_id, match_room_obj.participant_1, match_room_obj.participant_2)
            else:
                match_room_obj = await self.add_or_remove_participant(match_room_obj, profile, 1)

            if flag:
                self.connected = True

                match_room_name = f"match_{room_id}"
                self.match_room_name = match_room_name

                await self.channel_layer.group_add(
                    match_room_name,
                    self.channel_name,
                )

                if contest_obj:
                    new_contest_event = {
                        "type": "match_data_event",
                        "text": await self.encode_json(
                            {
                                "status": "OK",
                                "message": await self.serialize(contest_obj, ContestSerializer),
                                "code": 200,
                            }
                        ),
                    }
                    # broadcasts the message event to be sent
                    await self.channel_layer.group_send(
                        self.match_room_name,
                        new_contest_event,
                    )

    async def websocket_receive(self, event):
        """
        Websocket Receive
        """
        user = self.scope["user"]

        if user == AnonymousUser():
            await self.unauthenticated()
        elif self.connected:
            new_event = {
                "type": "match_data_event",
                "text": await self.encode_json(
                    {
                        "status": "OK",
                        "message": await self.decode_json(event["text"]),
                        "code": 200,
                    }
                ),
            }
            # broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.match_room_name,
                new_event,
            )

    async def match_data_event(self, event):
        """
        Handler for Canvas Drawings
        """
        # sends the actual message
        await self.send(
            text_data=event["text"],
        )

    async def websocket_disconnect(self, event):
        """
        Websocket Disconnect
        """

        self.connected = False

        user = self.scope["user"]
        room_id = self.scope["url_route"]["kwargs"]["room_id"]

        match_room_obj: MatchRoom = await self.get_match_room(room_id)

        if user == AnonymousUser():
            await self.unauthenticated()
        elif match_room_obj is None:
            await self.send_json(
                status="ERROR",
                content="Invalid Room ID",
                code=400,
                close=True,
            )
        else:
            if match_room_obj.participant_1 == user.profile:
                match_room_obj = await self.add_or_remove_participant(match_room_obj, None, 1)
            elif match_room_obj.participant_2 == user.profile:
                await self.add_or_remove_participant(match_room_obj, None, 2)

            await self.update_or_delete_match_room(match_room_obj)

        raise StopConsumer()

    @database_sync_to_async
    def serialize(self, model_obj: models.Model, SerializerClass: serializers.ModelSerializer) -> dict:
        return SerializerClass(model_obj).data

    @database_sync_to_async
    def get_profile(self) -> Profile:
        user = self.scope["user"]
        return user.profile

    @database_sync_to_async
    def add_or_remove_participant(self, match_room_obj: MatchRoom, profile: Optional[Profile], num) -> MatchRoom:
        if num == 1:
            match_room_obj.participant_1 = profile
        elif num == 2:
            match_room_obj.participant_2 = profile
        # saving match model
        self.save_match_room(match_room_obj)
        return match_room_obj

    @database_sync_to_async
    def get_match_room(self, room_id: str) -> Optional[MatchRoom]:
        """
        Returns Match Room Object
        """

        try:
            return MatchRoom.objects.select_related("participant_1", "participant_2").get(room_id__exact=room_id)
        except MatchRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def create_contest(self, room_id: str, participant_1: Profile, participant_2: Profile) -> Contest:
        """
        Returns Contest Object
        """

        contest = Contest(room_id=room_id, participant_1=participant_1, participant_2=participant_2)
        questions: List[Question] = self.__get_questions_queryset(participant_1.level, participant_2.level)
        contest.save()
        contest.questions.add(questions[0])
        contest.questions.add(questions[1])
        contest.questions.add(questions[2])
        contest.save()

        return contest

    @staticmethod
    def __get_questions_queryset(difficulty_1, difficulty_2) -> List[Question]:
        questions = list()
        _max, _min = max(difficulty_1, difficulty_2), min(difficulty_1, difficulty_2)
        random_question_level = choice(range(_min, _max+1))
        try:
            questions.append(choice(Question.objects.filter(level=random_question_level)))
            questions.append(choice(Question.objects.filter(level=difficulty_1)))
            questions.append(choice(Question.objects.filter(level=difficulty_2)))
        except IndexError:
            pass

        return questions

    @database_sync_to_async
    def delete_searching_object(self, searching_obj: Searching) -> None:
        searching_obj.delete()

    @database_sync_to_async
    def update_or_delete_match_room(self, match_room_obj: MatchRoom) -> None:
        """
        Update or delete Match Room obj
        """

        if match_room_obj.participant_1 is None and match_room_obj.participant_2 is None:
            match_room_obj.delete()
        else:
            self.save_match_room(match_room_obj)

    @staticmethod
    def save_match_room(match_room_obj: MatchRoom) -> None:
        match_room_obj.save(
            update_fields=[
                "participant_1",
                "participant_2",
            ]
        )

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
