import asyncio
import logging
from signal import SIGINT, SIGTERM
import cv2
from flask import Response
import numpy as np
import requests

import livekit

from object_detection import ObjectDetectionWrapper

URL = "0.0.0.0:7880"  # hardcoded livekit server
MONITORING_STUDENT_ID = (
    999  # set the id to 999 as we need to create a token to join room
)

tasks = set()


async def frame_loop(video_stream: livekit.VideoStream) -> None:
    argb_frame = None
    cv2.namedWindow("livekit_video", cv2.WINDOW_AUTOSIZE)
    cv2.startWindowThread()
    async for frame in video_stream:
        buffer = frame.buffer

        if (
            argb_frame is None
            or argb_frame.width != buffer.width
            or argb_frame.height != buffer.height
        ):
            argb_frame = livekit.ArgbFrame(
                livekit.VideoFormatType.FORMAT_ABGR, buffer.width, buffer.height
            )

        buffer.to_argb(argb_frame)

        arr = np.ctypeslib.as_array(argb_frame.data)
        arr = arr.reshape((argb_frame.height, argb_frame.width, 4))
        arr = cv2.cvtColor(arr, cv2.COLOR_RGBA2RGB)

        detection_result = ObjectDetectionWrapper.detectFrameByFrame(arr)

        arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

        cv2.imshow("livekit_video", arr)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


async def main(room: livekit.Room) -> None:
    video_stream = None

    @room.on("track_subscribed")
    def on_track_subscribed(track: livekit.Track, *_):
        print("Track subscribed!")
        if track.kind == livekit.TrackKind.KIND_VIDEO:
            nonlocal video_stream
            if video_stream is not None:
                # only process the first stream received
                return

            print("subscribed to track: " + track.name)
            video_stream = livekit.VideoStream(track)
            task = asyncio.create_task(frame_loop(video_stream))
            tasks.add(task)
            task.add_done_callback(tasks.remove)

    response: Response = await requests.request(
        "GET", f"http://localhost:8080/api/get_student_token/{MONITORING_STUDENT_ID}"
    )

    await room.connect(URL, response.token)
    print("connected to room: " + room.name)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.FileHandler("basic_room.log"), logging.StreamHandler()],
    )

    loop = asyncio.get_event_loop()
    room = livekit.Room(loop=loop)

    async def cleanup():
        await room.disconnect()
        loop.stop()

    asyncio.ensure_future(main(room))
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, lambda: asyncio.ensure_future(cleanup()))

    try:
        loop.run_forever()
    finally:
        loop.close()
