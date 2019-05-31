from tqdm import tqdm

from operations.operation import Operation


class Function(Operation):
    def apply(self):
        for i, path, img in tqdm(self.data_in, desc=self.name()):
            try:
                img_out = self.apply_single(img)
                self.data_out.add_by_img(img_out)
            except Exception as e:
                print('Exception while applying %s: %d, %s' % (self.name(), i, path))
                print(str(e))
