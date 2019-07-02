import face_recognition

from .function import Function


class CropFaceException(Exception):
    pass


class CropFace(Function):
    def __init__(self, margin=0, *args, **kwargs):
        self.margin = int(margin)
        super(CropFace, self).__init__(do_analysis=True, *args, **kwargs)

    def analyze_single(self, img):
        boxes = face_recognition.face_locations(img, model='hog')
        if not boxes:
            raise CropFaceException('No face detected')
        return boxes[0]

    def apply_single(self, img, meta):
        if meta is None:
            raise CropFaceException('No face detected')
        return img[max(0, meta[0] - self.margin):meta[2] + 1 + self.margin,
               max(0, meta[3] - self.margin):meta[1] + 1 + self.margin]

    def name(self):
        return super(CropFace, self).name() + ('_%d' % self.margin)
