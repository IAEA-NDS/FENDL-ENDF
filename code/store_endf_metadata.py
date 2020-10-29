############################################################
#
# Author:       Georg Schnabel
# Email:        g.schnabel@iaea.org
# Date:         2020/10/31
# Institution:  IAEA
#
# This script searches for ENDF files in a given path and
# extracts the library information from the file, such
# as ZA, AWS, NLIB, etc. This information is then added
# as metadata via git-annex metadata. The search works
# recursively and descends into subdirectories.
#
# Usage:
#     python store_endf_metadata.py <data-dir>
#
#     <data-dir>: directory with ENDF files
#
############################################################import subprocess
import os
import sys
import subprocess
from utils.endf_metadata import get_endf_metadata

if (len(sys.argv) != 2):
    raise ValueError('Expecting one argument being the path to ENDF directory')

data_dir = os.path.normpath(sys.argv[1])
for root, dirs, files in os.walk(data_dir):
    for fname in files:
        fpath = os.path.join(root, fname)
        meta_dic = get_endf_metadata(fpath)
        # add the metadata to the annex
        if meta_dic is not None:
            print('adding metadata for ' + fpath)
            annex_args = ['-s{}={}'.format(k, v) for k, v in meta_dic.items()]
            annex_cmd = ['git-annex', 'metadata', fpath]
            annex_cmd.extend(annex_args)
            subprocess.run(annex_cmd)
