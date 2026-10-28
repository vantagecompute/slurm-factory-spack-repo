# Slurm Package

The Slurm package in this repository provides an enhanced build of the [Slurm Workload Manager](https://slurm.schedmd.com) with a fixed, production-oriented feature set, relocatable RPATHs and managed dependencies.

## Overview

Slurm (Simple Linux Utility for Resource Management) is an open-source, fault-tolerant, and highly scalable cluster management and job scheduling system for Linux clusters.

Compared with the upstream Spack `slurm` package, this one:

- Builds every integration Slurm Factory ships (accounting, slurmrestd, PMIx, HDF5, InfluxDB, JWT, hwloc, FreeIPMI, Lua, Kafka, PAM) unconditionally, instead of behind variants
- Enables the `tls/s2n` TLS plugin on Slurm 25.11 and newer, linked against this repository's [s2n-tls](./s2n-tls.md)
- Builds and installs `libslurm_curl.so` and relinks the InfluxDB profiling plugin against it
- Installs the `pmi2` and `nss_slurm` contribs
- Sets `$ORIGIN`-relative RPATHs for relocatability
- Has pre-built binaries in the public buildcache

## Available Versions

Versions are named after SchedMD's release tags (`X-Y-Z-1`). The package maps each one to the release tarball on `download.schedmd.com`, so `26-05-5-1` builds `slurm-26.05.5.tar.bz2`.

| Version | Slurm release | Status |
|---------|---------------|--------|
| `26-05-5-1` | 26.05.5 | Latest; Slurm Factory's 26.05 build |
| `26-05-4-1` | 26.05.4 | |
| `26-05-0-1` | 26.05.0 | |
| `25-11-6-1` | 25.11.6 | Slurm Factory's 25.11 build |
| `24-11-6-1` | 24.11.6 | Slurm Factory's 24.11 build |
| `23-11-11-1` | 23.11.11 | Slurm Factory's 23.11 build |

:::note
Only the versions above are defined. The older, CVE-affected releases that upstream Spack's `slurm` package still lists are not carried here.
:::

## Build Variants

| Variant | Default | Description |
|---------|---------|-------------|
| `sysconfdir` | `PREFIX/etc` | System configuration directory (e.g., `/etc/slurm`) |
| `gtk` | `false` | Enable GTK+ support (`sview`) |
| `nvml` | `false` | Enable NVIDIA GPU autodetection via NVML (adds a `cuda` dependency) |
| `rsmi` | `false` | Enable AMD GPU support via ROCm SMI (adds a `rocm-smi-lib` dependency) |

### Always-On Features

These are configured on every build and have no variant:

- slurmrestd (`--enable-slurmrestd`, with http-parser)
- Accounting storage through the MySQL client library
- PMIx (`pmix@:5`)
- HDF5 job profiling
- InfluxDB job profiling through `libslurm_curl.so`
- JWT authentication (libjwt)
- hwloc topology
- FreeIPMI (for `acct_gather_energy/ipmi`)
- Lua (job submit plugins)
- Kafka (librdkafka)
- PAM and multiple-slurmd support
- `tls/s2n` on Slurm 25.11 and newer

## Installation Examples

### Basic Installation

Install the latest Slurm with default options:

```bash
spack install slurm_factory.slurm@26-05-5-1
```

### Production Configuration

Install with the configuration directory most deployments use:

```bash
spack install slurm_factory.slurm@26-05-5-1 sysconfdir=/etc/slurm
```

### GPU Cluster

For NVIDIA GPU clusters:

```bash
spack install slurm_factory.slurm@26-05-5-1 +nvml sysconfdir=/etc/slurm
```

For AMD GPU clusters:

```bash
spack install slurm_factory.slurm@26-05-5-1 +rsmi sysconfdir=/etc/slurm
```

This is the spec Slurm Factory builds and publishes to the buildcache:

```bash
spack install slurm_factory.slurm@26-05-5-1 +nvml +rsmi sysconfdir=/etc/slurm
```

### With GUI Tools

```bash
spack install slurm_factory.slurm@26-05-5-1 +gtk
```

## Dependencies

### Always Included

- **curl** (`libs=shared,static +nghttp2 +libssh2 +ldap`): Without LDAP, Slurm's configure does not set `WITH_CURL` and the InfluxDB plugin fails to link
- **MySQL** (`mysql@8.0.35 +client_only`): Client library for job accounting
- **OpenSSL**: Cryptography and secure communications
- **Munge**: Authentication service
- **PMIx** (`pmix@:5`): Process management interface
- **hwloc**: Hardware locality and topology
- **HDF5**: Profiling data
- **libjwt**: JWT authentication tokens
- **FreeIPMI**: IPMI hardware monitoring
- **Lua**: Scripting support
- **librdkafka**: Kafka client library
- **http-parser** and **libyaml**: slurmrestd
- **D-Bus**: Cgroup plugin
- **Linux PAM**: PAM authentication
- **JSON-C**, **LZ4**, **ncurses**, **readline**, **glib**, **libssh2**, **zlib**

### Slurm 25.11 and Newer

- **s2n-tls**: Backend for the `tls/s2n` plugin
- **patchelf** `@:0.17` (build only): Fixes the RPATH of `tls_s2n.so`. Versions from 0.18 leave misaligned load segments that the glibc 2.28 loader on Rocky Linux 8 rejects.

### Variant Dependencies

- **CUDA** (`+nvml`): NVIDIA GPU support
- **ROCm SMI** (`+rsmi`): AMD GPU support
- **GTK+** (`+gtk`): GUI toolkit

## Configuration Files

After installation, Slurm requires configuration files in the `sysconfdir` directory:

- `slurm.conf`: Main configuration file
- `slurmdbd.conf`: Database daemon configuration
- `cgroup.conf`: Cgroup plugin configuration
- `topology.conf`: Network topology (optional)
- `gres.conf`: Generic resource configuration (for GPUs, etc.)

Example `slurm.conf` location:

```bash
# Default (if sysconfdir=PREFIX/etc)
$(spack location -i slurm)/etc/slurm.conf

# Custom (if sysconfdir=/etc/slurm)
/etc/slurm/slurm.conf
```

## Relocatability

This package is built with RPATH configuration that makes it relocatable. You can:

- Install to a temporary location and move it later
- Create tarballs for deployment on other systems
- Use with container images

The package sets:

- `$ORIGIN/../lib/slurm` on Slurm's binaries, for `libslurmfull.so` and the other internal libraries
- `$ORIGIN/..` on the `tls_s2n.so` plugin (Slurm 25.11 and newer), so it finds `libs2n.so` in `lib/` of a view or tarball
- RPATHs for curl, Lua, librdkafka, MySQL and s2n-tls library directories

## Build from Source vs. Buildcache

### From Buildcache (Recommended)

Fast installation from pre-built binaries. The cached builds are `+nvml +rsmi sysconfdir=/etc/slurm`, built with the toolchain's GCC (13.3.0 on Ubuntu 24.04):

```bash
spack install --cache-only \
  slurm_factory.slurm@26-05-5-1 +nvml +rsmi sysconfdir=/etc/slurm %gcc@13.3.0
```

See [Getting Started](../getting-started.md) for adding the mirror.

### From Source

Build with your own variants (this can take several hours with all dependencies):

```bash
spack install slurm_factory.slurm@26-05-5-1 +nvml sysconfdir=/etc/slurm
```

## Package Source

- **Homepage**: [https://slurm.schedmd.com](https://slurm.schedmd.com)
- **Source**: Release tarballs from [download.schedmd.com](https://download.schedmd.com/slurm/) ([SchedMD/slurm](https://github.com/SchedMD/slurm) on GitHub)
- **Package Definition**: [`packages/slurm/package.py`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/spack_repo/slurm_factory/packages/slurm/package.py)

## License

Slurm is licensed under GPL-2.0-or-later.

## See Also

- [Getting Started](../getting-started.md): Installation guide
- [s2n-tls Package](./s2n-tls.md): TLS backend for Slurm 25.11 and newer
- [OpenSSL Package](./openssl.md): Custom OpenSSL for dependencies
- [FreeIPMI Package](./freeipmi.md): IPMI support
- [Pyxis Package](./pyxis.md): Container support through Enroot
- [Slurm Documentation](https://slurm.schedmd.com/documentation.html): Official Slurm docs
