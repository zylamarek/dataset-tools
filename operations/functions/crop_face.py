import face_recognition

from .function import Function


class CropFaceException(Exception):
    pass


class CropFace(Function):
    def __init__(self, margin=0, *args, **kwargs):
        self.margin = int(margin)
        super(CropFace, self).__init__(*args, **kwargs)

    def apply_single(self, img):
        boxes = face_recognition.face_locations(img, model='hog')
        if not boxes:
            raise CropFaceException('No face detected')
        box = boxes[0]
        return img[max(0, box[0] - self.margin):box[2] + 1 + self.margin,
               max(0, box[3] - self.margin):box[1] + 1 + self.margin]

    def name(self):
        return super(CropFace, self).name() + ('_%d' % self.margin)
