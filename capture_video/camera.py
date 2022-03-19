import threading
import cv2
import torch
from video_stream.settings import BASE_DIR

model = torch.hub.load(f'{BASE_DIR}/yolov5', 'custom',
                               path=f'{BASE_DIR}/model_yolo/best.pt',
                               source='local')  # YOLOv5 model loading
model.conf = 0.40  # set minimum confidence 33 %
model.iou = 0.45
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()


    def __del__(self):
        self.video.release()

    def get_frame(self):
        img = self.frame
        # img = cv2.resize(image, (1280, 1280))  # resizing image into 640*640
        results = model(img, size=640)  # passing the image into model
        results.render()
        # img = cv2.resize(img, (480, 480))
        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


