# curl

Command-line tool and library for transferring data with URLs.

## Overview

This package provides a custom build of curl for Slurm Factory. It defaults to OpenSSL for TLS and HTTP/2 through nghttp2; the Slurm package requests LDAP and SSH2 support on top of that.

## Package Information

- **Homepage**: [https://curl.se/](https://curl.se/)
- **Source**: Built from official curl releases
- **License**: curl license (MIT/X derivative)
- **Package Definition**: [`packages/curl/package.py`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/spack_repo/slurm_factory/packages/curl/package.py)

## Available Versions

| Version | Status |
|---------|--------|
| `8.15.0` | Latest; used by Slurm Factory |
| `8.14.1` | |

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
- `libs`: Build shared libs, static libs or both (default: `shared,static`)

The package builds with autotools by default; `build_system=cmake` is also supported.

## Usage

### Basic Installation

```bash
spack install slurm_factory.curl
```

### With LDAP Support (Required for Slurm)

The Slurm package depends on `curl libs=shared,static +nghttp2 +libssh2 +ldap`:

```bash
spack install slurm_factory.curl +ldap +libssh2 +nghttp2
```

Slurm Factory pins a fuller spec:

```bash
spack install slurm_factory.curl@8.15.0 libs=shared,static \
  +nghttp2 +libssh2 +ldap +gssapi +libidn2 tls=openssl
```

## Dependencies

curl has minimal dependencies, primarily:

- **OpenSSL**: TLS/SSL support (when `tls=openssl`, the default)
- **zlib**: Compression support
- **Perl** (build only, `@8.15.0`)

Additional dependencies based on variants:

- **nghttp2**: HTTP/2 support (when `+nghttp2`, the default)
- **libssh2**: SSH protocol support (when `+libssh2`)
- **libssh**: SSH protocol support (when `+libssh`)
- **openldap**: LDAP protocol support (when `+ldap`)
- **krb5**: Kerberos support (when `+gssapi`)
- **libidn2**: IDN support (when `+libidn2`)
- **GnuTLS** or **mbedTLS**: When selected with `tls=`

## Why This Package Exists

The Slurm Factory curl package ensures LDAP support is properly compiled in, which is required for Slurm's InfluxDB plugin to work correctly. Standard curl builds may not include LDAP support by default.

## Integration with Slurm

Slurm's configure only sets its `WITH_CURL` conditional when it finds a curl built with LDAP. Without it, `libslurm_curl` is not built and the InfluxDB profiling plugin (`acct_gather_profile/influxdb`) fails with undefined symbols. The Slurm package builds `libslurm_curl.so` against this curl and relinks the InfluxDB plugin against it.

## Additional Resources

- [curl Documentation](https://curl.se/docs/)
- [Slurm Documentation](https://slurm.schedmd.com)
- [Slurm Package](./slurm.md): Main Slurm package documentation
