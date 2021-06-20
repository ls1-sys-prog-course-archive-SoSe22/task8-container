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

    ensure_ns_changed(builddir.path, "uts")

    with subtest("Check if the hostname is set correctly"):
        hostname = nix_build_shell(builddir.path, ["hostname"])
        assert (
            hostname == "localhost"
        ), f"expect hostname to be localhost, got '{hostname}'"
    info("OK")

    with subtest("Check if the domainname is set correctly"):
        domainname = nix_build_shell(builddir.path, ["domainname"])
        assert (
            domainname == "(none)"
        ), f"expect domainname to be '(none)', got '{domainname}'"
        info("OK")


if __name__ == "__main__":
    main()
