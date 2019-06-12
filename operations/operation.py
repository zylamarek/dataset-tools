from dataset import Dataset


class Operation:
    def __init__(self, path_in, prepend_name=''):
        self.prepend_name = prepend_name

        if path_in[-1] == '/' or path_in[-1] == '\\':
            path_in = path_in[:-1]
        self.path_in = path_in
        self.data_in = Dataset(path_in)
        self.path_out = self.path_in + '_' + self.name()
        self.data_out = Dataset(self.path_out)

    def name(self):
        return self.prepend_name + self.__class__.__name__

    def apply(self):
        raise NotImplementedError

    def apply_single(self, img):
        raise NotImplementedError
