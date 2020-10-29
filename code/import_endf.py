############################################################
#
# Author:       Georg Schnabel
# Email:        g.schnabel@iaea.org
# Date:         2020/10/29
# Institution:  IAEA
#
# This script takes an input directory with ENDF files
# and copies them to a destination directory.
# It makes sure that only valid ENDF files are copied
# and changes all file extensions to .endf
#
# Usage:
#     python import_endf.py <inp-dir> <out-dir>
#
#     <inp-dir>: path to data directory of FENDL library
#     <out-dir>: path to data directory of FENDL repository
#
############################################################

import os
import sys
import shutil
from utils.endf_metadata import is_endf_file


if (len(sys.argv) < 3):
    raise ValueError

inpdir = os.path.normpath(sys.argv[1])
outdir = os.path.normpath(sys.argv[2])

if inpdir == outdir:
    print('input and output directory cannot be the same')
    raise ValueError

files = []
for curfile in os.listdir(inpdir):
    fpath = os.path.join(inpdir, curfile)
    # skip directories
    if not os.path.isfile(fpath):
        continue
    if not is_endf_file(fpath):
        print(fpath + ' is not a valid ENDF file!')
        raise ValueError
    # copy the endf file to the appropriate location
    # in the destination repository
    fname_out = os.path.splitext(curfile)[0] + '.endf'
    fpath_out = os.path.join(outdir, fname_out)
    print('copying ' + fpath + ' to ' + fpath_out)
    if os.path.islink(fpath_out):
        os.unlink(fpath_out)
    shutil.copy(fpath, fpath_out, follow_symlinks=False)
