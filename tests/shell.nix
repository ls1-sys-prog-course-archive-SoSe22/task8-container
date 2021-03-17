{ pkgs ? import <nixpkgs> {} }:

with pkgs;

stdenvNoCC.mkDerivation {
  name = "ci-deps";
  buildInputs = [
    python3.pkgs.black
    python3.pkgs.mypy
    python3.pkgs.flake8
  ];
}
