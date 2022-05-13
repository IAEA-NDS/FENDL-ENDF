# Fusion Evaluated Nuclear Data Library

This repository keeps track of updates to the
ENDF files of the Fusion Evaluated Nuclear Data Library (FENDL)
whose different versions are published on the
IAEA-NDS website at <https://www-nds.iaea.org/fendl/>.

Please note that the ENDF files are not directly stored
in this repository but rather symlinks to them. The targets
of the symlinks contain cryptographic hashes that can be
used to verify whether an ENDF file is indeed the correct
target of a symlink.

The command line tool
[git-annex](https://git-annex.branchable.com/) can be used
to download individually or in bulk current or previous
versions of ENDF files in this repository. For more information
on the data management, please
visit the [fendl-code](https://github.com/iaea-nds/fendl-code)
repository.

