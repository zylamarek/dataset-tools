from PIL import Image

from .function import Function
from utils import FaceAlignerSplit, fix_meta_sequence_kalman
import utils.frederic_context
from frederic.predictor import Predictor
from frederic.utils.general import L_EYE_LEFT, L_EYE_RIGHT
from frederic.utils.image import load_landmarks


class AlignFaceException(Exception):
    pass


class AlignCatFace(Function):
    def __init__(self, desired_face_width=256, desired_face_height=None, *args, **kwargs):
        self.desired_face_width = int(desired_face_width)
        if desired_face_height is None:
            desired_face_height = desired_face_width
        self.desired_face_height = int(desired_face_height)

        self.predictor = Predictor()
        self.face_aligner = FaceAlignerSplit(self.predictor, desiredLeftEye=(0.32, 0.3),
                                             desiredFaceWidth=self.desired_face_width,
                                             desiredFaceHeight=self.desired_face_height)
        super(AlignCatFace, self).__init__(do_analysis=True, *args, **kwargs)

    def fix_meta_sequence(self, metas):
        return fix_meta_sequence_kalman(metas)

    def analyze_single(self, img, path):
        try:
            landmarks = load_landmarks(path + '.cat')
        except FileNotFoundError:
            img_ = Image.fromarray(img, mode='RGB')
            landmarks = self.predictor.predict(img_)
            self.predictor.save_landmarks(landmarks, path + '.cat')

        eyes = landmarks[L_EYE_RIGHT:L_EYE_LEFT + 1]

        M = self.face_aligner.analyze(eyes)
        return M

    def apply_single(self, img, path, meta=None):
        return self.face_aligner.apply(img, meta)

    def name(self):
        return super(AlignCatFace, self).name() + ('_%dx%d' % (self.desired_face_width, self.desired_face_height))
