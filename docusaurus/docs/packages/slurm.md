# Slurm Package

The Slurm package in this repository provides an enhanced version of the [Slurm Workload Manager](https://slurm.schedmd.com) with additional build variants, production-ready patches, and optimized dependency management.

## Overview

Slurm (Simple Linux Utility for Resource Management) is an open-source, fault-tolerant, and highly scalable cluster management and job scheduling system for Linux clusters.

This custom package extends the standard Spack Slurm package with:

- Additional build variants for modern features
- Production-tested patches
- Optimized RPATH configuration for relocatability
- Enhanced dependency management
- Pre-built binaries in the public buildcache

## Available Versions

| Version | Release Date | Status |
|---------|--------------|--------|
| 25-11-0-1 | 2025-11 | Latest |
| 24-11-6-1 | 2024-11 | Stable |
| 23-11-11-1 | 2023-11 | Stable |

Older versions may be deprecated due to security vulnerabilities (CVE-2022-29500, CVE-2022-29501, CVE-2022-29502, CVE-2021-31215).

## Build Variants

The Slurm package supports numerous build variants to customize your installation:

### Core Features

| Variant | Default | Description |
|---------|---------|-------------|
| `sysconfdir` | `PREFIX/etc` | System configuration directory (e.g., `/etc/slurm`) |
| `readline` | `true` | Enable readline support for interactive commands |

### Scheduler & Plugins

| Variant | Default | Description |
|---------|---------|-------------|
| `pmix` | `false` | Enable PMIx support for MPI integration |
| `lua` | `false` | Enable Lua scripting support for job submit plugins |
| `kafka` | `false` | Enable Kafka profiling plugin for job accounting |
| `mcs` | `false` | Enable MCS support for Kubernetes integration |

### Monitoring & Hardware

| Variant | Default | Description |
|---------|---------|-------------|
| `hwloc` | `false` | Enable hwloc for hardware topology detection |
| `nvml` | `false` | Enable NVIDIA GPU support via NVML |
| `rsmi` | `false` | Enable AMD GPU support via ROCm SMI |
| `ipmi` | `false` | Enable IPMI support for hardware monitoring via FreeIPMI |
| `cgroup` | `false` | Enable cgroup plugin for resource isolation |

### Database & APIs

| Variant | Default | Description |
|---------|---------|-------------|
| `mariadb` | `false` | Use MariaDB instead of MySQL for accounting database |
| `hdf5` | `false` | Enable HDF5 support for profiling data |
| `restd` | `false` | Enable slurmrestd REST API server |

### Security & Authentication

| Variant | Default | Description |
|---------|---------|-------------|
| `pam` | `false` | Enable PAM support for authentication |
| `certs` | `false` | Enable certificate generation (Slurm >= 24.11) |

### UI

| Variant | Default | Description |
|---------|---------|-------------|
| `gtk` | `false` | Enable GTK+ support for GUI tools |

## Installation Examples

### Basic Installation

Install the latest Slurm with default options:

```bash
spack install slurm@25-11-0-1
```

### Production Configuration

Install with common production features:

```bash
spack install slurm@25-11-0-1 \\
  +pmix \\           # MPI integration
  +hwloc \\          # Hardware topology
  +restd \\          # REST API
  +pam \\            # PAM authentication
  +cgroup \\         # Resource isolation
  sysconfdir=/etc/slurm
```

### GPU Cluster

For NVIDIA GPU clusters:

```bash
spack install slurm@25-11-0-1 +nvml +hwloc +pmix
```

For AMD GPU clusters:

```bash
spack install slurm@25-11-0-1 +rsmi +hwloc +pmix
```

### Kubernetes Integration

For Kubernetes-integrated clusters:

```bash
spack install slurm@25-11-0-1 +mcs +restd +hwloc
```

### Advanced Monitoring

With IPMI hardware monitoring and Kafka profiling:

```bash
spack install slurm@25-11-0-1 \\
  +ipmi \\           # Hardware monitoring via IPMI
  +kafka \\          # Job profiling to Kafka
  +hwloc \\          # Hardware topology
  +hdf5              # HDF5 profiling data
```

### Development/Testing

Minimal installation for development:

```bash
spack install slurm@25-11-0-1 +readline +hwloc
```

## Dependencies

### Required Dependencies

Always included:

- **curl** (with LDAP support) - Required for InfluxDB plugin
- **MySQL** - Database for job accounting
- **OpenSSL** - Cryptography and secure communications
- **Munge** - Authentication service
- **JSON-C** - JSON parsing
- **LZ4** - Compression
- **ncurses** - Terminal handling
- **glib** - Core libraries
- **libssh2** - SSH protocol support
- **libjwt** - JWT authentication tokens
- **zlib** - Compression

### Optional Dependencies

Enabled by variants:

- **PMIx** (`+pmix`) - Process management interface
- **hwloc** (`+hwloc`) - Hardware locality/topology
- **Lua** (`+lua`) - Scripting support
- **librdkafka** (`+kafka`) - Kafka client library
- **FreeIPMI** (`+ipmi`) - IPMI hardware monitoring
- **CUDA** (`+nvml`) - NVIDIA GPU support
- **ROCm SMI** (`+rsmi`) - AMD GPU support
- **D-Bus** (`+cgroup`) - Cgroup plugin
- **Linux PAM** (`+pam`) - Authentication
- **HDF5** (`+hdf5`) - Hierarchical data format
- **http-parser** (`+restd`) - HTTP parsing for REST API
- **libyaml** (`+restd`) - YAML parsing for REST API
- **GTK+** (`+gtk`) - GUI toolkit

## Configuration Files

After installation, Slurm requires configuration files in the `sysconfdir` directory:

- `slurm.conf` - Main configuration file
- `slurmdbd.conf` - Database daemon configuration
- `cgroup.conf` - Cgroup plugin configuration (if `+cgroup`)
- `topology.conf` - Network topology (optional)
- `gres.conf` - Generic resource configuration (for GPUs, etc.)

Example `slurm.conf` location:

```bash
# Default (if sysconfdir=PREFIX/etc)
$(spack location -i slurm)/etc/slurm.conf

# Custom (if sysconfdir=/etc/slurm)
/etc/slurm/slurm.conf
```

## Relocatability

This package is built with proper RPATH configuration, making it relocatable. You can:

- Install to a temporary location and move it later
- Create tarballs for deployment on other systems
- Use with container images

The package includes RPATH entries for:

- `$ORIGIN/../lib/slurm` - Internal Slurm libraries
- Dependency library paths

## Build from Source vs. Buildcache

### From Buildcache (Recommended)

Fast installation from pre-built binaries:

```bash
spack install --cache-only slurm@25-11-0-1
```

### From Source

Build with custom variants (takes several hours):

```bash
spack install slurm@25-11-0-1 +pmix +hwloc +restd +ipmi
```

## Package Source

- **Homepage**: [https://slurm.schedmd.com](https://slurm.schedmd.com)
- **Source**: [https://github.com/SchedMD/slurm](https://github.com/SchedMD/slurm)
- **Package Definition**: [`packages/slurm/package.py`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/spack_repo/slurm_factory/packages/slurm/package.py)

## License

Slurm is licensed under GPL-2.0-or-later.

## Known Issues

### CVE Deprecations

Versions prior to the following are deprecated due to security vulnerabilities:

- **&lt; 20.11.9** or **&lt; 21.08.8**: CVE-2022-29500, CVE-2022-29501, CVE-2022-29502
- **&lt; 20.02.7** or **&lt; 20.11.7**: CVE-2021-31215

Always use the latest patch release for your version series.

### Compiler Compatibility

GCC 10+ requires the `-fcommon` flag for Slurm versions &lt;= 20.02.1. This is automatically handled by the package.

## See Also

- [Getting Started](../getting-started) - Installation guide
- [OpenSSL Package](./openssl) - Custom OpenSSL for dependencies
- [FreeIPMI Package](./freeipmi) - IPMI support
- [Slurm Documentation](https://slurm.schedmd.com/documentation.html) - Official Slurm docs
