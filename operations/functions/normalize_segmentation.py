from PIL import Image
import numpy as np

from .function import Function


class NormalizeSegmentation(Function):
    def __init__(self, n_categories, *args, **kwargs):
        self.n_categories = int(n_categories)
        super(NormalizeSegmentation, self).__init__(do_analysis=False, *args, **kwargs)

    def apply_single(self, img, path, meta):
        image = Image.fromarray(img, mode='RGB')
        new_image = Image.eval(image, lambda x: x / (self.n_categories - 1.) * 255)
        img = np.asarray(new_image)
        return img

    def name(self):
        return super(NormalizeSegmentation, self).name() + ('_%d' % self.n_categories)
