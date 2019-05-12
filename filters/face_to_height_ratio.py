import face_recognition
import numpy as np
import matplotlib.pyplot as plt

from .filter import Filter


class FaceToHeightRatio(Filter):
    def __init__(self, required_ratio=0.136, eps=0.04, show_histogram=True, *args, **kwargs):
        super(FaceToHeightRatio, self).__init__(*args, **kwargs)
        self.ratios = []
        self.eps = eps
        self.required_ratio = required_ratio
        self.show_histogram = show_histogram
        self.n_no_faces = 0

    def apply_single(self, img):
        boxes = face_recognition.face_locations(img, model='hog')
        if not boxes:
            self.n_no_faces += 1
            return False
        box = boxes[0]
        ratio = (box[2] - box[0]) / img.shape[0]
        self.ratios.append(ratio)
        return np.abs(ratio - self.required_ratio) <= self.eps

    def stats(self):
        super(FaceToHeightRatio, self).stats()
        print('# no faces: %d' % self.n_no_faces)
        print('Mean ratio: %.3f' % np.mean(self.ratios))
        if self.show_histogram:
            plt.hist(x=self.ratios, bins=50)
            plt.show()
