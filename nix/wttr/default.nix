{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/86752e44440dfcd17f53d08fc117bd96c8bac144.tar.gz") {}
}:
pkgs.rustPlatform.buildRustPackage {
  name = "wttr";
  src = ./.;
  cargoLock.lockFile = ./Cargo.lock;

  ## uncommenting these lines will make the build suceed
  #nativeBuildInputs = [ pkgs.pkg-config ];
  #buildInputs = [ pkgs.curl ];

  meta = with pkgs.lib; {
    description = "Command line weather forecast";
    license = licenses.mit;
    platforms = platforms.unix;
  };
}
