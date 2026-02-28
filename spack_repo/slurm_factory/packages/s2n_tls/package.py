# Copyright (c) 2025 Vantage Compute Corporation. and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import spack.llnl.util.tty as tty
import spack.util.executable as exe
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class S2nTls(CMakePackage):
    """
    s2n-tls is a C99 implementation of the TLS/SSL protocols.

    s2n-tls is a C99 implementation of the TLS/SSL protocols that is designed
    to be simple, small, fast, and with security as a priority. It is released
    and licensed under the Apache License 2.0. s2n-tls is used by Slurm >= 25.11
    for the tls/s2n plugin to provide secure communications between Slurm daemons.
    """

    homepage = "https://github.com/aws/s2n-tls"
    url = "https://github.com/aws/s2n-tls/archive/refs/tags/v1.5.14.tar.gz"
    git = "https://github.com/aws/s2n-tls.git"

    license("Apache-2.0")

    version("1.5.14", sha256="3f65f1eca85a8ac279de204455a3e4940bc6ad4a1df53387d86136bcecde0c08")

    variant("shared", default=True, description="Build shared libraries")

    depends_on("c", type="build")
    depends_on("cmake@3.0:", type="build")
    depends_on("openssl", type=("build", "link", "run"))
    # patchelf is needed to fix rpaths for relocatable deployments
    depends_on("patchelf", type="build")

    @property
    def libs(self):
        return find_libraries(
            ["libs2n"],
            root=self.prefix,
            recursive=True,
            shared=self.spec.variants["shared"].value,
            runtime=False,
        )

    @property
    def _openssl_lib_dir(self):
        """Detect the correct OpenSSL lib directory (lib64 vs lib)."""
        openssl_prefix = self.spec["openssl"].prefix
        lib64_dir = join_path(openssl_prefix, "lib64")
        if os.path.exists(join_path(lib64_dir, "libcrypto.so")):
            return lib64_dir
        return join_path(openssl_prefix, "lib")

    def cmake_args(self):
        spec = self.spec
        openssl_prefix = spec["openssl"].prefix
        openssl_lib_dir = self._openssl_lib_dir
        openssl_include_dir = join_path(openssl_prefix, "include")
        openssl_ssl_lib = join_path(openssl_lib_dir, "libssl.so")
        openssl_crypto_lib = join_path(openssl_lib_dir, "libcrypto.so")

        tty.msg(f"s2n-tls will use spack OpenSSL from {openssl_prefix}")
        tty.msg(f"  OpenSSL lib dir: {openssl_lib_dir}")
        tty.msg(f"  libcrypto: {openssl_crypto_lib} (exists={os.path.exists(openssl_crypto_lib)})")
        tty.msg(f"  libssl:    {openssl_ssl_lib} (exists={os.path.exists(openssl_ssl_lib)})")
        tty.msg(f"  headers:   {openssl_include_dir} (exists={os.path.exists(openssl_include_dir)})")

        args = [
            "-DCMAKE_BUILD_TYPE=Release",
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            # Disable tests — we only need libs2n.so for the Slurm tls/s2n plugin.
            # Building tests requires `ar` which may not be on PATH in the spack
            # build environment, causing "no such file or directory" at link time.
            "-DBUILD_TESTING=OFF",
            # Point CMake to spack OpenSSL for find_package / FindCrypto.cmake
            f"-DCMAKE_PREFIX_PATH={openssl_prefix}",
            f"-DOPENSSL_ROOT_DIR={openssl_prefix}",
            # Explicit library/include paths as fallback
            f"-DOPENSSL_INCLUDE_DIR={openssl_include_dir}",
            f"-DOPENSSL_SSL_LIBRARY={openssl_ssl_lib}",
            f"-DOPENSSL_CRYPTO_LIBRARY={openssl_crypto_lib}",
            # Don't search system paths — avoids picking up /usr/lib/libcrypto
            "-DCMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH=OFF",
            # Bake RPATH into libs2n.so so it finds spack libcrypto at runtime
            f"-DCMAKE_INSTALL_RPATH={openssl_lib_dir}",
            "-DCMAKE_BUILD_WITH_INSTALL_RPATH=ON",
        ]

        return args

    @run_after("install")
    def fixup_rpaths(self):
        """
        Fix RPATHs on libs2n.so for relocatable deployments.

        libs2n.so links to libcrypto.so and must find the spack-built OpenSSL
        at runtime, not the system one. We add $ORIGIN-relative paths so that
        when deployed via a spack view/tarball (where absolute spack install
        paths no longer exist), the library resolution still works.
        """
        openssl_lib_dir = self._openssl_lib_dir

        # Find the actual libs2n.so file (not a symlink) for patching
        lib_dir = self.prefix.lib
        if not os.path.isdir(str(lib_dir)):
            lib_dir = self.prefix.lib64
        if not os.path.isdir(str(lib_dir)):
            tty.warn("Could not find lib directory for rpath patching")
            return

        libs2n_real = None
        for f in sorted(os.listdir(str(lib_dir))):
            fpath = join_path(lib_dir, f)
            if f.startswith("libs2n.so") and not os.path.islink(fpath):
                libs2n_real = fpath
                break

        if not libs2n_real:
            tty.warn("libs2n.so real file not found for rpath patching")
            return

        patchelf = exe.which("patchelf")
        if not patchelf:
            tty.warn("patchelf not found — libs2n.so rpath may need manual fixing")
            return

        try:
            current_rpath = patchelf("--print-rpath", libs2n_real, output=str).strip()
            tty.msg(f"  libs2n.so current rpath: {current_rpath}")

            # Build new rpath — keep existing entries, drop temporary build paths
            new_rpath_parts = []
            for part in current_rpath.split(":"):
                if "s2n-tls-install" in part or "s2n-tls-build" in part:
                    continue  # drop temporary build paths
                if part:
                    new_rpath_parts.append(part)

            # Ensure spack OpenSSL lib dir is in RPATH (absolute, for spack env use)
            if openssl_lib_dir not in new_rpath_parts:
                new_rpath_parts.append(openssl_lib_dir)

            # CRITICAL: Add $ORIGIN-relative paths so libs2n.so can find
            # libcrypto.so when deployed via a spack view/tarball where the
            # absolute spack install paths no longer exist.
            # libs2n.so lives in <view>/lib/ and libcrypto.so lives in:
            #   <view>/lib64/  (OpenSSL 3.x on x86_64)
            #   <view>/lib/    (fallback / same dir)
            #   <view>/lib/private/  (spack view conflict resolution)
            for origin_path in ["$ORIGIN", "$ORIGIN/../lib64", "$ORIGIN/../lib/private"]:
                if origin_path not in new_rpath_parts:
                    new_rpath_parts.insert(0, origin_path)

            new_rpath = ":".join(new_rpath_parts)
            patchelf("--set-rpath", new_rpath, libs2n_real)
            tty.msg(f"  libs2n.so new rpath: {new_rpath}")
            tty.msg("✓ Fixed libs2n.so rpath for relocatable deployment")
        except Exception as e:
            tty.warn(f"Could not patch libs2n.so rpath: {e}")

    @run_after("install")
    def verify_linkage(self):
        """Verify libs2n.so is linked against the spack-built OpenSSL."""
        openssl_prefix = self.spec["openssl"].prefix

        # Find libs2n.so
        lib_dir = self.prefix.lib
        if not os.path.isdir(str(lib_dir)):
            lib_dir = self.prefix.lib64

        s2n_lib = join_path(lib_dir, "libs2n.so")
        if not os.path.exists(s2n_lib):
            # try versioned
            for f in os.listdir(str(lib_dir)):
                if f.startswith("libs2n.so"):
                    s2n_lib = join_path(lib_dir, f)
                    break

        ldd = exe.which("ldd")
        if ldd and os.path.exists(s2n_lib):
            try:
                ldd_output = ldd(s2n_lib, output=str, error=str)
                tty.msg("  libs2n.so linkage:")
                for line in ldd_output.splitlines():
                    if "crypto" in line or "ssl" in line:
                        tty.msg(f"    {line.strip()}")
                        if "/usr/lib" in line and str(openssl_prefix) not in line:
                            tty.warn(f"  WARNING: libs2n.so linked to system OpenSSL: {line.strip()}")
                            tty.warn(f"  Expected spack OpenSSL at: {openssl_prefix}")
            except Exception as e:
                tty.debug(f"Could not verify libs2n.so linkage: {e}")

        # Verify s2n.h header was installed
        s2n_header = join_path(self.prefix.include, "s2n.h")
        if os.path.exists(s2n_header):
            tty.msg("✓ s2n.h header installed")
        else:
            tty.warn(f"s2n.h header not found at {s2n_header}")

        tty.msg("✓ s2n-tls installed successfully")
