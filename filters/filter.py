from tqdm import tqdm

from dataset import Dataset


class Filter:
    def __init__(self, path_in, prepend_name='', include_failed=False):
        self.prepend_name = prepend_name
        if path_in[-1] == '/' or path_in[-1] == '\\':
            path_in = path_in[:-1]
        self.path_in = path_in
        self.data_in = Dataset(path_in)
        self.path_out = self.path_in + '_' + self.name()
        self.data_out = Dataset(self.path_out)

        self.include_failed = include_failed
        if include_failed:
            self.path_out_F = self.path_in + '_' + self.name() + '_F'
            self.data_out_F = Dataset(self.path_out_F)
        else:
            self.path_out_F = None
            self.data_out_F = None

    def apply(self):
        for i, path, img in tqdm(self.data_in):
            try:
                if self.apply_single(img):
                    self.data_out.add_by_path(path)
                else:
                    if self.include_failed:
                        self.data_out_F.add_by_path(path)
            except Exception as e:
                print('Exception while filtering: %d, %s' % (i, path))
                print(str(e))

    def stats(self):
        print('%s: %d out of %d passed through (%.2f%%)' % (self.name(), self.data_out.n, self.data_in.n,
                                                            self.data_out.n / self.data_in.n * 100))

    def name(self):
        return self.prepend_name + self.__class__.__name__

    def apply_single(self, img):
        # returns True if the image passes the filter
        raise NotImplementedError
