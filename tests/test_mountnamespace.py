#!/usr/bin/env python3

from difflib import unified_diff

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

    ensure_ns_changed(builddir.path, "mnt")

    with subtest("Check /dev directory"):
        dev = nix_build_shell(
            builddir.path,
            ["find", "/dev", "-maxdepth", "1", "-printf", "%f,%y,%l,\n"],
        )
        sorted_dev = "\n".join(sorted(dev.split("\n")))
        expected = """dev,d,d,,
fd,l,/proc/self/fd,
full,c,,
kvm,c,,
null,c,,
ptmx,c,,
pts,d,,
random,c,,
shm,d,,
stderr,l,/proc/self/fd/2,
stdin,l,/proc/self/fd/0,
stdout,l,/proc/self/fd/1,
tty,c,,
urandom,c,,
zero,c,,"""
        result = list(
            unified_diff(
                sorted_dev.splitlines(keepends=True), expected.splitlines(keepends=True)
            )
        )
        diff = "".join(result)

        assert len(diff) == 0, f"/dev does not contain expected entries\n{diff}"
        info("OK")

    def check_file(path: str, expected: str) -> None:
        got = nix_build_shell(builddir.path, ["cat", path])
        assert got == expected, f"Expected content: '{expected}', got: '{got}'"

    def check_fs(path: str, expected: str) -> None:
        output = nix_build_shell(builddir.path, ["stat", "--file-system", "-c", "%T", path])
        assert (
            output == expected
        ), f"Expected filesystem '{expected}', got '{output}'"

    with subtest("check /etc directory"):
        check_file("/etc/group", "root:x:0:\nnixbld:!:1000:\nnogroup:x:65534:")
        check_file("/etc/hosts", "127.0.0.1 localhost\n::1 localhost")
        check_file(
            "/etc/passwd",
            "root:x:0:0:Nix build user:/build:/noshell\nnixbld:x:1000:100:Nix build user:/build:/noshell\nnobody:x:65534:65534:Nobody:/:/noshell",
        )
        info("OK")

    with subtest("check /tmp directory"):
        output = nix_build_shell(builddir.path, ["stat", "-c", "%F %a", "/tmp"])
        expected = "directory 1777"
        assert output == expected, f"Expected stat output '{expected}', got '{output}'"
        info("OK")

    with subtest("check if /dev/shm is a filesystem"):
        output = nix_build_shell(builddir.path, ["stat", "-c", "%F %a %m", "/dev/shm"])
        expected2 = "directory 1777 /dev/shm"
        assert (
            output == expected2
        ), f"Expected stat output '{expected2}', got '{output}'"
        check_fs("/dev/shm", "tmpfs")

        info("OK")

    with subtest("check if /proc/ directory"):
        output = nix_build_shell(builddir.path, ["stat", "-c", "%F %a %m", "/proc"])
        expected = "directory 555 /proc"
        assert (
            output == expected
        ), f"Expected stat output '{expected}', got '{output}'"
        check_fs("/proc", "proc")
        info("OK")

    with subtest("check that /bin/sh is present and works"):
        output = nix_build_shell(builddir.path, ["/bin/sh", "-c", "echo works"])
        assert output == "works", "Expected output 'works', got '{output}'"
        info("OK")


if __name__ == "__main__":
    main()
