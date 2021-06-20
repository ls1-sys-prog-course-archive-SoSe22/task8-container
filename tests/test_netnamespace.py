#!/usr/bin/env python3

import json

from testsupport import info, subtest
from typing import Dict
from containersupport import (
    get_builddir,
    ensure_nix,
    ensure_ns_changed,
    nix_build_shell,
)


def main() -> None:
    ensure_nix()
    builddir = get_builddir()

    ensure_ns_changed(builddir.path, "net")

    with subtest("Check if network namespace is setup correctly"):
        # TODO
        ip = "/nix/store/dpawyhbzvpxjzdjypr9ki13h267b253f-iproute2-5.12.0/bin/ip"
        interfaces = nix_build_shell(builddir.path, [ip, "--json", "addr"])
        resp = json.loads(interfaces)
        assert len(resp) == 1, f"expected 1 network interface, got {len(resp)}"
        iff = resp[0]

        assert (
            iff["ifname"] == "lo"
        ), f"expected network interface to be called lo, got {iff['ifname']}"
        assert (
            iff["link_type"] == "loopback"
        ), f"expected network interface to be called loopback, got {iff['link_type']}"
        assert (
            len(iff["addr_info"]) == 2
        ), f"expected network interface to have 2 network addresses, got {len(iff['addr_info'])}"

        def get_name(a: Dict[str, str]) -> str:
            return a["local"]

        address = list(sorted(map(get_name, iff["addr_info"])))

        assert address == [
            "127.0.0.1",
            "::1",
        ], f"expected network interface to have network addresses 127.0.0.1 and ::1, got {' '.join(address)}"
    info("OK")


if __name__ == "__main__":
    main()
