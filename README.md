<div align="center">
<a href="https://www.vantagecompute.ai/">
  <img src="https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-black-horz.png" alt="Vantage Compute Logo" width="100"/>
</a>

# Slurm Factory Spack Repository

[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-24.0+-blue.svg)](https://docker.com)

Spack Repository for use with Vantage Compute Slurm Factory.

[Documentation](https://vantagecompute.github.io/slurm-factory-spack-repo) | [Buildcache](https://slurm-factory-spack-binary-cache.vantagecompute.ai)

</div>

## Overview

This repository provides custom Spack packages for use with Vantage Compute's Slurm-Factory. The custom packes included in this repo include:

- **slurm**: Enhanced Slurm workload manager with custom patches and optimizations
- **freeipmi**: IPMI library for hardware management
- **openssl**: OpenSSL cryptographic library
- **curl**: Command-line tool for transferring data with URLs

## Installation

### Adding the Repository

Add this repository to your Spack configuration in one of two ways:

#### Option 1: Using spack.yaml

Add to your `spack.yaml` or `spack/spack.yaml`:

```yaml
spack:
  repos:
  - https://github.com/vantagecompute/slurm-factory-spack-repo.git
  
  specs:
  - slurm@25-11-0-1 sysconfdir=/etc/slurm %gcc@13.4.0
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
```

### Slurm Variants

The Slurm package supports the following variants:

- `sysconfdir`: System configuration path (default: `PREFIX/etc`, commonly set to `/etc/slurm`)
- `gtk`: Enable GTK+ support (default: `False`)
- `nvml`: Enable NVIDIA NVML GPU detection (default: `False`)
- `rsmi`: Enable AMD ROCm SMI GPU support (default: `False`)

### Example Configuration

Here's a complete example for installing Slurm with production features:

```yaml
spack:
  repos:
  - https://github.com/vantagecompute/slurm-factory-spack-repo.git
  
  specs:
  - slurm_factory.slurm@23-11-11-1 sysconfdir=/etc/slurm %gcc@13.4.0
  
  concretizer:
    unify: true
```

For GPU clusters with NVIDIA hardware:

```yaml
spack:
  repos:
  - https://github.com/vantagecompute/slurm-factory-spack-repo.git
  
  specs:
  - slurm_factory.slurm@24-11-6-1 +nvml sysconfdir=/etc/slurm %gcc@13.4.0
  
  concretizer:
    unify: true
```

## Repository Structure

```text
├── README.md
├── spack-repo-index.yaml       # Repository index configuration
├── pyproject.toml              # Python project metadata
└── spack_repo
    └── slurm_factory           # Main repository namespace
        ├── repo.yaml           # Repository metadata
        └── packages
            ├── slurm/          # Slurm workload manager
            ├── freeipmi/       # IPMI hardware management
            ├── openssl/        # OpenSSL cryptographic library
            └── curl/           # URL transfer tool
```

## Available Packages

### slurm

Enhanced Slurm workload manager with custom patches and optimizations.

**Available versions:**

- `25-11-0-1` - Slurm 25.11.0-1
- `24-11-6-1` - Slurm 24.11.6-1
- `23-11-11-1` - Slurm 23.11.11-1

**Key features:**

- Full accounting support with MySQL backend
- InfluxDB metrics integration
- PMIx process management interface
- HDF5 profiling support
- JWT authentication
- REST API daemon (slurmrestd)
- Hardware locality (hwloc) support
- GPU support (NVIDIA NVML and AMD ROCm SMI)

### freeipmi

IPMI library for out-of-band hardware management.

### openssl

OpenSSL toolkit for secure communications.

### curl

Command-line URL transfer utility with LDAP and SSH support.

## Contributing

Please follow Spack's package development guidelines when contributing to this repository.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

Copyright 2025 Vantage Compute, Inc. and contributors.
