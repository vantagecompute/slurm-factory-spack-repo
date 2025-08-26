# Slurm Factory Spack Repository

Welcome to the Slurm Factory Spack Repository - a custom Spack repository providing enhanced Slurm packages and dependencies for production HPC deployments.

## What is This Repository

This repository provides:

- **Custom Spack Packages**: Enhanced Slurm workload manager with optimized build variants
- **Pre-built Binaries**: Access to public buildcache for instant installation (5-15 minutes vs 45-90 minutes compilation)
- **Multiple Versions**: Support for Slurm 23.11, 24.11, and 25.11
- **Production Ready**: All packages are GPG-signed and tested in production environments

## Key Features

- ⚡ **Instant Deployment**: Install from cache in 5-15 minutes instead of 45-90 minutes of compilation
- 📦 **Relocatable Packages**: Deploy to any filesystem path without recompilation
- 🔒 **GPG Signed**: All packages cryptographically signed for security and integrity
- 🧪 **Production Tested**: Configurations validated in real-world HPC environments
- 🔧 **Custom Variants**: Enhanced build options for GPU support, monitoring, and more

## Quick Start

### Option 1: Install from Buildcache (Recommended)

The fastest way to get Slurm - no compilation required:

```bash
# Install Spack
git clone --depth 1 --branch v1.0.0 https://github.com/spack/spack.git ~/spack
source ~/spack/share/spack/setup-env.sh

# Add this repository
git clone https://github.com/vantagecompute/slurm-factory-spack-repo.git
spack repo add slurm-factory-spack-repo/spack_repo/slurm_factory

# Add buildcache mirror
spack mirror add slurm-factory-slurm \
  https://slurm-factory-spack-binary-cache.vantagecompute.ai/slurm/25.11/15.2.0

# Trust GPG keys
spack buildcache keys --install --trust

# Install Slurm (5-15 minutes)
spack install --cache-only slurm@25-11-0-1
```

### Option 2: Build from Source

For custom configurations:

```bash
# After adding the repository (see above)
spack install slurm_factory.slurm@25-11-0-1 +nvml sysconfdir=/etc/slurm
```

## Available Packages

### slurm

Enhanced Slurm workload manager with production optimizations.

**Versions:**

- `25-11-0-1` - Latest (Slurm 25.11.0-1)
- `24-11-6-1` - Stable (Slurm 24.11.6-1)
- `23-11-11-1` - Stable (Slurm 23.11.11-1)

**Key Variants:**

- `sysconfdir` - Configuration directory (default: `PREFIX/etc`)
- `gtk` - GTK+ support for GUI tools
- `nvml` - NVIDIA GPU support
- `rsmi` - AMD ROCm GPU support

See [Slurm Package Documentation](./packages/slurm) for complete variant list.

### curl

Command-line URL transfer utility with LDAP support (required for Slurm's InfluxDB plugin).

See [curl Package Documentation](./packages/curl) for details.

### freeipmi

IPMI library for out-of-band hardware management.

See [FreeIPMI Package Documentation](./packages/freeipmi) for details.

### openssl

OpenSSL toolkit for secure communications.

See [OpenSSL Package Documentation](./packages/openssl) for details.

## Repository Structure

```text
slurm-factory-spack-repo/
├── spack_repo/
│   └── slurm_factory/           # Main Spack repository
│       ├── repo.yaml            # Repository metadata
│       └── packages/
│           ├── slurm/           # Slurm package
│           ├── curl/            # curl package
│           ├── freeipmi/        # FreeIPMI package
│           └── openssl/         # OpenSSL package
├── scripts/                     # Build and documentation scripts
├── docusaurus/                  # This documentation
└── README.md
```

## Public Buildcache

All packages are available in our public buildcache at:

`https://slurm-factory-spack-binary-cache.vantagecompute.ai/`

### Supported Combinations

- **Slurm Versions**: 23.11, 24.11, 25.11
- **GCC Versions**: 13.3.0, 13.4.0, 15.2.0
- **Total**: 27 version combinations, all GPG-signed

### Build Time Comparison

| Build Type | Dependencies | Size | Build Time | Buildcache Time | Use Case |
|------------|--------------|------|------------|-----------------|----------|
| CPU-only | ~45 packages | 2-5GB | 35-45 min | 5-10 min | Production clusters |
| GPU-enabled | ~180 packages | 15-25GB | 75-90 min | 15-20 min | GPU/CUDA clusters |

## GPG Package Signing

All packages in the buildcache are cryptographically signed with GPG for security:

- **Authenticity**: Verify packages were built by Vantage Compute
- **Integrity**: Detect tampering or corruption during download
- **Security**: Prevent man-in-the-middle attacks
- **Trust Chain**: Establish provenance for production deployments
- **Compliance**: Meets security requirements for regulated environments

Keys are automatically imported when using `spack buildcache keys --install --trust`.

## Use Cases

- **HPC Cluster Deployment** - Deploy Slurm on compute clusters with minimal build time
- **CI/CD Testing** - Test Slurm configurations in containerized environments
- **Development** - Quick Slurm installations for development and testing
- **Multi-version Management** - Maintain multiple Slurm versions side-by-side

## Installation Examples

### Basic CPU Cluster

```bash
spack install slurm_factory.slurm@25-11-0-1 sysconfdir=/etc/slurm
```

### GPU Cluster with NVIDIA Support

```bash
spack install slurm_factory.slurm@25-11-0-1 +nvml sysconfdir=/etc/slurm
```

### Full Featured Deployment

```bash
spack install slurm_factory.slurm@25-11-0-1 \
  +nvml +gtk sysconfdir=/etc/slurm %gcc@15.2.0
```

## Requirements

### For Using Buildcache

- Linux system (Ubuntu 22.04+, RHEL 8+, or similar)
- Spack 1.0.0 or later
- Internet connection for downloading packages

### For Building from Source

- All buildcache requirements, plus:
- 50GB disk space
- 4+ CPU cores, 16GB RAM recommended
- Build tools (gcc, make, cmake)

## Next Steps

- [Getting Started Guide](./getting-started) - Detailed installation instructions
- [Package Documentation](./packages/slurm) - Explore available packages and variants
- [Contributing Guide](./contributing) - Contribute to the repository
- [Contact](./contact) - Get help or report issues

## Related Projects

- [Slurm Factory](https://github.com/vantagecompute/slurm-factory) - Build system for creating Slurm binaries
- [Spack](https://spack.io) - The package manager powering this repository
- [Slurm](https://slurm.schedmd.com) - The workload manager we're packaging

## License

This project is licensed under the Apache License, Version 2.0.

Copyright 2025 Vantage Compute, Inc. and contributors.
