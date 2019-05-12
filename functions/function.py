from tqdm import tqdm

from dataset import Dataset


class Function:
    def __init__(self, path_in, size):
        self.size = size
        if path_in[-1] == '/' or path_in[-1] == '\\':
            path_in = path_in[:-1]
        self.path_in = path_in
        self.data_in = Dataset(path_in)
        self.path_out = self.path_in + ('_%d' % self.size)
        self.data_out = Dataset(self.path_out)

    def apply(self):
        for i, path, img in tqdm(self.data_in):
            try:
                img_out = self.apply_single(img)
                self.data_out.add_by_img(img_out)
            except Exception as e:
                print('Exception while applying %s: %d, %s' % (self.name(), i, path))
                print(str(e))

    def name(self):
        return self.__class__.__name__

    def apply_single(self, img):
        # returns changed image as numpy array
        raise NotImplementedError
