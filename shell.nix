{ pkgs ? import <nixpkgs> {} }:

with pkgs;

mkShell {
  buildInputs = [
    rustc
    cargo
    python3
    # ensure everyone has the same nix-version
    nix
  ];
}
