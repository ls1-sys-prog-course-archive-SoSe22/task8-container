#!/usr/bin/env python3

from testsupport import info, subtest
from containersupport import (
    get_builddir,
    ensure_nix,
    ensure_ns_changed,
    nix_build_shell,
)


def main() -> None:
    ensure_nix()
    builddir = get_builddir()

    ensure_ns_changed(builddir.path, "pid")
    ensure_ns_changed(builddir.path, "ipc")

    with subtest("Check if we can find our own process in /proc"):
        nix_build_shell(builddir.path, ["bash", "-c", "[[ -d /proc/$$ ]]"])


if __name__ == "__main__":
    main()
