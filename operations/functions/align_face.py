from imutils.face_utils import FaceAligner
from PIL import Image
import numpy as np

from .function import Function
from utils import predictor_setup


class AlignFaceException(Exception):
    pass


class AlignFace(Function):
    def __init__(self, desired_face_width=256, desired_face_height=None, *args, **kwargs):
        self.desired_face_width = int(desired_face_width)
        if desired_face_height is None:
            desired_face_height = desired_face_width
        self.desired_face_height = int(desired_face_height)

        self.detector, self.predictor = predictor_setup()
        self.face_aligner = FaceAligner(self.predictor, desiredLeftEye=(0.3, 0.35))
        super(AlignFace, self).__init__(*args, **kwargs)

    def apply_single(self, img):
        gray = np.asarray(Image.fromarray(img, mode='RGB').convert('L'))
        boxes = self.detector(img)
        if not boxes:
            raise AlignFaceException('No face detected')
        return self.face_aligner.align(img, gray, boxes[0])

    def name(self):
        return super(AlignFace, self).name() + ('_%dx%d' % (self.desired_face_width, self.desired_face_height))
