# Slurm Factory Spack Repository

Welcome to the Slurm Factory Spack Repository, a custom Spack repository providing enhanced Slurm packages and dependencies for production HPC deployments. It is the package source that [Slurm Factory](https://github.com/vantagecompute/slurm-factory) builds from.

## What is This Repository

This repository provides:

- **Custom Spack Packages**: Slurm, plus the dependencies whose upstream Spack recipes do not build the way Slurm Factory needs (curl, FreeIPMI, OpenSSL, s2n-tls) and the Pyxis SPANK plugin
- **Pre-built Binaries**: A public, GPG-signed Spack buildcache that Slurm Factory publishes from these recipes
- **Multiple Versions**: Slurm 23.11, 24.11, 25.11 and 26.05
- **Relocatable Builds**: RPATHs set up so installs work from Spack views and tarballs

## Key Features

- **Fast Deployment**: Install from the buildcache instead of compiling Slurm and its dependency tree
- **Relocatable Packages**: `$ORIGIN`-relative RPATHs for Slurm plugins and libraries
- **GPG Signed**: Every package in the buildcache is signed
- **Batteries Included**: Accounting (MySQL client), slurmrestd, PMIx, HDF5 and InfluxDB profiling, JWT, hwloc, FreeIPMI, Lua and Kafka support are built in, with TLS through s2n-tls on Slurm 25.11 and newer
- **GPU Variants**: NVIDIA NVML and AMD ROCm SMI support

## Quick Start

### Option 1: Install from Buildcache (Recommended)

The buildcache is organized by OS toolchain. Pick the one matching your host (here Ubuntu 24.04, `noble`):

```bash
# Install Spack
git clone --depth 1 --branch v1.0.0 https://github.com/spack/spack.git ~/spack
source ~/spack/share/spack/setup-env.sh

# Add this repository
git clone https://github.com/vantagecompute/slurm-factory-spack-repo.git
spack repo add slurm-factory-spack-repo/spack_repo/slurm_factory

# Add the buildcache mirror for your toolchain
spack mirror add slurm-factory \
  https://slurm-factory-spack-binary-cache.vantagecompute.ai/noble/spack

# Trust the signing key
spack buildcache keys --install --trust

# Find the Slurm build you want and install it by hash
spack buildcache list --long --variants slurm
spack install --cache-only /<hash>
```

See the [Getting Started Guide](./getting-started.md) for the full walkthrough.

### Option 2: Build from Source

For custom configurations:

```bash
# After adding the repository (see above)
spack install slurm_factory.slurm@26-05-5-1 +nvml sysconfdir=/etc/slurm
```

## Available Packages

### slurm

Enhanced Slurm workload manager with production optimizations.

**Versions:**

- `26-05-5-1`: Latest (Slurm 26.05.5)
- `26-05-4-1`: Slurm 26.05.4
- `26-05-0-1`: Slurm 26.05.0
- `25-11-6-1`: Slurm 25.11.6
- `24-11-6-1`: Slurm 24.11.6
- `23-11-11-1`: Slurm 23.11.11

**Variants:**

- `sysconfdir`: Configuration directory (default: `PREFIX/etc`)
- `gtk`: GTK+ support for GUI tools
- `nvml`: NVIDIA GPU support
- `rsmi`: AMD ROCm GPU support

See the [Slurm Package Documentation](./packages/slurm.md) for details.

### curl

Command-line URL transfer utility with LDAP support (required for Slurm's InfluxDB plugin).

See the [curl Package Documentation](./packages/curl.md) for details.

### freeipmi

IPMI library for out-of-band hardware management.

See the [FreeIPMI Package Documentation](./packages/freeipmi.md) for details.

### openssl

OpenSSL toolkit for secure communications.

See the [OpenSSL Package Documentation](./packages/openssl.md) for details.

### s2n-tls

AWS's C99 TLS implementation, used by Slurm's `tls/s2n` plugin on Slurm 25.11 and newer.

See the [s2n-tls Package Documentation](./packages/s2n-tls.md) for details.

### pyxis

NVIDIA's SPANK plugin for running containerized tasks with Enroot through `srun`.

See the [Pyxis Package Documentation](./packages/pyxis.md) for details.

## Repository Structure

```text
slurm-factory-spack-repo/
├── spack-repo-index.yaml        # Points Spack at spack_repo/slurm_factory
├── spack_repo/
│   └── slurm_factory/           # The Spack repository (namespace slurm_factory)
│       ├── repo.yaml            # Repository metadata
│       └── packages/
│           ├── slurm/           # Slurm package
│           ├── curl/            # curl package
│           ├── freeipmi/        # FreeIPMI package
│           ├── openssl/         # OpenSSL package
│           ├── s2n_tls/         # s2n-tls package
│           └── pyxis/           # Pyxis package
├── scripts/                     # Repository tooling (license headers)
├── tests/                       # Repository tests
├── docusaurus/                  # This documentation
├── justfile                     # Development and release recipes
└── README.md
```

## Public Buildcache

All packages are available in the public buildcache at:

`https://slurm-factory-spack-binary-cache.vantagecompute.ai/`

There is one Spack mirror per OS toolchain, at `<toolchain>/spack`. Each mirror holds every supported Slurm series for both `x86_64` and `aarch64`, together with the dependencies and the GCC that built them.

### Supported Toolchains

| Toolchain | OS | GCC | Mirror URL |
|-----------|----|-----|------------|
| `resolute` | Ubuntu 26.04 | 15.2.0 | `https://slurm-factory-spack-binary-cache.vantagecompute.ai/resolute/spack` |
| `noble` | Ubuntu 24.04 | 13.3.0 | `https://slurm-factory-spack-binary-cache.vantagecompute.ai/noble/spack` |
| `jammy` | Ubuntu 22.04 | 11.4.0 | `https://slurm-factory-spack-binary-cache.vantagecompute.ai/jammy/spack` |
| `rockylinux10` | Rocky Linux 10 | 14.3.1 | `https://slurm-factory-spack-binary-cache.vantagecompute.ai/rockylinux10/spack` |
| `rockylinux9` | Rocky Linux 9 | 11.5.0 | `https://slurm-factory-spack-binary-cache.vantagecompute.ai/rockylinux9/spack` |
| `rockylinux8` | Rocky Linux 8 | 8.5.0 | `https://slurm-factory-spack-binary-cache.vantagecompute.ai/rockylinux8/spack` |

**Slurm series**: 26.05, 25.11, 24.11 and 23.11, built as `26-05-5-1`, `25-11-6-1`, `24-11-6-1` and `23-11-11-1`.

:::note
Slurm Factory publishes the GPU build, so the cached Slurm specs are `+nvml +rsmi sysconfdir=/etc/slurm`. A spec with different variants will not match the cache and is built from source.
:::

## GPG Package Signing

All packages in the buildcache are signed with GPG:

- **Authenticity**: Verify packages were built by Vantage Compute
- **Integrity**: Detect tampering or corruption during download
- **Trust Chain**: Establish provenance for production deployments

Import and trust the key with `spack buildcache keys --install --trust`. The signing key fingerprint is `FDEA90667641505264EFD114DFB92630BCA5AB71`.

## Use Cases

- **HPC Cluster Deployment**: Deploy Slurm on compute clusters with minimal build time
- **CI/CD Testing**: Test Slurm configurations in containerized environments
- **Development**: Quick Slurm installations for development and testing
- **Multi-version Management**: Maintain multiple Slurm versions side-by-side

## Installation Examples

### Basic CPU Cluster

```bash
spack install slurm_factory.slurm@26-05-5-1 sysconfdir=/etc/slurm
```

### GPU Cluster with NVIDIA Support

```bash
spack install slurm_factory.slurm@26-05-5-1 +nvml sysconfdir=/etc/slurm
```

### Full Featured Deployment

```bash
spack install slurm_factory.slurm@26-05-5-1 \
  +nvml +rsmi +gtk sysconfdir=/etc/slurm %gcc@15.2.0
```

## Requirements

### For Using Buildcache

- Linux on `x86_64` or `aarch64`, matching one of the toolchains above
- Spack 1.0.0 or later
- Internet connection for downloading packages

### For Building from Source

- All buildcache requirements, plus:
- 50GB disk space
- 4+ CPU cores, 16GB RAM recommended
- Build tools (gcc, make, cmake)

## Next Steps

- [Getting Started Guide](./getting-started.md): Detailed installation instructions
- [Package Documentation](./packages/slurm.md): Explore available packages and variants
- [Contributing Guide](./contributing.md): Contribute to the repository
- [Contact](./contact.md): Get help or report issues

## Related Projects

- [Slurm Factory](https://github.com/vantagecompute/slurm-factory): Build system for creating Slurm binaries
- [Spack](https://spack.io): The package manager powering this repository
- [Slurm](https://slurm.schedmd.com): The workload manager we're packaging

## License

This project is licensed under the Apache License, Version 2.0.

Copyright 2025 Vantage Compute, Inc. and contributors.
