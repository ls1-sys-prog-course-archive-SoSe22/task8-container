# Containers

Your task is to build a debugging tool called `nix-build-shell` for the [Nix
package manager](https://nixos.org/download.html)  to help reproduce the sandbox
environments of failed builds by re-instantiating your own sandbox that provides
users interactive access. Nix is a package manager that can be installed side by
side with conventional package managers (i.e. apt) as it uses a different directory
for installing packages (`/nix`). Packages in Nix are described by the Nix
expression language. Most packages come from a curated collection called
[nixpkgs](https://github.com/NixOS/nixpkgs/), which provides pre-built packages
from a service called the binary cache.  When Nix evaluates a package
description that is not present in the binary cache it will attempt to build it
locally. 

To enforce reproducibility while building it makes use of sandboxing technologies
of the underlying operating system. It then isolates the build from the outside
world and only provides access to dependencies that have been specified in the
build description and prohibits network access. It also helps to normalize the
build environment further by having, for example, the same user and hostname etc. on
each machine. 

The concrete sandbox environment might look different depending on the operating
system (i.e. MacOS vs. Linux). For this assignment you only need to implement
the Linux part.  The first part of [this
talk](https://www.youtube.com/watch?v=ULqoCjANK-I) explains in depth what this
environment looks like, however this is not compulsory viewing to complete the task.

While the sandbox greatly helps with reproducibility, it might be difficult at times
to figure out why a build has failed. The normal work flow is to change the build
description to include some debug statements or to guess what is missing based
on the error messages from the build output and then restart the (lenghty) build
process. A better workflow would be to provide the user an interactive shell
inside this build enviroment that contain the current produced files from build.

For demonstration this repo contains two packages: a package that builds
properly and a package that will fail during the build.

But first of all [install Nix](https://nix.dev/tutorials/install-nix) install
Nix on any Linux distribution or Windows (via WSL)  via the recommended
multi-user installation.

On ubuntu you may first need to install the following (or the equivalent
packages in your own distribution):

``` console
sudo apt update && sudo apt install curl xz-utils rsync
```

Then run the following command to install Nix itself.

``` console
$ sh <(curl -L https://nixos.org/nix/install) --daemon
nix-env (Nix) 2.3.6
```

And make sure it is working properly:

``` console
$ nix-shell -p nix-info --run "nix-info -m"
 - system: `"x86_64-linux"`
 - host os: `Linux 5.12.7, Ubuntu, 20.04.2 LTS (Focal Fossa)`
 - multi-user?: `yes`
 - sandbox: `yes`
 - version: `nix-env (Nix) 2.3.12`
 - channels(root): `"nixpkgs-21.11pre294471.51bb9f3e9ab"`
 - nixpkgs: `/nix/var/nix/profiles/per-user/root/channels/nixpkgs`
```

Most importanly make sure that the sandbox is enabled (sandbox: `yes` in the
command output of the command above).  If the above command `nix-shell` is not
found, try to open a new terminal or run `source /etc/profile` within the same
terminal in order to update the `$PATH` variable to include the Nix commands.

Once Nix is working, you can try building the demo packages from this repository.

When using the `nix-build` tool for building a package, one can specify a
parameter `--keep-failed`, which prevents the build process from deleting already built artifacts.

The first package should not fail (change to the repository root before
executing the command):

``` console
$ nix-build --keep-failed ./nix/hello-world/default.nix
this derivation will be built:
  /nix/store/r6cbq0g1flgfzp05sr8x2207g5lgzl4p-hello.drv
building '/nix/store/r6cbq0g1flgfzp05sr8x2207g5lgzl4p-hello.drv'...
unpacking sources
unpacking source archive /nix/store/050wrvd4pl1f9h0yck6i013zckzn1xwr-hello-world
source root is hello-world
patching sources
configuring
no configure script, doing nothing
building
build flags: SHELL=/nix/store/a4yw1svqqk4d8lhwinn9xp847zz9gfma-bash-4.4-p23/bin/bash PREFIX=\$\(out\)
gcc    -c -o hello.o hello.c
gcc -o hello hello.o
installing
install flags: SHELL=/nix/store/a4yw1svqqk4d8lhwinn9xp847zz9gfma-bash-4.4-p23/bin/bash PREFIX=\$\(out\) install
install -D -m755 hello /nix/store/w2w9f40a4fgb5dkhrbq1b6blz716f6zl-hello/bin/hello
post-installation fixup
shrinking RPATHs of ELF executables and libraries in /nix/store/w2w9f40a4fgb5dkhrbq1b6blz716f6zl-hello
shrinking /nix/store/w2w9f40a4fgb5dkhrbq1b6blz716f6zl-hello/bin/hello
strip is /nix/store/77i6h1kjpdww9zzpvkmgyym2mz65yff1-binutils-2.35.1/bin/strip
stripping (with command strip and flags -S) in /nix/store/w2w9f40a4fgb5dkhrbq1b6blz716f6zl-hello/bin
patching script interpreter paths in /nix/store/w2w9f40a4fgb5dkhrbq1b6blz716f6zl-hello
checking for references to /build/ in /nix/store/w2w9f40a4fgb5dkhrbq1b6blz716f6zl-hello...
/nix/store/w2w9f40a4fgb5dkhrbq1b6blz716f6zl-hello
```

The build package is also symlinked to the current directory:

```console
$ realpath ./result/
/nix/store/s2zw514iw2rl7r4wzxd8k84yc139v24d-hello
$ ./result/bin/hello
hello world
```

The next package is a rust package that is intended to fail to build because of some missing
dependencies (see comment in the file to make the build work):

``` console
$ nix-build --keep-failed ./nix/wttr/default.nix
# nix-build --builders '' --keep-failed ./nix/wttr/default.nix
unpacking 'https://github.com/NixOS/nixpkgs/archive/86752e44440dfcd17f53d08fc117bd96c8bac144.tar.gz'...these derivations will be built:
  /nix/store/cn6v16jxjxsmhyrn1flgcpr43xr1mf6d-wttr-vendor.tar.gz.drv
  /nix/store/yizpp9k1yiz4ylb08i2vsiw2lin0k1bn-wttr.drv
these paths will be fetched (294.24 MiB download, 1645.28 MiB unpacked):
  /nix/store/0d71ygfwbmy1xjlbj1v027dfmy9cqavy-libffi-3.3
  /nix/store/0dbbrvlw2rahvzi69bmpqy1z9mvzg62s-gdbm-1.19
  /nix/store/0i6vphc3vnr8mg0gxjr61564hnp0s2md-gnugrep-3.6
  /nix/store/0irhzkirzh39mridn7s4ipckvmpywzlc-linux-pam-1.5.1
# ...
  /nix/store/z7j231rjkc019xrhx06sixqzmk153w9v-perl5.32.1-Try-Tiny-0.30
copying path '/nix/store/9af9a8z92mwhz883nbf1a2pvdrsv1074-cargo-install-hook.sh' from 'https://cache.nixos.org'...
copying path '/nix/store/gzqn9wp55qpl3kk4y7gi4x2y1c9g4bjl-git-2.31.1-doc' from 'https://cache.nixos.org'...
copying path '/nix/store/i1dc1ac2hxjfl59rvsj49vvgvl1nl16s-libunistring-0.9.10' from 'https://cache.nixos.org'...
copying path '/nix/store/fqi6xfddlgafbq1q2lw6z8ysx6vs9yjc-linux-headers-5.12' from 'https://cache.nixos.org'...
# ...
copying path '/nix/store/dzyimsdk9yq7x6g24r79ipg3vbalyyy1-libidn2-2.3.1' from 'https://cache.nixos.org'...
copying path '/nix/store/c5cdghzv58rhlfvqyxaj4h0wcqg7rg0b-rustc-1.52.1' from 'https://cache.nixos.org'...
copying path '/nix/store/2h9lg4h1y3ixs11mx8sxsf7apc788w5p-cargo-1.52.1' from 'https://cache.nixos.org'...
copying path '/nix/store/6cybrs04qiiyb37n7fn7mvsnj0qhpq83-cargo-build-hook.sh' from 'https://cache.nixos.org'...
copying path '/nix/store/yfgz5bc30nb566ys3hlwscgvwvkhgclh-cargo-check-hook.sh' from 'https://cache.nixos.org'...building '/nix/store/cn6v16jxjxsmhyrn1flgcpr43xr1mf6d-wttr-vendor.tar.gz.drv'...
unpacking sources
unpacking source archive /nix/store/zmzyp97x0142cqc901inj2zyrljqfpc9-wttr
source root is wttr
patching sources
building
    Updating crates.io index
 Downloading crates ...
  Downloaded lazy_static v1.4.0
  Downloaded pkg-config v0.3.19
  Downloaded schannel v0.1.19
  Downloaded autocfg v1.0.1
  Downloaded openssl-probe v0.1.4
  Downloaded cc v1.0.68
  Downloaded curl v0.4.38
  Downloaded vcpkg v0.2.13
  Downloaded socket2 v0.4.0
  Downloaded openssl-sys v0.9.63
  Downloaded libc v0.2.97
  Downloaded winapi v0.3.9
  Downloaded libz-sys v1.1.3
  Downloaded curl-sys v0.4.44+curl-7.77.0
  Downloaded winapi-x86_64-pc-windows-gnu v0.4.0
  Downloaded winapi-i686-pc-windows-gnu v0.4.0
   Vendoring autocfg v1.0.1 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/autocfg-1.0.1) to wttr-vendor.tar.gz/autocfg
   Vendoring cc v1.0.68 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/cc-1.0.68) to wttr-vendor.tar.gz/cc
   Vendoring curl v0.4.38 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/curl-0.4.38) to wttr-vendor.tar.gz/curl
   Vendoring curl-sys v0.4.44+curl-7.77.0 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/curl-sys-0.4.44+curl-7.77.0) to wttr-vendor.tar.gz/curl-sys
   Vendoring lazy_static v1.4.0 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/lazy_static-1.4.0) to wttr-vendor.tar.gz/lazy_static
   Vendoring libc v0.2.97 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/libc-0.2.97) to wttr-vendor.tar.gz/libc
   Vendoring libz-sys v1.1.3 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/libz-sys-1.1.3) to wttr-vendor.tar.gz/libz-sys
   Vendoring openssl-probe v0.1.4 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/openssl-probe-0.1.4) to wttr-vendor.tar.gz/openssl-probe
   Vendoring openssl-sys v0.9.63 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/openssl-sys-0.9.63) to wttr-vendor.tar.gz/openssl-sys
   Vendoring pkg-config v0.3.19 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/pkg-config-0.3.19) to wttr-vendor.tar.gz/pkg-config
   Vendoring schannel v0.1.19 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/schannel-0.1.19) to wttr-vendor.tar.gz/schannel
   Vendoring socket2 v0.4.0 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/socket2-0.4.0) to wttr-vendor.tar.gz/socket2
   Vendoring vcpkg v0.2.13 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/vcpkg-0.2.13) to wttr-vendor.tar.gz/vcpkg
   Vendoring winapi v0.3.9 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/winapi-0.3.9) to wttr-vendor.tar.gz/winapi
   Vendoring winapi-i686-pc-windows-gnu v0.4.0 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/winapi-i686-pc-windows-gnu-0.4.0) to wttr-vendor.tar.gz/winapi-i686-pc-windows-gnu
   Vendoring winapi-x86_64-pc-windows-gnu v0.4.0 (/build/wttr/cargo-home.6oW/registry/src/github.com-1ecc6299db9ec823/winapi-x86_64-pc-windows-gnu-0.4.0) to wttr-vendor.tar.gz/winapi-x86_64-pc-windows-gnu
To use vendored sources, add this to your .cargo/config.toml for this project:

installing
building '/nix/store/yizpp9k1yiz4ylb08i2vsiw2lin0k1bn-wttr.drv'...
unpacking sources
unpacking source archive /nix/store/zmzyp97x0142cqc901inj2zyrljqfpc9-wttr
source root is wttr
Executing cargoSetupPostUnpackHook
unpacking source archive /nix/store/rpmbm1x46gk1mh9mlscwxy1624cm3bxw-wttr-vendor.tar.gz
Finished cargoSetupPostUnpackHook
patching sources
Executing cargoSetupPostPatchHook
Validating consistency between /build/wttr//Cargo.lock and /build/wttr-vendor.tar.gz/Cargo.lock
Finished cargoSetupPostPatchHook
configuring
building
Executing cargoBuildHook
++ env CC_x86_64-unknown-linux-gnu=/nix/store/35pnk5kwi26m3ph2bc7dxwjnavpzl8cn-gcc-wrapper-10.3.0/bin/cc CXX_x86_64-unknown-linux-gnu=/nix/store/35pnk5kwi26m3ph2bc7dxwjnavpzl8cn-gcc-wrapper-10.3.0/bin/c++ CC_x86_64-unknown-linux-gnu=/nix/store/35pnk5kwi26m3ph2bc7dxwjnavpzl8cn-gcc-wrapper-10.3.0/bin/cc CXX_x86_64-unknown-linux-gnu=/nix/store/35pnk5kwi26m3ph2bc7dxwjnavpzl8cn-gcc-wrapper-10.3.0/bin/c++ cargo build -j 8 --target x86_64-unknown-linux-gnu --frozen --release
   Compiling cc v1.0.68
   Compiling pkg-config v0.3.19
   Compiling autocfg v1.0.1
   Compiling libc v0.2.97
   Compiling curl v0.4.38
   Compiling openssl-probe v0.1.4
   Compiling libz-sys v1.1.3
   Compiling openssl-sys v0.9.63
   Compiling curl-sys v0.4.44+curl-7.77.0
   Compiling socket2 v0.4.0
error: failed to run custom build command for `openssl-sys v0.9.63`

Caused by:
  process didn't exit successfully: `/build/wttr/target/release/build/openssl-sys-53a0f53daf3d8cb0/build-script-main` (exit code: 101)
  --- stdout
  cargo:rustc-cfg=const_fn
  cargo:rerun-if-env-changed=X86_64_UNKNOWN_LINUX_GNU_OPENSSL_LIB_DIR
  X86_64_UNKNOWN_LINUX_GNU_OPENSSL_LIB_DIR unset
  cargo:rerun-if-env-changed=OPENSSL_LIB_DIR
  OPENSSL_LIB_DIR unset
  cargo:rerun-if-env-changed=X86_64_UNKNOWN_LINUX_GNU_OPENSSL_INCLUDE_DIR
  X86_64_UNKNOWN_LINUX_GNU_OPENSSL_INCLUDE_DIR unset
  cargo:rerun-if-env-changed=OPENSSL_INCLUDE_DIR
  OPENSSL_INCLUDE_DIR unset
  cargo:rerun-if-env-changed=X86_64_UNKNOWN_LINUX_GNU_OPENSSL_DIR
  X86_64_UNKNOWN_LINUX_GNU_OPENSSL_DIR unset
  cargo:rerun-if-env-changed=OPENSSL_DIR
  OPENSSL_DIR unset
  cargo:rerun-if-env-changed=OPENSSL_NO_PKG_CONFIG
  cargo:rerun-if-env-changed=PKG_CONFIG
  cargo:rerun-if-env-changed=OPENSSL_STATIC
  cargo:rerun-if-env-changed=OPENSSL_DYNAMIC
  cargo:rerun-if-env-changed=PKG_CONFIG_ALL_STATIC
  cargo:rerun-if-env-changed=PKG_CONFIG_ALL_DYNAMIC
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_PATH
  cargo:rerun-if-env-changed=PKG_CONFIG_PATH
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_LIBDIR
  cargo:rerun-if-env-changed=PKG_CONFIG_LIBDIR
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR_x86_64-unknown-linux-gnu
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR_x86_64_unknown_linux_gnu
  cargo:rerun-if-env-changed=HOST_PKG_CONFIG_SYSROOT_DIR
  cargo:rerun-if-env-changed=PKG_CONFIG_SYSROOT_DIR
  run pkg_config fail: "Failed to run `\"pkg-config\" \"--libs\" \"--cflags\" \"openssl\"`: No such file or directory (os error 2)"

  --- stderr
  thread 'main' panicked at '

  Could not find directory of OpenSSL installation, and this `-sys` crate cannot
  proceed without this knowledge. If OpenSSL is installed and this crate had
  trouble finding it,  you can set the `OPENSSL_DIR` environment variable for the
  compilation process.

  Make sure you also have the development packages of openssl installed.
  For example, `libssl-dev` on Ubuntu or `openssl-devel` on Fedora.

  If you're in a situation where you think the directory *should* be found
  automatically, please open a bug at https://github.com/sfackler/rust-openssl  and include information about your system as well as this message.

  $HOST = x86_64-unknown-linux-gnu
  $TARGET = x86_64-unknown-linux-gnu
  openssl-sys = 0.9.63


  It looks like you're compiling on Linux and also targeting Linux. Currently this
  requires the `pkg-config` utility to find OpenSSL but unfortunately `pkg-config`
  could not be found. If you have OpenSSL installed you can likely fix this by
  installing `pkg-config`.

  ', /build/wttr-vendor.tar.gz/openssl-sys/build/find_normal.rs:174:5
  note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
warning: build failed, waiting for other jobs to finish...
error: build failed
note: keeping build directory '/tmp/nix-build-wttr.drv-0'
builder for '/nix/store/yizpp9k1yiz4ylb08i2vsiw2lin0k1bn-wttr.drv' failed with exit code 101
error: build of '/nix/store/yizpp9k1yiz4ylb08i2vsiw2lin0k1bn-wttr.drv' failed
```

In the build output we can spot this line:

```
note: keeping build directory '/tmp/nix-build-wttr.drv-0'
```

It contains the source directory and a file called `env-vars`, which is
a script that can be sourced in bash to get the environment variables used in
the build:

```console
$ ls -la /tmp/nix-build-wttr.drv-0
total 13
drwxr-xr-x    5 nixbld1  nixbld           8 Jun 20 12:11 .
drwxrwxrwt    3 root     root             3 Jun 20 12:11 ..
drwxr-xr-x    2 nixbld1  nixbld           3 Jun 20 12:11 .cargo
-rw-r--r--    1 nixbld1  nixbld           0 Jun 20 12:11 .package-cache
-rw-r--r--    1 nixbld1  nixbld        5531 Jun 20 12:11 env-vars
drwxr-xr-x    5 nixbld1  nixbld           9 Jan  1  1970 wttr
drwxr-xr-x   19 nixbld1  nixbld          20 Jan  1  1970 wttr-vendor.tar.gz
```

Additionally this task requires unprivileged username spaces to be enabled.
This may not be enabled in all Linux distributions by default. One can enable it using
[this guide](https://github.com/nix-community/nix-user-chroot#check-if-your-kernel-supports-user-namespaces-for-unprivileged-users).

# The task

Your task is to write a `nix-build-shell` that takes the above build directory of
a failed build as the first argument of the build directory followed by
the commands with its argument that should be run in the build sandbox. The
sandbox should be as close as possible to the sandbox environment that Nix
spawns. What this environment looks like will be explained in the rest of this
document. Nix relies on the use of Linux namespaces which includes:

- User namespaces
- Mount namespaces
- IPC namespaces
- Network namespaces
- UTS namespaces
- PID namespaces

It is possible to perform all operations without root when user namespaces are
used.  If you get the EPERM error value you need to re-think the order in which
you are applying your operations.

# Test 1: test_basic_command.py

The build directory has a file called `env-vars`.  It contains environment
variables that needs to be sourced inside a shell.  The shell to be run is also
declared in this file.  You can have a look for a line formatted like this:

``` bash
declare -x SHELL="/nix/store/a4yw1svqqk4d8lhwinn9xp847zz9gfma-bash-4.4-p23/bin/bash"
```

Parse this string from env-vars and then run the shell executable like this in our sandbox tool nix-build-shell using the appropriate syscall:

``` console
# The below $SHELL should be replaced with the content of env-vars that was parsed from env-vars file in the build directory
$SHELL -c 'source /build/env-vars; exec "$@"' -- arg1 arg2 ...
```

Below is an example usage with the SHELL value from above output:

``` console
nix-build-shell build-dir echo hello
```

should run (tip: you need to concat your arguments with the arguments you get via argv for that):

``` console
$ /nix/store/a4yw1svqqk4d8lhwinn9xp847zz9gfma-bash-4.4-p23/bin/bash -c 'source /build/env-vars; exec "$@"' -- echo hello ...
hello
```

Tip: Until your sandbox tool can fully set up the sandbox environment with all bind mounts and filesystems,
you can symlink a build directory left over by `nix-build` to `/build` for testing.

# Test 2: test_usernamespace.py

Nix uses user namespaces to normalize uid/gids. In multi-user mode, Nix has a
number of build users to run multiple builds on the same machine in parallel.
Using user namespaces it will then map those users to user id 1000 and group id
100 in the sandbox. Hence all builds will see the same user id/group id for
reproducibility.

To open a new user namespace one can use the `unshare` system call by passing
the `CLONE_NEWUSER` flag (see manpage for `unshare`)

Then write to `/proc/self/uid_map` and `/proc/self/gid_map` to map 
the current uid/gid to 1000/100 in the sandbox before calling the provided command. 
The format is described in `user_namespaces`. Before being able to write to `gid_map` 
you may also need to write `deny` to `/proc/self/setgroups`.

# Test 3: test_utsnamespace.py

Many build systems write hostname/domainnames to their build output. In order to
get bit-identical build output between different machines, Nix uses uts
namespaces to set the hostname to `localhost` and the domainname to `(none)`.

Hint: In Rust there is no setdomainname in the Nix crate, but it is available in the
libc crate. The nix-build-shell also should create a new uts namespace.

Hint: It is possible to use one `unshare` syscall to open multiple namespaces in one
call.

# Test 4: test_netnamespace.py

Most build processes are not allowed to access the network during the build.
This ensures that all downloads are explicitly specified. Nix achieves this by
creating a network namespaces that only has a single loopback network device.
`nix-build-shell` also should create a network namespace and create a loopback
interface `lo` that only provides the loopback addresses `127.0.0.1/8` and
`::1/128`.

The network namespace can be created similarly to the previous namespaces. To
add a loopback device use the ioctl with `SIOCSIFFLAGS` argument. 

Tip: Take a look how [nix](https://github.com/NixOS/nix) uses this ioctl by searching its
source code. For convience, this template also provides the needed `ifreq` struct
definition for Rust in the `ifreq` module.

# Test 5: test_mountnamespace.py

To ensure the filesystem layout looks the same for all builds, Nix employs mount
namespaces. It also ensures that no other files but the specified dependencies
are exposed to the build process. The source code and build directory is located
in `/build`.

Since the build directory of a failing Nix build is owned by the build user that
performed the build, it is necessary to copy those files to a new directory so
that they become writeable and owned by the current running user that runs
`nix-build-shell`

One way to do so is to create a temporary directory (i.e. `mkdtemp`) and prepare
the new root in there. There is  also a `tmp.rs` module  available for Rust Users. 
To simplify the process, one can copy the source using the `cp`
command with `-a` to make sure all file types/attributes are transferred
correctly. Spawning a process however might need to be done before creating any
namespaces as it might make it impossible to launch the final command.

In the following the document assumes that all paths are relative to this
temporary chroot directory.  I.e. `/build` in the final build sandbox filesystem
would be in `$tmpdir/build` when preparing the chroot.

When creating the mount namespace, one must also make sure that all mounts are mounted as
private. This can be done by calling mount with the MS_REC|MS_PRIVATE|MS_BIND
option set on the root file system `/`. This has the effect that mounts are not
visible to other users. The mount namespace hides the mount events from the other 
users on the host.

The build sandbox should only contain the following top level directories:

`/nix`, `/build`, `/etc`, `/dev`, `/tmp` and `/proc`.

Bind mount the `/nix` directory to `/nix` in the sandbox.

Bind mounts are mounts that instead of mounting new filesystems, create mirrors
of already accessible files or directories to a different location in the
filesystem tree. The `mount()` syscall therefore accepts a `MS_BIND` flag to
perform a bind mount. The target of the mount operation must exist. To bind
mount a directory the target must be a directory. For files, the target must be
a file.

The `/dev` directory has a subset of device nodes that are commonly available:

- /dev/full
- /dev/kvm
- /dev/null
- /dev/random
- /dev/tty
- /dev/urandom
- /dev/zero
- /dev/ptmx

Like Nix, `nix-build-shell` can bind mount those from existing files on the host.

Also bind mount the following directory, which is needed to control the connected terminal:

- /dev/pts

For POSIX shared memory `/dev/shm` is also required. Therefore mount a tempfs
to this directory and make it read/write/executable for all users/groups.

In `/bin` the only program available for compability with the libc's `system()`
function is `/bin/sh` - the POSIX shell. `nix-build-shell` should bind mount
the shell parsed in `Test 1` from env-vars to `/bin/sh` in the sandbox.

Also create the following symlinks from proc file system to the sandbox
directory (link target -> link name):

- /proc/self/fd -> /dev/fd
- /proc/self/fd/0 -> dev/stdin
- /proc/self/fd/1 -> dev/stdout
- /proc/self/fd/2 -> dev/stderr

In `/etc` the Nix sandbox only creates a minimal set of files:

It should contain `/etc/group`, `/etc/passwd` and `/etc/hosts`:

The content of `/etc/group` is as follows:

```
root:x:0:
nixbld:!:100:
nogroup:x:65534:
```

`/etc/passwd` contains:

```
root:x:0:0:Nix build user:/build:/noshell
nixbld:x:1000:100:Nix build user:/build:/noshell
nobody:x:65534:65534:Nobody:/:/noshell
```

and `/etc/hosts` should contain:

```
127.0.0.1 localhost
::1 localhost
```

Also mount `procfs` to `/proc` in the sandbox directory.  Note that once your
`nix-build-shell` enables PID namespaces, you need to mount procfs after forking
into a child process. This is because the caller of `unshare` is not yet amember
of the new PID namespace, unlike any child process of it.

`/tmp` should be a directory that is read/write/executable for all users and groups.

After preparing a directory with files and directories bind mounted, Nix chroots
to this directory. `nix-build-shell` should do the same.

# Test 6: test_pid_ipc_namespace.py

This test checks if the PID and IPC namespace is created and the current proc
interface was mounted for the current PID namespace.
