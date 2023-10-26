import cv2
from imageai.Detection import VideoObjectDetection, ObjectDetection
import os


class ObjectDetectionWrapper:
    def __init__(
        self,
        student_id,
        model_path=os.path.join(os.getcwd(), "tiny-yolov3.pt"),
        output_path=os.path.join(os.getcwd(), "camera_detected_video"),
        frames_per_second=30,
        log_progress=True,
    ):
        self.model_path = model_path
        self.student_id = student_id
        self.output_path = output_path
        self.frames_per_second = frames_per_second
        self.log_progress = log_progress
        # self.filename = self.student_id + ".avi"
        self.frame_detector = ObjectDetection()
        self.frame_detector.setModelTypeAsTinyYOLOv3()
        self.frame_detector.setModelPath(self.model_path)
        self.frame_detector.loadModel()
        self.currentDetectedObjects = []

    def detectFromVideo(self):
        """
        This can process a whole video and detect objects in each frame.
        """

        video_path = self.video_detector.detectObjectsFromVideo(
            input_file_path=self.filename,
            frames_per_second=self.frames_per_second,
            log_progress=self.log_progress,
            save_detected_video=True,
            per_frame_function=self.forFrame,
            minimum_percentage_probability=30,
        )
        return video_path

    def detectFrameByFrame(self, frame):
        """
        This can process a single frame and detect objects in that frame.
        """
        custom_objects = self.frame_detector.CustomObjects(cell_phone=True, laptop=True)
        detections = self.frame_detector.detectObjectsFromImage(
            custom_objects=custom_objects,
            input_image=frame,
            output_type="array",
        )
        self.currentDetectedObjects = detections
        return detections[1]

    def forFrame(frame_number, output_array, output_count):
        print("FOR FRAME ", frame_number)
        print("Output for each object : ", output_array)
        print("Output count for unique objects : ", output_count)
        print("------------END OF A FRAME --------------")
