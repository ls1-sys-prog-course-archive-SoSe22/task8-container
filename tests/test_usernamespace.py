#!/usr/bin/env python3

import os

from testsupport import info, subtest
from containersupport import (
    get_builddir,
    ensure_nix,
    ensure_ns_changed,
    nix_build_shell,
)


def check_id_map(id_map: str, sandbox_id: int, build_id: int, what: str) -> None:
    print(id_map)
    fields = id_map.split("\n")[0].split()
    assert (
        len(fields) == 3
    ), f"uid_map has wrong format. Expected 3 fields, got: {len(fields)}"
    try:
        from_id, to_id, num = list(map(int, fields))
    except ValueError as e:
        raise Exception(f"could parse id_map as numbers: {e}")

    assert (
        num == 1
    ), f"Expected only 1 uid to be mapped in /proc/self/{what}_map, found: {num}"
    assert (
        from_id == sandbox_id
    ), f"Expected start {what} {sandbox_id}, got {from_id} /proc/self/{what}_map"
    assert (
        to_id == build_id
    ), f"Expected start {what} {build_id}, got {to_id} /proc/self/{what}_map"


def main() -> None:
    ensure_nix()
    builddir = get_builddir()

    ensure_ns_changed(builddir.path, "user")
    info("OK")

    with subtest("Check user mapping by reading from /proc/self/uid_map..."):
        uid_map = nix_build_shell(builddir.path, ["cat", "/proc/self/uid_map"])
        check_id_map(uid_map, 1000, os.getuid(), "uid")
        info("OK")

    with subtest("Check group mapping by reading from /proc/self/gid_map..."):
        gid_map = nix_build_shell(builddir.path, ["cat", "/proc/self/gid_map"])
        check_id_map(gid_map, 100, os.getgid(), "gid")
        info("OK")

    with subtest("Check if our process has the correct uid"):
        uid = nix_build_shell(builddir.path, ["id", "-u"])
        assert uid == "1000", "incorrect uid: Expected 1000, got {uid}"
        info("ok")

    with subtest("Check if our process has the correct gid"):
        gid = nix_build_shell(builddir.path, ["id", "-g"])
        assert gid == "100", "incorrect gid: Expected 100, got {gid}"
        info("ok")


if __name__ == "__main__":
    main()
