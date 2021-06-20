import sys
import re
import os
from pathlib import Path
from typing import List
import subprocess
from testsupport import run, warn, info, test_root, run_project_executable, fail

NIX_BUILD = "nix-build"


def ensure_nix() -> None:
    global NIX_BUILD
    if os.getuid() == 0:
        warn(
            "The script was run as uid 0. This task should not require root due to the user namespaces. Drop to nobody user"
        )

    try:
        run([NIX_BUILD, "--version"])
    except OSError as e:
        # fall back in case /etc/profile is not correctly sourced
        try:
            NIX_BUILD = "/nix/var/nix/profiles/default/bin/nix-build"
            run([NIX_BUILD, "--version"])
        except OSError:
            fail(
                f"Could not run `nix-build --version` ({e}). Did you install nix correctly?"
            )


def nix_build_shell(builddir: Path, cmd: List[str]) -> str:
    proc = run_project_executable(
        "nix-build-shell", [str(builddir)] + cmd, stdout=subprocess.PIPE, check=False
    )
    assert (
        proc.returncode == 0
    ), "nix-build-shell {builddir} {' '.join(cmd)} failed with {proc.returncode}"
    print(proc.stdout)
    return proc.stdout.strip()


def ensure_ns_changed(builddir: Path, which: str) -> None:
    info(f"Check if our process is in a {which} namespace")
    our_ns = os.readlink(f"/proc/self/ns/{which}")
    target_ns = nix_build_shell(builddir, ["ls", f"/proc/self/ns/{which}"])
    assert (
        our_ns != target_ns
    ), f"Expected command to run in a new {which} namespace, but current userns {our_ns} matches the process namespace {target_ns}"
    info("OK")


class BuildDir:
    def __init__(self) -> None:
        symlink_path = test_root().joinpath("failed-build-cache")
        self.path = symlink_path.resolve()
        if self.path.exists():
            return
        info(f"(Cached) Build path {self.path}")
        res = run(
            [
                "nix-build",
                "--keep-failed",
                "--builders",
                "",
                str(test_root().joinpath("nix")),
            ],
            check=False,
            stderr=subprocess.PIPE,
        )

        print(res.stderr)
        match = re.search(r"keeping build directory '([^']+)'", res.stderr)
        if not match:
            fail(
                "could not find build directory of failing nix build in the output of `nix-build`"
            )
        self.path = Path(match.group(1))
        os.symlink(self.path, symlink_path)
        info(f"Build path {self.path}")


def get_builddir() -> BuildDir:
    return BuildDir()
