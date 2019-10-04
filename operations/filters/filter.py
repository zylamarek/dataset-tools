from tqdm import tqdm
import os

from dataset import Dataset
from operations.operation import Operation


class Filter(Operation):
    def __init__(self, cache_out=False, *args, **kwargs):
        super(Filter, self).__init__(cache_out=cache_out, *args, **kwargs)

        self.path_out_not_passed = self.path_out + '_not_passed'
        self.data_out_not_passed = Dataset(self.path_out_not_passed, cache=cache_out)

    def apply(self):
        for i, path, img in tqdm(self.data_in, desc=self.name()):
            try:
                if self.apply_single(img):
                    if self.keep_filenames:
                        self.data_out.add_by_path(path, filename=os.path.basename(path))
                    else:
                        self.data_out.add_by_path(path)
                else:
                    if self.keep_filenames:
                        self.data_out_not_passed.add_by_path(path, filename=os.path.basename(path))
                    else:
                        self.data_out_not_passed.add_by_path(path)
            except Exception as e:
                print('Exception while filtering: %d, %s' % (i, path))
                print(str(e))
        self.show_stats()

    def show_stats(self):
        try:
            ratio_passed = self.data_out.n / self.data_in.n * 100
        except ZeroDivisionError:
            ratio_passed = 0.
        print('%s: %d out of %d passed through (%.2f%%)' % (self.name(), self.data_out.n, self.data_in.n, ratio_passed))

    def apply_single(self, img):
        # returns True if the image passes the filter
        raise NotImplementedError
