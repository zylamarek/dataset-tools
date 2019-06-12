import face_recognition

from .function import Function


class CropFaceException(Exception):
    pass


class CropFace(Function):
    def apply_single(self, img):
        boxes = face_recognition.face_locations(img, model='hog')
        if not boxes:
            raise CropFaceException('No face detected')
        box = boxes[0]
        return img[box[0]:box[2] + 1, box[3]:box[1] + 1]
