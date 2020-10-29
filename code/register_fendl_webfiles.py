############################################################
#
# Author:       Georg Schnabel
# Email:        g.schnabel@iaea.org
# Date:         2020/11/04
# Institution:  IAEA
#
# This script takes the root url of a specific FENDL library version,
# a local directory containing the same ENDF files,
# as well as a text file containing tuples of file paths associations
# within these two directories.
# It registers all the website file as external special remote
# in git-annex.
#
# Usage:
#     python register_fendl_webfiles.py <website-url> <data-dir> <copy-log-file>
#
#     <website-url>:   website url to the FENDL library version
#     <data-dir>:      directory under git-annex control with ENDF files
#     <copy-log-file>: file containing the file associations between
#                      FENDL website and local directory
#
# Example:
#     python register_fendl_webfiles.py \
#        https://www-nds.iaea.org/fendl31/data/ \
#        ../data/ ../data/copy_log.txt
#
############################################################

import sys
import re
import subprocess

if len(sys.argv) != 4:
    raise ValueError('Expecting three arguments: <website-url> <data-dir> <copy-log-file>')

website_root = sys.argv[1]
data_dir = sys.argv[2]
copyfile = sys.argv[3]

# read the file associations
with open(copyfile, 'r') as f:
    lines = f.read().splitlines()
    lines = [l for l in lines if not re.match(r'^ *#', l)] 
    file_assoc = [tuple(l.split('\t')) for l in lines]


for cur_file_assoc in file_assoc:

    webfile = website_root + cur_file_assoc[0]
    datafile = data_dir + cur_file_assoc[1]

    print('\nAttaching remote source ' + webfile + ' to ' + datafile)
    subprocess.run(['git-annex', 'addurl', '--fast', '--file', datafile, webfile],
                   check=True)
