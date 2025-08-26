# curl

Command-line tool and library for transferring data with URLs.

## Overview

This package provides a custom build of curl optimized for Slurm Factory, with LDAP and SSH2 support enabled by default.

## Package Information

- **Homepage**: [https://curl.se/](https://curl.se/)
- **Source**: Built from official curl releases
- **License**: MIT/X derivate license

## Variants

The curl package supports the following build variants:

- `tls`: TLS backend (default: `openssl`)
- `nghttp2`: Enable HTTP/2 support (default: `True`)
- `libssh2`: Enable SSH2 protocol support (default: `False`)
- `libssh`: Enable libssh support (default: `False`)
- `gssapi`: Enable Kerberos/GSSAPI support (default: `False`)
- `ldap`: Enable LDAP protocol support (default: `False`)
- `libidn2`: Enable IDN support (default: `False`)
- `librtmp`: Enable RTMP protocol support (default: `False`)

## Usage

### Basic Installation

```bash
spack install slurm_factory.curl
```

### With LDAP Support (Required for Slurm)

```bash
spack install slurm_factory.curl +ldap +libssh2 +nghttp2
```

## Dependencies

curl has minimal dependencies, primarily:

- **OpenSSL** - TLS/SSL support
- **zlib** - Compression support

Additional dependencies based on variants:

- **nghttp2** - HTTP/2 support (when `+nghttp2`)
- **libssh2** - SSH protocol support (when `+libssh2`)
- **openldap** - LDAP protocol support (when `+ldap`)

## Why This Package Exists

The Slurm Factory curl package ensures LDAP support is properly compiled in, which is required for Slurm's influxdb plugin to work correctly. Standard curl builds may not include LDAP support by default.

## Integration with Slurm

Slurm requires curl with LDAP support for the following components:

- InfluxDB plugin for metrics collection
- REST API daemon (slurmrestd)
- Various HTTP-based plugins

## Additional Resources

- [curl Documentation](https://curl.se/docs/)
- [Slurm Documentation](https://slurm.schedmd.com)
