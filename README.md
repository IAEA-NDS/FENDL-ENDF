# Fusion Evaluated Nuclear Data Library

This repository keeps track of updates to the
Fusion Evaluated Nuclear Data Library (FENDL)
whose different versions are published on the
IAEA-NDS website at <https://www-nds.iaea.org/fendl/>.

The ENDF files of FENDL-3.1d and earlier versions recorded
here are exactly those published at the IAEA-NDS website.
The ENDF files associated with FENDL-3.2 in this
repository have still to undergo a rigorous quality
assurance procedure.

Please note that the ENDF files are not stored directly
in this repository but rather as links that can be consumed
by `git-annex` which is a tool to leverage the version
tracking functionality of `git` for large files.

If you want to download all or a subset of the ENDF files
in this repository, you have three options:

1. Install the command line tool `git-annex` to download the files from this repository
2. Download the ENDF files as zip-files from the derived repository FENDL-ENDF-EXT
3. Visit the [FENDL website](https://www-nds.iaea.org/fendl/)
   and download the files from there
 
### Interacting with this repository using git-annex

The command line tool [git-annex](https://git-annex.branchable.com/) offers
the functionality to store large files only as symbolic links in `git`.
`git-annex` is used to replace these links by the files themselves whenever
they are required.

Installation instructions for git-annex are provided [here](https://git-annex.branchable.com/install/).
In order to have an up-to-date version, we recommend installing git-annex via 
the [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda
Python distribution.
If Miniconda is installed, git-annex can be installed on the command line like so:
```
    conda install -c conda-forge git-annex
```

After the successful installation, you can use git and git-annex to download 
ENDF files of interest. The following instructions perform the download of
all ENDF files in this repository:
```
    git clone https://github.com/IAEA-NDS/FENDL-ENDF.git
    cd FENDL-ENDF
    git annex init
    git annex get .
```
