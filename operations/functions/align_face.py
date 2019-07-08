from PIL import Image
import numpy as np
from pykalman import KalmanFilter

from .function import Function
from utils import predictor_setup, FaceAlignerSplit


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
        measurements = np.ma.asarray(np.zeros((len(metas), 6)))
        for i, meta in enumerate(metas):
            if meta is not None:
                measurements[i] = meta.flatten()
            else:
                measurements[i] = np.ma.masked

        means = np.mean(measurements, axis=0)
        vars = np.var(measurements, axis=0)
        measurements -= means
        measurements /= vars

        kf = KalmanFilter(n_dim_obs=6, n_dim_state=6,
                          observation_covariance=1e4 * np.eye(6),
                          transition_covariance=1e4 * np.eye(6),
                          em_vars=['initial_state_mean', 'initial_state_covariance'])
        kf = kf.em(measurements)

        smoothed, _ = kf.smooth(measurements)
        smoothed *= vars
        smoothed += means
        metas = [np.reshape(sm, (2, 3)) for sm in smoothed]

        return metas

    def analyze_single(self, img):
        boxes = self.detector(img)
        if not boxes:
            raise AlignFaceException('No face detected')
        gray = np.asarray(Image.fromarray(img, mode='RGB').convert('L'))
        M = self.face_aligner.analyze(gray, boxes[0])
        return M

    def apply_single(self, img, meta=None):
        if meta is None:
            raise AlignFaceException('No face detected')
        return self.face_aligner.apply(img, meta)

    def name(self):
        return super(AlignFace, self).name() + ('_%dx%d' % (self.desired_face_width, self.desired_face_height))
