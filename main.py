import argparse

import operations.filters
import operations.functions
import utils

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sequence', action='store_true', help='treat data as a sequence')
parser.add_argument('path_in', type=str)
parser.add_argument('operations', type=str, nargs='+',
                    help='filters %s and functions %s to apply' % \
                         (str(operations.filters.__all__), str(operations.functions.__all__)))
args = parser.parse_args()

path_in = args.path_in
is_sequence = args.sequence

op_stack = [(i,) + utils.interpret_op(operation_txt) for i, operation_txt in enumerate(args.operations)]
print('Interpreted op stack:')
print(' -> '.join(['%d_%s(' % (i, operation_name) + ','.join(args) + ')'
                   for i, operation_name, args in op_stack]))

for i_operation, operation_name, args in op_stack:
    operation = getattr(operations, operation_name)(*args, path_in=path_in, prepend_name='%d_' % i_operation,
                                                    is_sequence=is_sequence)
    operation.apply()
    path_in = operation.path_out
