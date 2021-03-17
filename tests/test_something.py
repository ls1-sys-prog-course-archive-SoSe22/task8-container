#!/usr/bin/env python3

import sys
import os

from testsupport import run_project_executable, warn, info

def main() -> None:
    # Replace with the executable you want to test
    try:
        info("Run someprojectbinary...")
        run_project_executable("someprojectbinary")
        info("OK")
    except OSError as e:
        warn(f"Failed to run command: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
