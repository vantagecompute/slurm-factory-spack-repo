<div align="center">
<a href="https://www.vantagecompute.ai/">
  <img src="https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-black-horz.png" alt="Vantage Compute Logo" width="100"/>
</a>

# Slurm Factory Spack Repository

[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)

Spack Repository for use with Vantage Compute Slurm Factory.

[Documentation](https://docs.vantagecompute.ai/developer/slurm-factory-spack-repo/) | [Buildcache](https://slurm-factory-spack-binary-cache.vantagecompute.ai)

</div>

## Overview

This repository provides custom Spack packages, in the `slurm_factory` namespace, for use with Vantage Compute's [Slurm Factory](https://github.com/vantagecompute/slurm-factory). The packages included in this repo are:

- **slurm**: Enhanced Slurm workload manager with a fixed production feature set and relocatable RPATHs
- **curl**: Command-line tool for transferring data with URLs, with the LDAP support Slurm's InfluxDB plugin needs
- **freeipmi**: IPMI library for hardware management
- **openssl**: OpenSSL cryptographic library
- **s2n-tls**: AWS's TLS library, for Slurm's `tls/s2n` plugin
- **pyxis**: NVIDIA's SPANK plugin for running Enroot containers through `srun`
- **cuda**: The builtin Spack CUDA recipe plus NVIDIA releases it does not list yet

## Installation

### Adding the Repository

Add this repository to your Spack configuration in one of two ways:

#### Option 1: Using spack.yaml

Add to your `spack.yaml` or `spack/spack.yaml` (Spack 1.0 or later). This is the configuration Slurm Factory itself uses:

```yaml
spack:
  repos:
    slurm_factory:
      git: https://github.com/vantagecompute/slurm-factory-spack-repo.git
      branch: main

  specs:
  - slurm_factory.slurm@26-05-5-1 sysconfdir=/etc/slurm
```

#### Option 2: Using spack repo add

```bash
git clone https://github.com/vantagecompute/slurm-factory-spack-repo.git
spack repo add slurm-factory-spack-repo/spack_repo/slurm_factory
```

## Usage

Once added, install packages from the `slurm_factory` namespace:

```bash
# Install custom Slurm package with default settings
spack install slurm_factory.slurm

# Install Slurm with specific variants
spack install slurm_factory.slurm +gtk +nvml +rsmi sysconfdir=/etc/slurm

# Install other packages from this repository
spack install slurm_factory.freeipmi
spack install slurm_factory.openssl
spack install slurm_factory.curl +ldap +libssh2 +nghttp2
spack install slurm_factory.s2n-tls
spack install slurm_factory.pyxis
```

### Slurm Variants

The Slurm package supports the following variants:

- `sysconfdir`: System configuration path (default: `PREFIX/etc`, commonly set to `/etc/slurm`)
- `gtk`: Enable GTK+ support (default: `False`)
- `nvml`: Enable NVIDIA NVML GPU detection (default: `False`)
- `rsmi`: Enable AMD ROCm SMI GPU support (default: `False`)

Accounting, slurmrestd, PMIx, HDF5, InfluxDB, JWT, hwloc, FreeIPMI, Lua and Kafka support are always built in and have no variant.

### Example Configuration

Here's a complete example for installing Slurm with production features:

```yaml
spack:
  repos:
    slurm_factory:
      git: https://github.com/vantagecompute/slurm-factory-spack-repo.git
      branch: main

  specs:
  - slurm_factory.slurm@26-05-5-1 sysconfdir=/etc/slurm

  concretizer:
    unify: true
```

For GPU clusters with NVIDIA hardware:

```yaml
spack:
  repos:
    slurm_factory:
      git: https://github.com/vantagecompute/slurm-factory-spack-repo.git
      branch: main

  specs:
  - slurm_factory.slurm@26-05-5-1 +nvml sysconfdir=/etc/slurm

  concretizer:
    unify: true
```

### Installing from the Buildcache

Pre-built, GPG-signed binaries are published per OS toolchain at
`https://slurm-factory-spack-binary-cache.vantagecompute.ai/<toolchain>/spack`, where the
toolchain is one of `resolute`, `noble`, `jammy`, `rockylinux10`, `rockylinux9` or `rockylinux8`:

```bash
spack mirror add slurm-factory \
  https://slurm-factory-spack-binary-cache.vantagecompute.ai/noble/spack
spack buildcache keys --install --trust
spack buildcache list --long --variants slurm
spack install --cache-only /<hash>
```

The published Slurm builds are `+nvml +rsmi sysconfdir=/etc/slurm`. See the
[Getting Started guide](https://docs.vantagecompute.ai/developer/slurm-factory-spack-repo/getting-started)
for details.

## Repository Structure

```text
├── README.md
├── justfile                    # Development and release recipes
├── spack-repo-index.yaml       # Repository index configuration
├── pyproject.toml              # Python project metadata
├── docusaurus/                 # Documentation site
├── tests/                      # Repository tests
└── spack_repo
    └── slurm_factory           # Main repository namespace
        ├── repo.yaml           # Repository metadata
        └── packages
            ├── slurm/          # Slurm workload manager
            ├── curl/           # URL transfer tool
            ├── freeipmi/       # IPMI hardware management
            ├── openssl/        # OpenSSL cryptographic library
            ├── s2n_tls/        # s2n-tls TLS library
            ├── pyxis/          # Pyxis SPANK plugin
            └── cuda/           # CUDA (builtin plus newer releases)
```

## Available Packages

### slurm

Enhanced Slurm workload manager with a fixed production feature set and relocatable RPATHs.

**Available versions** (SchedMD tag style; `26-05-5-1` builds `slurm-26.05.5.tar.bz2`):

- `26-05-5-1`: Slurm 26.05.5 (latest)
- `26-05-4-1`: Slurm 26.05.4
- `26-05-0-1`: Slurm 26.05.0

**Key features:**

- Full accounting support with MySQL backend
- InfluxDB metrics integration
- PMIx process management interface
- HDF5 profiling support
- JWT authentication
- REST API daemon (slurmrestd)
- Hardware locality (hwloc) support
- FreeIPMI energy accounting, Lua and Kafka support
- TLS through s2n-tls
- GPU support (NVIDIA NVML and AMD ROCm SMI)

### freeipmi

IPMI library for out-of-band hardware management.

### openssl

OpenSSL toolkit for secure communications.

### curl

Command-line URL transfer utility with LDAP and SSH support.

### s2n-tls

AWS's C99 TLS implementation, linked against this repository's OpenSSL, with `$ORIGIN`
RPATHs for relocatable deployments.

### pyxis

NVIDIA's SPANK plugin for running containerized tasks with Enroot, built against
`slurm_factory.slurm`.

## Development

The repository is driven by a [justfile](justfile); `just` lists every recipe.

```bash
just check        # lint, typecheck and tests, as CI runs them
just docs-build   # build the docs site, including the generated package reference
just docs-dev     # docs development server
```

Releases are cut with `just release X.Y.Z` (or `--docs-only`), which opens a release
branch for review; the tag is pushed from `main` after it merges. See
[Releasing](docusaurus/docs/releasing.md).

## Contributing

Please follow Spack's package development guidelines when contributing to this repository.
Commits follow Conventional Commits, checked in CI against [.commitlintrc.yml](.commitlintrc.yml).

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

Copyright 2025 Vantage Compute, Inc. and contributors.
