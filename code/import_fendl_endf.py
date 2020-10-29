############################################################
#
# Author:       Georg Schnabel
# Email:        g.schnabel@iaea.org
# Date:         2020/10/29
# Institution:  IAEA
#
# This script reads the ENDF files from the FENDL
# library and copies them to a repository folder
# changing the hierarchical structure of the
# directories for compliance with YODA principles [1].
#
# Usage:
#     python import_endf.py <inp-dir> <out-dir>
#
#     <inp-dir>: path to data directory of FENDL library
#     <out-dir>: path to data directory of FENDL repository
#
# NOTE:
#     This script in its current form is not useful
#     to persons outside the IAEA because of the lack
#     of access to the FENDL library directory.
#     It is provided to increase traceability as it
#     can be seen, e.g., which files were excluded
#     and how the migration process worked in general.
#
# [1]: https://handbook.datalad.org/en/latest/basics/101-127-yoda.html 
#
############################################################

import os
import sys
import shutil
from utils.endf_metadata import is_endf_file


def main():
    
    if (len(sys.argv) < 3):
        raise ValueError
    
    inpdir = os.path.normpath(sys.argv[1])
    outdir = os.path.normpath(sys.argv[2])

    if inpdir == outdir:
        print('input and output directory cannot be the same')
        raise ValueError
    
    # store tuples of source and destionation paths
    copy_log = []

    ##################################################
    #  copy general purpose endf files to repository
    ##################################################
    
    gp_lib_outdir = os.path.join(outdir, 'general-purpose') 
    
    # define the libraries
    gp_libs = ['atom', 'neutron', 'proton', 'deuteron', 'neutron-shadow']
    
    # define where the ENDF files of the libraries are located
    gp_lib_inpdirs = {os.path.join(inpdir, k, 'endf'): k for k in gp_libs} 
    
    # define to which directories the ENDF files in the input
    # directory should be copied
    gp_lib_outdirs = {k: os.path.join(gp_lib_outdir, v)
                      for k, v in gp_lib_inpdirs.items()}
    
    # check that all required input directories are available
    check_if_dirs_exist(gp_lib_inpdirs)
    # clean existing output directories
    shutil.rmtree(gp_lib_outdir, ignore_errors=True)

    # create the output directories
    os.mkdir(gp_lib_outdir)
    for k, curpath in gp_lib_outdirs.items():
        os.mkdir(curpath)
    
    # traverse input dirs and transfer endf files
    # to output directories in repository
    for cur_inpdir, cur_outdir in gp_lib_outdirs.items():
        files = []
        for curfile in os.listdir(cur_inpdir):
            fpath = os.path.join(cur_inpdir, curfile)
            # skip directories
            if not os.path.isfile(fpath):
                continue
            # skip files that are known not to
            # be endf files
            if curfile in ['index.html',
                           'n_1925_19-K-39_.endf', 'n_1925_19-K-39_.txt',
                           'n_1928_19-K-40_.endf', 'n_1928_19-K-40_.txt',
                           'n_1931_19-K-41_.endf', 'n_1931_19-K-41_.txt']:
                continue

            if not is_endf_file(fpath):
                raise ValueError
            # copy the endf file to the appropriate location
            # in the destination repository
            fname_out = os.path.splitext(curfile)[0] + '.endf'
            fpath_out = os.path.join(cur_outdir, fname_out)
            print('copying ' + fpath + ' to ' + fpath_out)
            copy_log.append((os.path.relpath(fpath, start=inpdir),
                             os.path.relpath(fpath_out, start=outdir)))
            shutil.copy(fpath, fpath_out)

            
    ##################################################
    #  copy activation files to repository
    ##################################################
    
    activ_lib_outdir = os.path.join(outdir, 'activation') 
    activ_libs = ['neutron-activ', 'proton-activ',
                  'deuteron-activ', 'deuteron-activ-renorm']
    
    # define where the ENDF files of the libraries are located
    activ_lib_inpdirs = {}
    activ_lib_outdirs = {}
    for curlib in activ_libs:
        # for neutrons we have a endf file
        # so we don't read the derived gendf, pendf files, etc.
        # they will be stored in an additional super-dataset
        if curlib == 'neutron-activ':
            curinpdir = os.path.join(inpdir, curlib, 'endf')
            activ_lib_inpdirs.update({
                curinpdir: curlib
            })
            activ_lib_outdirs.update({
                curinpdir: os.path.join(activ_lib_outdir, curlib)  
            })
        # for the other activation files, we only have 
        # gendf and pendf files so we include them 
        else:
            basedirs = ('gendf', 'pendf')
            curinpdirs = {k: os.path.join(inpdir, curlib, k)
                          for k in basedirs}
            activ_lib_inpdirs.update({
                v: curlib for k, v in curinpdirs.items()
            })
            activ_lib_outdirs.update({
                v: os.path.join(activ_lib_outdir, curlib, k)
                for k, v in curinpdirs.items()
            })

    # check that all required input directories are available
    check_if_dirs_exist(activ_lib_inpdirs)
    # clean existing output directories
    shutil.rmtree(activ_lib_outdir, ignore_errors=True)

    # create the output directories
    os.mkdir(activ_lib_outdir)
    for k, curpath in activ_lib_outdirs.items():
        os.makedirs(curpath)
    
    # traverse input dirs and transfer endf files
    # to output directories in repository
    problematic_files = []
    for cur_inpdir, cur_outdir in activ_lib_outdirs.items():
        files = []
        for curfile in os.listdir(cur_inpdir):
            fpath = os.path.join(cur_inpdir, curfile)
            # skip directories
            if not os.path.isfile(fpath):
                continue
            # skip files that are known not to
            # be endf files
            if curfile in []:
                raise ValueError
            if not is_endf_file(fpath):
                problematic_files.append(os.path.relpath(fpath, start=inpdir))
                print('The file at ' + fpath + ' is not a valid ENDF file')
                continue
            # copy the endf file to the appropriate location
            # in the destination repository
            fname_out = os.path.splitext(curfile)[0] + '.endf'
            fpath_out = os.path.join(cur_outdir, fname_out)
            print('copying ' + fpath + ' to ' + fpath_out)
            copy_log.append((os.path.relpath(fpath, start=inpdir),
                             os.path.relpath(fpath_out, start=outdir)))
            shutil.copy(fpath, fpath_out)

    # record files that have been copied
    copy_log_header = [
        '# The first path is the location of the source',
        '# file given as path relative to the root of the FENDL',
        '# library path exposed to the public on the IAEA-NDS website.',
        '# The second path (after a tabulator) is the',
        '# destination of the file in the repository.'
    ]
    copy_log_body = [x[0] + '\t' + x[1] for x in copy_log]
    copy_log_content = copy_log_header + copy_log_body

    copy_log_fpath = os.path.join(outdir, 'copy_log.txt')
    with open(copy_log_fpath, 'w+') as f:
        f.write('\n'.join(copy_log_content))
    
    # record files that had problems

    problem_header = [
        '# The following files were not included',
        '# in the repository because they are not',
        '# valid ENDF files. Usually these files',
        '# do not have any content'
    ]
    problem_file_content = problem_header + problematic_files
    problem_fpath = os.path.join(activ_lib_outdir, 'excluded_files.txt')
    with open(problem_fpath, 'w+') as f:
        f.write('\n'.join(problem_file_content))

    print('########## COPYING COMPLETED ##########')
    print()
    print('The following files are not ENDF files and were not copied:')
    for curfile in problematic_files:
        print('Not an ENDF file: ' + curfile)
    print()
    print('Number of problematic files: ' + str(len(problematic_files)))


##################################################
#  useful utility functions
##################################################

def check_if_dirs_exist(dirs):
    """Check if the directories given as iterable exist"""
    for curpath in dirs:
        if not os.path.isdir(curpath):
            print('The path ' + curpath + ' does not exist')
            raise ValueError


##################################################
#  start up
##################################################

if __name__ == '__main__':
    main()
