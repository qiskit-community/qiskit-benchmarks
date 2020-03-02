from ddt import data, unpack
from itertools import product


class Case(dict):
    """ A test case, see https://ddt.readthedocs.io/en/latest/example.html MyList."""
    pass


def generate_cases(dsc=None, name=None, **kwargs):
    """Combines kwargs in cartesian product and creates Case with them"""
    ret = []
    keys = kwargs.keys()
    vals = kwargs.values()
    for values in product(*vals):
        case = Case(zip(keys, values))
        if dsc is not None:
            setattr(case, "__doc__", dsc.format(**case))
        if name is not None:
            setattr(case, "__name__", name.format(**case))
        ret.append(case)
    return ret


def combine(**kwargs):
    """Decorator to create combinations and tests
        @combine(level=[0, 1, 2, 3],
                 circuit=[a, b, c, d],
                 dsc='Test circuit {circuit.__name__} with level {level}',
                 name='{circuit.__name__}_level{level}')
    """

    def deco(func):
        return data(*generate_cases(**kwargs))(unpack(func))

    return deco
