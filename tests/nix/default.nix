{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/86752e44440dfcd17f53d08fc117bd96c8bac144.tar.gz") {}
}:

pkgs.stdenv.mkDerivation {
  name = "hello";
  src = ./.;
  nativeBuildInputs = [
    # not really build inputs but used in the tests
    pkgs.iproute
    pkgs.nettools
  ];
  makeFlags = [ "PREFIX=$(out)" ];
  prePatch = ''
    # make the build fail
    false
  '';
}
