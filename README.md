# Fusion Evaluated Nuclear Data Library

This repository keeps track of updates to the
ENDF files of the Fusion Evaluated Nuclear Data Library (FENDL)
whose different versions are published on the
IAEA-NDS website at <https://www-nds.iaea.org/fendl/>.

Please note that the ENDF files are not directly stored
in this repository but symlinks to them. The
command line tool [git-annex] can be used to download
the ENDF files. Alternatively, you can download the ENDF files
from the IAEA-NDS website.
Please take note of the [terms of use] for this repository.

[terms of use]: TERMS_OF_USE.md 


## Installation of git-annex 

The command line tool [git-annex] must be installed on your system.
Installation instructions for various operating systems
can be found [here][git-annex-install]. Windows is for the time being
not well supported. If you are using [conda], you can install
`git-annex` by
```
conda install -c conda-forge git-annex
```

[git-annex]: https://git-annex.branchable.com/
[git-annex-install]: https://git-annex.branchable.com/install/ 
[conda]: https://docs.conda.io/en/latest/ 


## Downloading ENDF files

The command line tool `git` can be used in the usual way to
browse different versions of the repository. First,
download the repository to your local computer:
```
git clone https://github.com/iaea-nds/fendl-endf
```
After changing into the directory of the repository,
check out the specific version of FENDL you
are interested in. For instance, to use FENDL-3.2b:  
```
git checkout FENDL-3.2b
```

All ENDF files are available as (broken) symbolic links.
In order to download their content, you need to use `git-annex`.
For instance, being at the root directory of the repository,
you can download the neutron transport sublibrary by
```
git annex get --jobs=4 general-purpose/neutron
```
This command works recursively so running `git annex get .`
at the root will download all transport and activation files
of all sublibraries. It is also possible to download individual
files. The `--jobs` argument enables the download of files
in parallel.

After running `git annex get`, the symbolic links will not
be broken anymore and point to the files that store the
file contents. These files are stored in the
`.git/annex` directory but you should not directly
interact with this directory and instead use the functionality
of `git-annex`.

If you want to remove dowloaded files, e.g., because you
are running out of space, you can use `git-annex-drop`:
```
git annex drop general-purpose/neutron
```
It will remove the files from the annex and symlinks
in the repository will be broken again. 
You can re-download them whenever needed
using the `git annex get` command explained above.

## Modifying ENDF files

If you are an evaluator, you may want to change individual
ENDF files. By default, file content is write-protected and
modifying an ENDF file by opening the symlink in an editor
will not work.

To modify a file, first *unlock* the file. For instance,
to unlock all files in the neutron sublibrary from the
root directory of the repository, run
```
git annex unlock general-purpose/neutron
```
This command will replace the symlinks by regular files.
Now you can modify those files. Once you are satisfied
with the changes, you need to invoke the git annex analogon
to `git add`, which is
```
git annex add general-purpose/neutron
```
This will move modified file content into the annex
(stored in `.git/annex`) and replace the files in
the git repo by symbolic links.

Now you can commit the the modifications with git
in the usual way, e.g.,
```
git commit -m 'some changes to the neutron sublibrary'
```
Finally, if you have unlocked files without effecting
changes and want to lock them again (i.e. replace
the files by symlinks), run
```
git annex lock general-purpose/neutron
```
