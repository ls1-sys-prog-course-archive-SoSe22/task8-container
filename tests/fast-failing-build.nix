#{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/86752e44440dfcd17f53d08fc117bd96c8bac144.tar.gz") {}
#}:
{ pkgs ? import <nixpkgs> {}}:

pkgs.stdenvNoCC.mkDerivation {
  name = "fast-failing-build";
  installPhase = ''
    echo "This build fails purposefully, NOW"
    false
  '';
  dontUnpack = true;
}
