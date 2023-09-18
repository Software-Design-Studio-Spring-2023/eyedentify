import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
import cv2
from aiohttp import web
# import tracemalloc
import aiohttp_cors
from av import VideoFrame
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
from lib.MongoDbWrapper import MongoDbWrapper
from lib.ObjectDetection import ObjectDetectionWrapper

obj = ObjectDetectionWrapper("1")
users_collection = MongoDbWrapper()

# set root as ../frontend/
ROOT = os.path.dirname(__file__) + "/frontend/"

logger = logging.getLogger("pc")
pcs = set()

from pymongo import MongoClient




class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform

    async def recv(self):
        frame = await self.track.recv()

        if self.transform == "cartoon":
            img = frame.to_ndarray(format="bgr24")

            # prepare color
            img_color = cv2.pyrDown(cv2.pyrDown(img))
            for _ in range(6):
                img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
            img_color = cv2.pyrUp(cv2.pyrUp(img_color))

            # prepare edges
            img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            img_edges = cv2.adaptiveThreshold(
                cv2.medianBlur(img_edges, 7),
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                9,
                2,
            )
            img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

            # combine color and edges
            img = cv2.bitwise_and(img_color, img_edges)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "object-detection":
            img = frame.to_ndarray(format="bgr24")
            detections = obj.detectFrameByFrame(img)
            # draw the detection results onto the original image
            for detection in detections[1]:
                # print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
                cv2.rectangle(
                    img,
                    (detection["box_points"][0], detection["box_points"][1]),
                    (detection["box_points"][2], detection["box_points"][3]),
                    (0, 255, 0),
                    2,
                )
                cv2.putText(
                    img,
                    detection["name"] + " " + str(detection["percentage_probability"]),
                    (detection["box_points"][0], detection["box_points"][1]),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame

        else:
            return frame


async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def get_all_users(request):
    all_users = users_collection.all_users()
    return web.Response(
        content_type="application/json",
        text=json.dumps(all_users),
    )

async def update_login(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get('id', None)
        data = await request.json()
        loggedIn = data.get('loggedIn', None)

        if user_id and loggedIn is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one({'id': int(user_id)}, {'$set': {'loggedIn': loggedIn}})
            
            if response.matched_count:
                return web.Response(content_type="application/json", text=json.dumps({'message': 'User status updated successfully'}))
            else:
                raise web.HTTPNotFound(text=json.dumps({'message': 'User not found'}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({'message': 'Invalid input'}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({'message': str(e)}))
    
async def update_terminate(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get('id', None)
        data = await request.json()
        terminated = data.get('terminated', None)

        if user_id and terminated is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one({'id': int(user_id)}, {'$set': {'terminated': terminated}})
            
            if response.matched_count:
                return web.Response(content_type="application/json", text=json.dumps({'message': 'User status updated successfully'}))
            else:
                raise web.HTTPNotFound(text=json.dumps({'message': 'User not found'}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({'message': 'Invalid input'}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({'message': str(e)}))
    
async def update_warnings(request):
    try:
        # Get user ID and update data from request
        user_id = request.match_info.get('id', None)
        data = await request.json()
        warnings = data.get('warnings', None)

        if user_id and warnings is not None:
            # Find user by ID and update their loggedIn status
            response = userCollection.update_one({'id': int(user_id)}, {'$set': {'warnings': warnings}})
            
            if response.matched_count:
                return web.Response(content_type="application/json", text=json.dumps({'message': 'User status updated successfully'}))
            else:
                raise web.HTTPNotFound(text=json.dumps({'message': 'User not found'}))
        else:
            raise web.HTTPBadRequest(text=json.dumps({'message': 'Invalid input'}))

    except Exception as e:
        return web.Response(status=500, text=json.dumps({'message': str(e)}))

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pcs.add(pc)

    def log_info(msg, *args):
        logger.info(pc_id + " " + msg, *args)

    log_info("Created for %s", request.remote)

    # prepare local media
    # player = MediaPlayer(os.path.join(ROOT, "demo-instruct.wav"))
    # player.audio.set_volume(0)
    if args.write_audio:
        recorder = MediaRecorder(args.write_audio)
    else:
        recorder = MediaBlackhole()

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            if isinstance(message, str) and message.startswith("ping"):
                channel.send("pong" + message[4:])
                channel.send("detections: " + str(obj.currentDetectedObjects))

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        log_info("ICE connection state is %s", pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        log_info("Track %s received", track.kind)

        if track.kind == "audio":
            # pc.addTrack(player.audio)
            recorder.addTrack(track)
        elif track.kind == "video":
            local_video = VideoTransformTrack(
                track, transform=params["video_transform"]
            )
            pc.addTrack(local_video)

        @track.on("ended")
        async def on_ended():
            log_info("Track %s ended", track.kind)
            await recorder.stop()

    # handle offer
    await pc.setRemoteDescription(offer)
    await recorder.start()

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        ),
    )


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


if __name__ == "__main__":
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
    args = parser.parse_args()

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

    app.router.add_get("/", index)
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    app.router.add_patch("/api/update_login/{id}", update_login)
    app.router.add_patch("/api/update_warnings/{id}", update_warnings)
    app.router.add_patch("/api/update_terminate/{id}", update_terminate)
    app.router.add_get("/api/all_users", get_all_users)
    cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    )
