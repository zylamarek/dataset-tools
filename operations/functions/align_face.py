from PIL import Image
import numpy as np
from imutils.face_utils.helpers import shape_to_np, FACIAL_LANDMARKS_68_IDXS

from .function import Function
from utils import predictor_setup, FaceAlignerSplit, fix_meta_sequence_kalman


class AlignFaceException(Exception):
    pass


class AlignFace(Function):
    def __init__(self, desired_face_width=256, desired_face_height=None, *args, **kwargs):
        self.desired_face_width = int(desired_face_width)
        if desired_face_height is None:
            desired_face_height = desired_face_width
        self.desired_face_height = int(desired_face_height)

        self.detector, self.predictor = predictor_setup()
        self.face_aligner = FaceAlignerSplit(self.predictor, desiredLeftEye=(0.32, 0.3),
                                             desiredFaceWidth=self.desired_face_width,
                                             desiredFaceHeight=self.desired_face_height)
        super(AlignFace, self).__init__(do_analysis=True, *args, **kwargs)

    def fix_meta_sequence(self, metas):
        return fix_meta_sequence_kalman(metas)

    def analyze_single(self, img, path):
        boxes = self.detector(img)
        if not boxes:
            raise AlignFaceException('No face detected')

        gray = np.asarray(Image.fromarray(img, mode='RGB').convert('L'))
        shape = self.predictor(gray, boxes[0])
        shape = shape_to_np(shape)

        # extract the left and right eye (x, y)-coordinates
        (lStart, lEnd) = FACIAL_LANDMARKS_68_IDXS["left_eye"]
        (rStart, rEnd) = FACIAL_LANDMARKS_68_IDXS["right_eye"]
        leftEyePts = shape[lStart:lEnd]
        rightEyePts = shape[rStart:rEnd]

        # compute the center of mass for each eye
        leftEyeCenter = leftEyePts.mean(axis=0)
        rightEyeCenter = rightEyePts.mean(axis=0)

        M = self.face_aligner.analyze((rightEyeCenter, leftEyeCenter))
        return M

    def apply_single(self, img, path, meta=None):
        if meta is None:
            raise AlignFaceException('No face detected')
        return self.face_aligner.apply(img, meta)

    def name(self):
        return super(AlignFace, self).name() + ('_%dx%d' % (self.desired_face_width, self.desired_face_height))
