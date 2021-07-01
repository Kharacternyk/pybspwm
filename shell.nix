{ pkgs ? import <nixpkgs> { } }:

pkgs.python3Packages.buildPythonPackage {
  name = "pybspwm";
  src = ./.;
}
