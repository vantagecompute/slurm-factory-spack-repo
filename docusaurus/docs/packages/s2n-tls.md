# s2n-tls Package

This package provides s2n-tls, Amazon's C99 TLS implementation, for use with Slurm's `tls/s2n` plugin.

## Overview

[s2n-tls](https://github.com/aws/s2n-tls) is a C99 implementation of the TLS/SSL protocols designed to be simple, small, fast, and with security as a priority. Starting with Slurm 25.11, the `tls/s2n` plugin is the recommended TLS backend for secure communications between Slurm daemons.

## Why a Custom Package?

The custom s2n-tls package in this repository:

- Ensures s2n-tls links against the **spack-built OpenSSL** (not the system one), preventing version mismatch errors like `OPENSSL_3.6.0 not found`
- Adds `$ORIGIN`-relative RPATHs for relocatable deployments via spack views and tarballs
- Disables test builds to streamline compilation in the spack environment
- Provides verified linkage diagnostics during the install phase

## The Problem This Solves

When `libs2n.so` is built against OpenSSL 3.6.0 but deployed on a system with an older OpenSSL (e.g., 3.0.x on Ubuntu Noble), Slurm commands fail with:

```
sinfo: error: certgen/script: openssl: version `OPENSSL_3.6.0' not found
sinfo: fatal: failed to initialize tls plugin
```

This package ensures `libs2n.so` always resolves to the correct spack-built `libcrypto.so.3` at runtime, regardless of the deployment method.

## Available Versions

| Version | Status |
|---------|--------|
| 1.5.14  | Latest |

## Installation

### As a Slurm Dependency

s2n-tls is automatically installed as a dependency of Slurm >= 25.11:

```bash
spack install slurm@25-11-2-1
```

### Standalone Installation

To install s2n-tls directly:

```bash
spack install slurm_factory.s2n-tls
```

## Build Variants

| Variant | Default | Description |
|---------|---------|-------------|
| `shared` | `true` | Build shared libraries (`libs2n.so`) |

## Dependencies

- **OpenSSL** — Cryptographic backend (`libcrypto.so`)
- **CMake** (build only) — Build system
- **patchelf** (build only) — RPATH fixup for relocatable deployments

## How It Works with Slurm

Slurm's `tls/s2n` plugin (`tls_s2n.so`) loads `libs2n.so.1` at runtime, which in turn needs `libcrypto.so.3` from OpenSSL. The library resolution chain is:

```
tls_s2n.so  →  libs2n.so.1  →  libcrypto.so.3 (OpenSSL)
```

In a spack view or tarball deployment, the libraries are laid out as:

```
<prefix>/lib/slurm/tls_s2n.so    # Slurm plugin
<prefix>/lib/libs2n.so.1          # s2n-tls library
<prefix>/lib64/libcrypto.so.3     # spack-built OpenSSL
```

This package configures RPATHs with `$ORIGIN`-relative entries so each library can find the next in the chain without relying on absolute paths or `LD_LIBRARY_PATH`.

## RPATH Configuration

The package sets the following RPATHs on `libs2n.so`:

| RPATH Entry | Purpose |
|-------------|---------|
| `$ORIGIN` | Same directory as `libs2n.so` |
| `$ORIGIN/../lib64` | OpenSSL 3.x on x86_64 (installs to `lib64/`) |
| `$ORIGIN/../lib/private` | Spack view conflict resolution directory |
| `<openssl_prefix>/lib64` | Absolute path for spack environment use |

## Package Source

- **Homepage**: [https://github.com/aws/s2n-tls](https://github.com/aws/s2n-tls)
- **Package Definition**: [`packages/s2n-tls/package.py`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/spack_repo/slurm_factory/packages/s2n-tls/package.py)

## License

s2n-tls is licensed under the Apache License 2.0.

## See Also

- [Slurm Package](./slurm) — Main Slurm package documentation
- [OpenSSL Package](./openssl) — OpenSSL dependency
- [Getting Started](../getting-started) — Installation guide
