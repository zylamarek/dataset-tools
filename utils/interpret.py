import re

import operations


class InterpreterException(Exception):
    pass


def interpret_op(txt):
    fn_match = re.match(r'(?P<op>\w+)\s?(?P<argl>\((?P<arg>(?P<args>[a-zA-Z0-9_.](,\s?)?)*)\))?', txt)
    if fn_match is None:
        raise InterpreterException('Could not interpret: %s' % txt)

    fn_dict = fn_match.groupdict()
    op = fn_dict['op']
    if fn_dict['arg'] is not None:
        args = [arg.strip() for arg in fn_dict['arg'].split(',') if arg.strip()]
    else:
        args = []

    operations_names = [operation_name.lower() for operation_name in operations.__all__]

    if op.lower() not in operations_names:
        raise InterpreterException('Unknown operation: %s' % op)

    return op, args
