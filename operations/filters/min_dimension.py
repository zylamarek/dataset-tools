from PIL import Image

from .filter import Filter


class MinDimension(Filter):
    def __init__(self, width, height=None, *args, **kwargs):
        self.width = int(width)

        if height is None:
            height = self.width
        self.height = int(height)
        super(MinDimension, self).__init__(*args, **kwargs)

    def apply_single(self, img):
        image = Image.fromarray(img)
        w, h = image.size
        return w >= self.width and h >= self.height

    def name(self):
        return super(MinDimension, self).name() + ('_%dx%d' % (self.width, self.height))
