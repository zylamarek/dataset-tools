import numpy as np
from PIL import Image

from .filter import Filter


class Duplicate(Filter):
    def __init__(self, eps=0.003, *args, **kwargs):
        super(Duplicate, self).__init__(*args, **kwargs)
        self.eps = eps

    def apply_single(self, img):
        diff = lambda x, y: (np.sqrt(np.sum(np.power(np.asarray(x) - np.asarray(y), 2))) / np.prod(x.size))
        for i, path, img_out in self.data_out:
            img_in = Image.fromarray(img, mode='RGB')
            # img_in = img.copy()
            img_out = Image.fromarray(img_out, mode='RGB')
            if np.prod(img_in.size) > np.prod(img_out.size):
                img_in = img_in.resize(img_out.size)
            else:
                img_out = img_out.resize(img_in.size)
            # print(diff(img_out, img_in))
            if diff(img_out, img_in) < self.eps:
                return False
        return True
