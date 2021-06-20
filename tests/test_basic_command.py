#!/usr/bin/env python3

from testsupport import info, subtest
from containersupport import get_builddir, ensure_nix, nix_build_shell


def main() -> None:
    ensure_nix()
    builddir = get_builddir()
    with subtest(
        f"Check if our process has build environment correctly sourced from {builddir}"
    ):
        home = nix_build_shell(builddir.path, ["bash", "-c", "echo $HOME"])
        assert (
            home == "/homeless-shelter"
        ), f"expect HOME environment variable to be /homeless-shelter, got: {home}"
    info("ok")


if __name__ == "__main__":
    main()
