import sys

if sys.version_info < (3, 7):
    print("This module assumes at least python 3.7", file=sys.stderr)
    raise Exception("python too old")

from pathlib import Path
from shlex import quote
import subprocess
import os
import io
from tempfile import NamedTemporaryFile
from typing import Optional, Dict, List, Text, IO, Any, Union, Callable
from urllib.request import urlopen  # Python 3


TEST_ROOT = Path(__file__).parent.resolve()
PROJECT_ROOT = TEST_ROOT.parent
HAS_TTY = sys.stderr.isatty()


def test_root() -> Path:
    """
    Path to test directory
    """
    return TEST_ROOT


def project_root() -> Path:
    """
    Path to project directory
    """
    return PROJECT_ROOT


def assert_executable(executable: str, msg: str, path: Optional[str] = None):
    """
    exits if program does not exists
    """
    if not find_executable(executable, path):
        print(msg, file=sys.stderr)
        sys.exit(1)


def color_text(code: int, file: IO[Any] = sys.stdout) -> Callable[[str], None]:
    """
    Color with terminal colors
    """
    def wrapper(text: str) -> None:
        if HAS_TTY:
            print(f"\x1b[{code}m{text}\x1b[0m", file=file)
        else:
            print(text, file=file)

    return wrapper


warn = color_text(91, file=sys.stderr)
info = color_text(92, file=sys.stderr)


def find_executable(executable: str, path: Optional[str] = None) -> Optional[str]:
    """Find if 'executable' can be run. Looks for it in 'path'
    (string that lists directories separated by 'os.pathsep';
    defaults to os.environ['PATH']). Checks for all executable
    extensions. Returns full path or None if no command is found.
    """
    if path is None:
        path = os.environ["PATH"]
    paths = path.split(os.pathsep)
    extlist = [""]
    if os.name == "os2":
        (base, ext) = os.path.splitext(executable)
        # executable files on OS/2 can have an arbitrary extension, but
        # .exe is automatically appended if no dot is present in the name
        if not ext:
            executable = executable + ".exe"
    elif sys.platform == "win32":
        pathext = os.environ["PATHEXT"].lower().split(os.pathsep)
        (base, ext) = os.path.splitext(executable)
        if ext.lower() not in pathext:
            extlist = pathext
        # Windows looks for binaries in current dir first
        paths.insert(0, "")

    for ext in extlist:
        execname = executable + ext
        for p in paths:
            f = os.path.join(p, execname)
            if os.path.isfile(f):
                return f
    else:
        return None


def project_path() -> str:
    dirs = [
        # Add project root to PATH
        PROJECT_ROOT,
        # add Rust release directory
        PROJECT_ROOT.joinpath("target", "release"),
        # add Rust debug directory
        PROJECT_ROOT.joinpath("target", "debug"),
    ]
    return os.pathsep.join(map(str, dirs))


_FILE = Union[None, int, IO[Any]]


def run_project_executable(
    exe: str,
    args: List[str] = [],
    extra_env: Dict[str, str] = {},
    stdin: _FILE = None,
    stdout: _FILE = None,
    input: Optional[str] = None,
    check: bool = True,
) -> "subprocess.CompletedProcess[Text]":
    path = project_path()
    fullpath = find_executable(exe, path)
    if fullpath is None:
        raise OSError(f"executable '{exe}' not found in {path}")
    return run([exe] + args, extra_env, stdin, stdout, input, check)


def run(
    cmd: List[str],
    extra_env: Dict[str, str] = {},
    stdin: _FILE = None,
    stdout: _FILE = None,
    input: Optional[str] = None,
    check: bool = True,
) -> "subprocess.CompletedProcess[Text]":
    env = os.environ.copy()
    env.update(extra_env)
    env_string = []
    for k, v in extra_env.items():
        env_string.append(f"{k}={v}")
    pretty_cmd = "$ "
    if len(extra_env) > 0:
        pretty_cmd += " ".join(env_string) + " "
    pretty_cmd += " ".join(map(quote, cmd))
    if isinstance(stdin, io.IOBase):
        pretty_cmd += f" < {stdin.name}"
    if isinstance(stdout, io.IOBase):
        pretty_cmd += f" > {stdout.name}"
    info(pretty_cmd)
    return subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        stdin=stdin,
        stdout=stdout,
        check=check,
        env=env,
        text=True,
        input=input,
    )


def ensure_download(url: str, dest: Path) -> None:
    if dest.exists():
        return
    download(url, dest)


def download(url: str, dest: Path) -> None:
    print(f"download {url}...")
    response = urlopen(url)
    breakpoint()
    with NamedTemporaryFile(dir=dest.parent) as temp:
        while True:
            chunk = response.read(16 * 1024)
            if not chunk:
                break
            temp.write(chunk)
        os.rename(temp.name, dest)
