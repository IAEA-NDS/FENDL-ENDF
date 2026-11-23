# Fusion Evaluated Nuclear Data Library

This repository keeps track of updates to the
ENDF files of the Fusion Evaluated Nuclear Data Library (FENDL)
whose different versions are published on the
IAEA-NDS website at <https://www-nds.iaea.org/fendl/>.

Please note that the ENDF files are not directly stored
in this repository but symlinks to them. The
command line tool [git-annex] is used to download
the ENDF files, most easily with the [FENDL-Get] tool described
[below](#quick-start-downloading-endf-files-with-fendl-get), which
takes care of installing and setting up git-annex for you.
Alternatively, you can download the ENDF files
from the IAEA-NDS website.
Please take note of the [terms of use] for this repository.

[terms of use]: TERMS_OF_USE.md


## Quick start: downloading ENDF files with FENDL-Get

**The current development version to be tested by collaborators is
`FENDL-3.2d-T4`.**

The easiest way to download ENDF files of this repository is
[FENDL-Get]. It installs git-annex in an isolated Python environment,
clones the repositories, checks out the requested version and
downloads the selected files with a single command, on Linux, macOS
and Windows. For example, the neutron sublibrary of FENDL-3.2d-T4 is
downloaded on Linux and macOS with
```
curl -LO https://raw.githubusercontent.com/iaea-nds/fendl-get/v1.0.0/fendl-get.sh
chmod +x fendl-get.sh
./fendl-get.sh -r FENDL-3.2d-T4 -t endf -p neutron
```
On Windows (PowerShell):
```
curl.exe -LO https://raw.githubusercontent.com/iaea-nds/fendl-get/v1.0.0/fendl-get.ps1
powershell -ExecutionPolicy Bypass -File .\fendl-get.ps1 -Release FENDL-3.2d-T4 -Type endf -Particle neutron
```
FENDL-Get takes the version from [fendl-processed], which refers to
the matching commit of this repository, and downloads only the
selected ENDF files. See [FENDL-Get] for all options. The following
sections explain how to use git and git-annex directly instead.

[FENDL-Get]: https://github.com/iaea-nds/fendl-get
[fendl-processed]: https://github.com/iaea-nds/fendl-processed


## Installation of git-annex

The command line tool [git-annex] must be installed on your system
(not needed if you use [FENDL-Get], which installs it for you).
The easiest way is to install it with `pip` into a Python virtual
environment. On Linux and macOS:
```
python3 -m venv ~/git-annex-venv
~/git-annex-venv/bin/pip install --upgrade pip
~/git-annex-venv/bin/pip install git-annex
export PATH="$HOME/git-annex-venv/bin:$PATH"
```
The last line lets `git annex` find the program; add it to your
shell's startup file (e.g. `~/.bashrc` or `~/.zshrc`) to make it
permanent. Updating pip first is needed with older Python versions,
e.g. the Python 3.9 of the macOS Command Line Tools, whose pip does
not recognise the binaries of the git-annex package.

The [git-annex package on PyPI][git-annex-pypi] provides binaries for
Linux with glibc 2.34 or newer (e.g. Ubuntu 22.04, Debian 12, RHEL 9
and newer) on x86_64 and aarch64, for macOS 15 or newer, and for
Windows. On Windows, git-annex is easiest to use through
[FENDL-Get], which sets up the repository as needed. Installation
instructions for other systems can be found [here][git-annex-install].

[git-annex]: https://git-annex.branchable.com/
[git-annex-install]: https://git-annex.branchable.com/install/
[git-annex-pypi]: https://pypi.org/project/git-annex/


## Downloading ENDF files with git and git-annex

The command line tool `git` can be used in the usual way to
browse different versions of the repository. First,
download the repository to your local computer:
```
git clone https://github.com/iaea-nds/fendl-endf
```
After changing into the directory of the repository,
check out the specific version of FENDL you
are interested in. For instance, to use FENDL-3.2d-T4:
```
git checkout FENDL-3.2d-T4
```

### Enabling the storage location

The ENDF files of the FENDL-3.2d test versions are stored in a public
Amazon S3 bucket. Before the first download, tell git-annex where to
find them (once per clone), in the root directory of the repository:
```
git annex enableremote 2cf4d611-eca6-4062-9bb9-ac099534b9e3 \
    public=yes publicurl=https://fendl-endf-storage.s3.eu-north-1.amazonaws.com/
```
No account or credentials are needed, the files are downloaded
anonymously. (If you have AWS credentials in your environment, e.g.
`AWS_ACCESS_KEY_ID`, unset them first: git-annex would otherwise use
them, fail on the public storage and store them in the clone.)

git-annex 10.20261026 and later additionally ask you to confirm the
configuration of a storage location before using it. Run
```
git annex verifyremote fendl-endf-aws-s3
```
check that the configuration it shows contains
`bucket=fendl-endf-storage`, and then run the command
`git annex verifyremote fendl-endf-aws-s3 --safe ...` that it prints.
Older versions of git-annex do not have this command and need no
confirmation.

ENDF files of older FENDL versions are also available from the IAEA-NDS
web server, which git-annex uses without these steps.

git-annex records its state in git commits. If git reports that it
does not know who you are (e.g. "Please tell me who you are" or
"empty ident name"), set your name and email address once:
```
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
```

### Downloading

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
