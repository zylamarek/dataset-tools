from PIL import Image
import numpy as np

from .function import Function


class Resize(Function):
    def __init__(self, size, *args, **kwargs):
        self.size = int(size)
        super(Resize, self).__init__(*args, **kwargs)

    def apply_single(self, img):
        image = Image.fromarray(img)
        w, h = image.size
        scale_ratio = min(self.size / w, self.size / h)
        image = image.resize((int(w * scale_ratio), int(h * scale_ratio)), Image.ANTIALIAS)
        w, h = image.size
        new_image = Image.new('RGB', (self.size, self.size), (255, 255, 255))
        new_image.paste(image, ((self.size - w) // 2, (self.size - h) // 2))
        img = np.asarray(new_image)
        return img

    def name(self):
        return super(Resize, self).name() + ('_%d' % self.size)
