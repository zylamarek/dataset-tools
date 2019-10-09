from tqdm import tqdm
import os

from operations.operation import Operation


class Function(Operation):
    def __init__(self, do_analysis, *args, **kwargs):
        self.do_analysis = do_analysis
        super(Function, self).__init__(*args, **kwargs)

    def apply(self):
        if self.do_analysis:
            metas = []
            for i, path, img in tqdm(self.data_in, desc=self.name() + ' analysis'):
                meta = None
                try:
                    meta = self.analyze_single(img, path)
                except Exception as e:
                    print('Exception while analyzing %s: %d, %s' % (self.name(), i, path))
                    print(str(e))
                metas.append(meta)

            if self.is_sequence:
                metas = self.fix_meta_sequence(metas)
        else:
            metas = [None] * self.data_in.n

        for (i, path, img), meta in tqdm(zip(self.data_in, metas), desc=self.name(), total=self.data_in.n):
            try:
                img_out = self.apply_single(img, path, meta)
                if self.keep_filenames:
                    self.data_out.add_by_img(img_out, filename=os.path.basename(path))
                else:
                    self.data_out.add_by_img(img_out)
            except Exception as e:
                print('Exception while applying %s: %d, %s' % (self.name(), i, path))
                print(str(e))

    def fix_meta_sequence(self, metas):
        prev_meta = None
        for i in range(len(metas)):
            if metas[i] is None:
                metas[i] = prev_meta
            prev_meta = metas[i]

        prev_meta = None
        for i in range(len(metas) - 1, -1, -1):
            if metas[i] is None:
                metas[i] = prev_meta
            prev_meta = metas[i]

        return metas

    def analyze_single(self, img, path):
        # extracts meta data from img for the function to be applied
        raise NotImplementedError

    def apply_single(self, img, path, meta):
        # applies a function to img using meta data and returns the result
        raise NotImplementedError
