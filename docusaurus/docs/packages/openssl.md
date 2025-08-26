# OpenSSL Package

This package provides custom OpenSSL builds optimized for use with Slurm and related dependencies.

## Overview

OpenSSL is a robust, commercial-grade, full-featured toolkit for general-purpose cryptography and secure communication. This custom package ensures compatibility and optimization for Slurm deployments.

## Why a Custom Package?

The custom OpenSSL package in this repository:

- Ensures version compatibility with Slurm requirements
- Optimizes build flags for production use
- Maintains consistent dependency chains
- Supports relocatable installations

## Available Versions

The package supports multiple OpenSSL versions to maintain compatibility with different Slurm releases. Check the package definition for currently supported versions.

## Installation

### From Buildcache

OpenSSL is typically installed automatically as a dependency of Slurm:

```bash
# OpenSSL is pulled in automatically
spack install slurm@25-11-0-1
```

### Standalone Installation

To install OpenSSL directly:

```bash
spack install slurm_factory.openssl
```

## Usage with Slurm

OpenSSL provides:

- **TLS/SSL Support** - Secure communications between Slurm components
- **Authentication** - Cryptographic functions for authentication
- **Certificate Management** - X.509 certificates for node identity

Slurm uses OpenSSL for:

- Munge authentication backend
- slurmrestd HTTPS support
- Secure RPC communications (future Slurm versions)

## Configuration

OpenSSL typically requires no special configuration for Slurm. However, you may need to configure:

- Certificate paths for TLS
- Cipher suites for security policies
- FIPS mode (if required by compliance)

## Dependencies

OpenSSL has minimal dependencies:

- **zlib** - Compression support
- Build tools (gcc, make, perl)

## Package Source

- **Homepage**: [https://www.openssl.org](https://www.openssl.org)
- **Package Definition**: [`packages/openssl/package.py`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/spack_repo/slurm_factory/packages/openssl/package.py)

## License

OpenSSL is dual-licensed under the Apache License 2.0 and the OpenSSL License.

## See Also

- [Slurm Package](./slurm) - Main Slurm package documentation
- [Getting Started](../getting-started) - Installation guide
