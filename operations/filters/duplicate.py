import numpy as np
from PIL import Image

from .filter import Filter


class Duplicate(Filter):
    def __init__(self, eps=0.00001, *args, **kwargs):
        self.eps = float(eps)
        super(Duplicate, self).__init__(*args, **kwargs)

    def apply_single(self, img):
        if self.eps == 0.:
            for i, path, img_out in self.data_out:
                if np.array_equal(img, img_out):
                    return False
        else:
            for i, path, img_out in self.data_out:
                img_in = Image.fromarray(img, mode='RGB')
                img_out = Image.fromarray(img_out, mode='RGB')
                if np.prod(img_in.size) > np.prod(img_out.size):
                    img_in = img_in.resize(img_out.size)
                else:
                    img_out = img_out.resize(img_in.size)
                if self._diff(img_out, img_in) < self.eps:
                    return False
        return True

    def name(self):
        return super(Duplicate, self).name() + ('_%.5f' % self.eps)

    @staticmethod
    def _diff(x, y):
        return np.sum(np.square(np.asarray(x) - np.asarray(y))) / np.prod(x.size)
