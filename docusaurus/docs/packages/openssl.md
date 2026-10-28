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

| Version | Status |
|---------|--------|
| `4.1.0` | Latest; OpenSSL 4 (`libcrypto.so.4`), opt in with `@4.1.0` |
| `3.6.5` | Preferred (default); used by Slurm Factory |
| `3.6.0` | Previous |

## Build Variants

| Variant | Default | Description |
|---------|---------|-------------|
| `certs` | `mozilla` | CA certificates: `mozilla` (from `ca-certificates-mozilla`), `system` (symlink the host's) or `none` |
| `shared` | `true` | Build shared libraries |
| `docs` | `false` | Install docs and manpages |

## Installation

### From Buildcache

OpenSSL is typically installed automatically as a dependency of Slurm:

```bash
# OpenSSL is pulled in automatically
spack install slurm_factory.slurm@26-05-5-1
```

### Standalone Installation

To install OpenSSL directly:

```bash
spack install slurm_factory.openssl
```

## Usage with Slurm

OpenSSL provides:

- **TLS/SSL Support**: Secure communications between Slurm components
- **Authentication**: Cryptographic functions for authentication
- **Certificate Management**: X.509 certificates for node identity

In the Slurm Factory build, OpenSSL is:

- A build, link and run dependency of Slurm itself
- The `libcrypto` behind [s2n-tls](./s2n-tls.md), and so behind Slurm's `tls/s2n` plugin
- The TLS backend of the [curl](./curl.md) package (`tls=openssl`)

## Configuration

OpenSSL typically requires no special configuration for Slurm. However, you may need to configure:

- Certificate paths for TLS
- Cipher suites for security policies
- FIPS mode (if required by compliance)

## Dependencies

OpenSSL has minimal dependencies:

- **zlib**: Compression support
- **Perl** 5.14.0 or newer (build and test)
- **ca-certificates-mozilla** (build, when `certs=mozilla`)
- Build tools (gcc, gmake)

## Package Source

- **Homepage**: [https://www.openssl.org](https://www.openssl.org)
- **Package Definition**: [`packages/openssl/package.py`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/spack_repo/slurm_factory/packages/openssl/package.py)

## License

OpenSSL 3.x is licensed under the Apache License 2.0.

## See Also

- [Slurm Package](./slurm.md): Main Slurm package documentation
- [s2n-tls Package](./s2n-tls.md): TLS library built on this OpenSSL
- [Getting Started](../getting-started.md): Installation guide
