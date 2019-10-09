import os
from PIL import Image
import numpy as np
from shutil import copyfile


class Dataset:
    def __init__(self, path, random=False, cache=False):
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)

        self.files = [os.path.join(self.path, f) for f in os.listdir(self.path)
                      if os.path.isfile(os.path.join(self.path, f)) and not f.endswith('.cat')]
        self.n = len(self.files)

        if random:
            np.random.shuffle(self.files)

        self.cache = cache
        self.cached_imgs = []
        if cache:
            self.cached_imgs = [None] * self.n

        self.i = 0
        self.i_filename = 0

    def add_by_path(self, path, filename=None):
        if filename is None:
            filename = self.get_next_filename()
        path_out = os.path.join(self.path, filename)
        copyfile(path, path_out)
        self.files.append(path_out)
        self.n = len(self.files)
        self.cached_imgs.append(None)

    def add_by_img(self, img, filename=None):
        if filename is None:
            filename = self.get_next_filename()
        path_out = os.path.join(self.path, filename)
        Image.fromarray(img, mode='RGB').save(path_out)
        self.files.append(path_out)
        self.n = len(self.files)
        self.cached_imgs.append(None)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        path = self.files[self.i]
        if self.cache:
            if self.cached_imgs[self.i] is None:
                img = np.asarray(Image.open(path))
                self.cached_imgs[self.i] = img
            else:
                img = self.cached_imgs[self.i]
        else:
            img = np.asarray(Image.open(path))
        self.i += 1
        return self.i, path, img

    def get_next_filename(self):
        filename = '%05d.png' % self.i_filename
        while os.path.exists(os.path.join(self.path, filename)):
            if self.i_filename > 1e8:
                raise Exception('Too many iterations')
            self.i_filename += 1
            root, ext = os.path.splitext(filename)
            filename = '%05d%s' % (self.i_filename, ext)
        return filename

    def __len__(self):
        return self.n
