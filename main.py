import argparse

import filters
import functions

parser = argparse.ArgumentParser()
parser.add_argument('--path_in', type=str)
parser.add_argument('--filter', type=str, nargs='+', choices=filters.__all__,
                    help='filters to apply')
parser.add_argument('--resize', type=int)
args = parser.parse_args()

path_in = args.path_in

if args.filter is not None:
    for i_filter, filter_name in enumerate(args.filter):
        filter = getattr(filters, filter_name)(path_in=path_in, prepend_name='%d_' % i_filter,
                                               include_failed=True)
        filter.apply()
        filter.stats()
        path_in = filter.path_out

if args.resize is not None:
    func = functions.Resize(path_in=path_in, size=args.resize)
    func.apply()
