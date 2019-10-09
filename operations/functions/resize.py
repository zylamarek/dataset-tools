from PIL import Image
import numpy as np

from .function import Function


class Resize(Function):
    """
    Resize function keeps the aspect ratio of the image. Adds white borders (full mode)
    or crops the image (fill mode). You may drop the height parameter to get a square
    image.

    """

    def __init__(self, width, height=None, mode='full', *args, **kwargs):
        self.width = int(width)

        if height is None:
            height = self.width
        self.height = int(height)

        if mode not in ('fill', 'full'):
            raise Exception('Unknown mode. Mode must be either "full" or "fill".')
        self.mode = mode

        super(Resize, self).__init__(do_analysis=False, *args, **kwargs)

    def apply_single(self, img, path, meta):
        image = Image.fromarray(img)

        w, h = image.size
        if self.mode == 'full':
            scale_ratio = min(self.width / w, self.height / h)
        else:
            scale_ratio = max(self.width / w, self.height / h)
        image = image.resize((int(w * scale_ratio), int(h * scale_ratio)), Image.ANTIALIAS)

        w, h = image.size
        new_image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        new_image.paste(image, ((self.width - w) // 2, (self.height - h) // 2))

        img = np.asarray(new_image)
        return img

    def name(self):
        return super(Resize, self).name() + ('_%dx%d_%s' % (self.width, self.height, self.mode))
