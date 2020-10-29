from fortranformat import FortranRecordReader, FortranRecordWriter
from .generic_utils import flatten, static_vars


@static_vars(frr_cache={})
def fort_read(fobj, formatstr, none_as=None, varnames=None, debug=False):
    """Read from a file or string using a format descriptor

    Keyword arguments:
    fobj      -- file object or string to read from
    formatstr -- the Fortran format description string
    none_as   -- conversion of None resulting from incomplete reads
    varnames  -- a list with variable names used as keys in the resulting
                 dictionary that contains the values read.
                 If None, return the values read as a list
    debug     -- print extra information on stdout for debugging purposes
    """
    if formatstr not in fort_read.frr_cache:
        fort_read.frr_cache[formatstr] = FortranRecordReader(formatstr) 
    frr = fort_read.frr_cache[formatstr]

    if not isinstance(fobj, str):
        fname = fobj.name
        inpline = fobj.readline()
    else:
        fname = 'console'
        inpline = fobj

    res = frr.read(inpline)
    if none_as is not None:
        res = [none_as if x is None else x for x in res]

    if varnames:
        res = {k: res[i] for i, k in enumerate(varnames)}

    if debug:
        print('--- reading ---')
        print('file: ' + fname)
        print('fmt: ' + formatstr)
        print('str: ' + inpline)

    return res


@static_vars(frw_cache={})
def fort_write(fobj, formatstr, values, debug=False):
    """Write values to a file in a specified Fortran format.

    Keyword arguments:
    fobj      -- file object for output
    formatstr -- the Fortran format description string
    values    -- values given in a (potentially nested) list
    debug     -- print extra information for debugging purposes
    """
    vals = list(flatten(values))
    vals = [v for v in vals if v is not None]
    if debug:
        print('--- writing ---')
        try:
            print('file: ' + fobj.name)
        except AttributeError:
            print('file: console')
        print('fmt: ' + formatstr)
        print('values: ')
        print(vals)

    if formatstr not in fort_write.frw_cache:
        fort_write.frw_cache[formatstr] = FortranRecordWriter(formatstr)
    frw = fort_write.frw_cache[formatstr]

    line = frw.write(vals)
    if fobj is None:
        print(line)
    else:
        fobj.write(line + '\n')


def fort_range(*args):
    """Specify a range Fortran style.

    For instance, fort_range(1,3) equals range(1,4).
    """
    if len(args) == 2:
        return range(args[0], args[1]+1)
    elif len(args) == 3:
        return range(args[0], args[1]+1, args[2])
    else:
        raise IndexError
