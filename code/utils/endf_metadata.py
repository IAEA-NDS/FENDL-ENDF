from .fortran_utils import fort_read as fr


def is_endf_file(fpath):
    """Determines whether file is a valid ENDF file"""
    with open(fpath, 'r', errors='ignore') as f:
        lines = f.readlines(80*10)
        for curline in lines:
            if curline[70:75] == ' 1451':
                return True
    return False


def get_endf_metadata(fpath):
    """Extract the metadata from an ENDF file"""
    with open(fpath, 'r', errors='ignore') as f:
        header = f.readlines(10000)
    meta_dic = None
    for nr, curline in enumerate(header):
        if curline[70:75] == ' 1451':
            fmt = r'(2E11.6,4I11)'
            meta_dic = {}
            mu = meta_dic.update
            mu(fr(header[nr],   fmt,
                varnames = ['ZA','AWR','LRP','LFI','NLIB','NMOD']))
            mu(fr(header[nr+1], fmt,
                varnames=['ELIS', 'STA', 'LIS', 'LIS0', '_', 'NFOR']))
            mu(fr(header[nr+2], fmt,
                varnames=['AWI', 'EMAX', 'LREL', '_', 'NSUB', 'NVER']))
            mu(fr(header[nr+3], fmt,
                varnames=['TEMP', '_', 'LDRV', '_', 'NWD', 'NXC']))
            mu(fr(header[nr+4], r'(2A11,A10,1X,A33)',
                varnames=['ZSYMAM', 'ALAB', 'EDATE', 'AUTH']))
            mu(fr(header[nr+5], r'(1X,A21,A10,1X,A10,12X,A8)',
                varnames=['REF', 'DDATE', 'RDATE', 'ENDATE']))
            mu(fr(header[nr+6], r'(4X,A18,A22,A11)',
                varnames=['HSUB_LIB', 'HSUB_MAT', 'HSUB_IREV']))
            mu(fr(header[nr+7], r'5X,A61',
                varnames=['HSUB_SUBLIB']))
            mu(fr(header[nr+8], r'6X,A60',
                varnames=['HSUB_NFOR']))

            meta_dic.pop('_', None)
            # strip away blanks from beginning and end of fields with strings
            for k, v in meta_dic.items():
                if isinstance(v, str):
                    meta_dic[k] = v.strip()
            # some other conversions
            meta_dic['ZA'] = int(meta_dic['ZA'])
            meta_dic['ZSYMAM'] = meta_dic['ZSYMAM'].replace(' ', '')
            return meta_dic

    return None
