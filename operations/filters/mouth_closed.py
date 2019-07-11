from imutils.face_utils.helpers import FACIAL_LANDMARKS_68_IDXS
from imutils.face_utils.helpers import shape_to_np
import numpy as np
from PIL import Image

from .filter import Filter
from utils import predictor_setup


class MouthClosedException(Exception):
    pass


class MouthClosed(Filter):
    def __init__(self, eps=0.03, *args, **kwargs):
        self.eps = float(eps)
        self.detector, self.predictor = predictor_setup()
        super(MouthClosed, self).__init__(*args, **kwargs)

    def apply_single(self, img):
        boxes = self.detector(img)
        if not boxes:
            raise MouthClosedException('No face detected')

        gray = np.asarray(Image.fromarray(img, mode='RGB').convert('L'))
        shape = self.predictor(gray, boxes[0])
        shape = shape_to_np(shape)

        right_eye_start = FACIAL_LANDMARKS_68_IDXS["right_eye"][0]
        left_eye_end = FACIAL_LANDMARKS_68_IDXS["left_eye"][1]
        mouth_start, mouth_end = FACIAL_LANDMARKS_68_IDXS["mouth"]

        eyes_pts = shape[right_eye_start:left_eye_end]
        mouth_pts = shape[mouth_start:mouth_end]
        upper_lip_pts = shape[61:64]
        lower_lip_pts = shape[65:68]

        eyes_center = eyes_pts.mean(axis=0)
        mouth_center = mouth_pts.mean(axis=0)
        upper_lip_center = upper_lip_pts.mean(axis=0)
        lower_lip_center = lower_lip_pts.mean(axis=0)

        h = np.linalg.norm(eyes_center - mouth_center)
        d = np.linalg.norm(upper_lip_center - lower_lip_center)

        return bool((d / h) <= self.eps)

    def name(self):
        return super(MouthClosed, self).name() + ('_%.3f' % self.eps)
