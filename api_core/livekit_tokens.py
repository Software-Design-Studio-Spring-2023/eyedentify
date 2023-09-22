from livekit import AccessToken
from livekit import VideoGrant
from aiohttp import web
import json


async def generate_student_token(user_id):
    # You need to replace "API_KEY" and "API_SECRET" with your LiveKit API credentials
    API_KEY = "APIHQFZktdSvLyM"
    API_SECRET = "j7c47tGVqe3gZYe6Aai5YT2i2sr8fV9SuPAfI3PO0l9B"

    token = AccessToken(
        API_KEY,
        API_SECRET,
        VideoGrant(room="exam", room_join=True, can_publish=True, can_subscribe=False),
        identity=user_id,
    )
    return token.to_jwt()


async def get_student_token(request):
    user_id = request.match_info.get("id")
    if not user_id:
        return web.Response(status=400, text="User ID is required")

    token = await generate_student_token(user_id)
    return web.Response(
        content_type="application/json", text=json.dumps({"token": token})
    )


async def generate_staff_token(user_id):
    # You need to replace "API_KEY" and "API_SECRET" with your LiveKit API credentials
    API_KEY = "APIHQFZktdSvLyM"
    API_SECRET = "j7c47tGVqe3gZYe6Aai5YT2i2sr8fV9SuPAfI3PO0l9B"

    token = AccessToken(
        API_KEY,
        API_SECRET,
        VideoGrant(room="exam", room_join=True, can_publish=False, can_subscribe=True),
        identity=user_id,
    )
    return token.to_jwt()


async def get_staff_token(request):
    user_id = request.match_info.get("id")
    if not user_id:
        return web.Response(status=400, text="User ID is required")

    token = await generate_staff_token(user_id)
    return web.Response(
        content_type="application/json", text=json.dumps({"token": token})
    )
