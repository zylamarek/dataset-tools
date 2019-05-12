import face_recognition

from .filter import Filter


class FaceDetection(Filter):
    def apply_single(self, img):
        boxes = face_recognition.face_locations(img, model='hog')
        return bool(boxes)
