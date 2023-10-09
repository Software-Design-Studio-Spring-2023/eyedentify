import argparse
import asyncio
import json
import logging
import os
import ssl
from aiohttp import web
import aiohttp_cors
from pymongo import MongoClient
from api_core.livekit_tokens import get_student_token, get_staff_token

# set root as ../frontend/
ROOT = os.path.dirname(__file__) + "/frontend/"
logger = logging.getLogger("pc")
pcs = set()
client = MongoClient("mongodb+srv://Reuben:Fire@systemcluster.hwra6cw.mongodb.net/")
db = client["Online-Exam-System"]
userCollection = db["Users"]


def setup_cli_args():
    parser = argparse.ArgumentParser(
        description="WebRTC audio / video / data-channels demo"
    )
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--host", default="localhost", help="Host for HTTP server (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument("--write-audio", help="Write received audio to a file")
    return parser.parse_args()


async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def getAllUsers(request):
    allUsers = userCollection.find({})
    allUsers = list(allUsers)
    for user in allUsers:
        user["_id"] = str(user["_id"])
    return web.Response(content_type="application/json", text=json.dumps(allUsers))


async def update_login(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get("id", None)
        data = await request.json()
        loggedIn = data.get("loggedIn", None)

        if user_id and loggedIn is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one(
                {"id": int(user_id)}, {"$set": {"loggedIn": loggedIn}}
            )

            if response.matched_count:
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"message": "User status updated successfully"}),
                )
            else:
                raise web.HTTPNotFound(text=json.dumps({"message": "User not found"}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({"message": "Invalid input"}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({"message": str(e)}))
    
async def update_warning_one(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get("id", None)
        data = await request.json()
        warningOne = data.get("warningOne", None)

        if user_id and warningOne is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one(
                {"id": int(user_id)}, {"$set": {"warningOne": warningOne}}
            )

            if response.matched_count:
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"message": "User status updated successfully"}),
                )
            else:
                raise web.HTTPNotFound(text=json.dumps({"message": "User not found"}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({"message": "Invalid input"}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({"message": str(e)}))
    
async def update_warning_two(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get("id", None)
        data = await request.json()
        warningTwo = data.get("warningTwo", None)

        if user_id and warningTwo is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one(
                {"id": int(user_id)}, {"$set": {"warningTwo": warningTwo}}
            )

            if response.matched_count:
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"message": "User status updated successfully"}),
                )
            else:
                raise web.HTTPNotFound(text=json.dumps({"message": "User not found"}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({"message": "Invalid input"}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({"message": str(e)}))
    
async def update_ready(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get("id", None)
        data = await request.json()
        ready = data.get("ready", None)

        if user_id and ready is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one(
                {"id": int(user_id)}, {"$set": {"ready": ready}}
            )

            if response.matched_count:
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"message": "User status updated successfully"}),
                )
            else:
                raise web.HTTPNotFound(text=json.dumps({"message": "User not found"}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({"message": "Invalid input"}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({"message": str(e)}))


async def update_terminate(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get("id", None)
        data = await request.json()
        terminated = data.get("terminated", None)

        if user_id and terminated is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one(
                {"id": int(user_id)}, {"$set": {"terminated": terminated}}
            )

            if response.matched_count:
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"message": "User status updated successfully"}),
                )
            else:
                raise web.HTTPNotFound(text=json.dumps({"message": "User not found"}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({"message": "Invalid input"}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({"message": str(e)}))


async def update_warnings(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get("id", None)
        data = await request.json()
        warnings = data.get("warnings", None)

        if user_id and warnings is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one(
                {"id": int(user_id)}, {"$set": {"warnings": warnings}}
            )

            if response.matched_count:
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"message": "User status updated successfully"}),
                )
            else:
                raise web.HTTPNotFound(text=json.dumps({"message": "User not found"}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({"message": "Invalid input"}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({"message": str(e)}))


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


def run_server():
    args = setup_cli_args()
    
    port = int(os.environ.get("PORT", 8080))

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    app = web.Application()
    app.on_shutdown.append(on_shutdown)

    app.router.add_get("/api/all_users", getAllUsers)
    app.router.add_patch("/api/update_login/{id}", update_login)
    app.router.add_patch("/api/update_warnings/{id}", update_warnings)
    app.router.add_patch("/api/update_terminate/{id}", update_terminate)
    app.router.add_patch("/api/update_warning_one/{id}", update_warning_one)
    app.router.add_patch("/api/update_warning_two/{id}", update_warning_two)
    app.router.add_patch("/api/update_ready/{id}", update_ready)
    app.router.add_get("/api/get_student_token/{id}", get_student_token)
    app.router.add_get("/api/get_staff_token/{id}", get_staff_token)
    

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )

    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(
        app, access_log=None, host='0.0.0.0', port=port, ssl_context=ssl_context
    )
