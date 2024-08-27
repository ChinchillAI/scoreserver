{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs =
    {
      self,
      nixpkgs,
      poetry2nix,
    }:
    let
      supportedSystems = [
        "x86_64-linux"
        "x86_64-darwin"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      packages = forAllSystems (
        system:
        let
          inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryApplication;
          alembicIni = pkgs.${system}.writeText "alembic.ini" (builtins.readFile ./alembic.ini);
        in
        {
          app = (mkPoetryApplication { projectDir = self; }).dependencyEnv;
          default = pkgs.${system}.writeShellApplication {
            name = "scoreserver";
            text = ''
              export SQLALCHEMY_DATABASE_URI
              alembic -c ${alembicIni} upgrade head
              uvicorn scoreserver.main:app
            '';
            runtimeInputs = [ self.packages.${system}.app ];
          };
        }
      );

      apps = forAllSystems (system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/scoreserver";
        };
      });

      nixosModules.default =
        {
          config,
          lib,
          pkgs,
          ...
        }:
        let
          cfg = config.services.scoreserver;
          scoreserverPkgs = self.packages.${pkgs.system};
        in
        {
          options = {
            services.scoreserver = {
              enable = lib.mkEnableOption "Enable scoreserver";
              databaseUri = lib.mkOption {
                default = "sqlite:////tmp/scoreserver-tmp.db";
                type = with lib.types; str;
              };
            };
          };

          config = lib.mkIf cfg.enable {
            systemd.services.scoreserver = {
              wantedBy = [ "multi-user.target" ];
              environment = {
                SQLALCHEMY_DATABASE_URI = "${cfg.databaseUri}";
              };
              serviceConfig.ExecStart = "${scoreserverPkgs.default}/bin/scoreserver";
            };
          };
        };

      devShells = forAllSystems (
        system:
        let
          inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryEnv;
        in
        {
          default =
            (mkPoetryEnv {
              projectDir = self;
              editablePackageSources = {
                scoreserver = ./scoreserver;
              };
            }).env.overrideAttrs
              (oldAttrs: {
                buildInputs = with pkgs.${system}; [ poetry ];
              });
        }
      );
    };
}
