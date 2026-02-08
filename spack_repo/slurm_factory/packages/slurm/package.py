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
import re

import spack.llnl.util.tty as tty
import spack.util.executable as exe
from spack.package import *
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage


class Slurm(AutotoolsPackage):
    """
    Slurm is an open source, fault-tolerant, and highly scalable cluster management system.

    Slurm is an open source, fault-tolerant, and highly scalable cluster
    management and job scheduling system for large and small Linux clusters.

    Slurm requires no kernel modifications for its operation and is relatively
    self-contained. As a cluster workload manager, Slurm has three key
    functions. First, it allocates exclusive and/or non-exclusive access to
    resources (compute nodes) to users for some duration of time so they can
    perform work. Second, it provides a framework for starting, executing,
    and monitoring work (normally a parallel job) on the set of allocated
    nodes. Finally, it arbitrates contention for resources by managing a
    queue of pending work.
    """

    homepage = "https://slurm.schedmd.com"
    url = "https://github.com/SchedMD/slurm/releases"

    license("GPL-2.0-or-later")

    version("25-11-2-1", sha256="719783317e46b6241ab5c8f1e3f91e1e34fda63b5a1cd21403fa7696ec8d517c")
    version("24-11-6-1", sha256="282708483326f381eb001a14852a1a82e65e18f37b62b7a5f4936c0ed443b600")
    version("23-11-11-1", sha256="e9234e664ce30be206f73c0ff1a5f33e0ce32be35ece812eac930fcaa9da2c2f")

    variant(
        "sysconfdir",
        default="PREFIX/etc",
        values=any,
        description="Set system configuration path (possibly /etc/slurm)",
    )
    variant("gtk", default=False, description="Enable GTK+ support")
    variant("nvml", default=False, description="Enable NVML autodetection")
    variant("rsmi", default=False, description="Enable ROCm SMI support")

    # TODO: add support for checkpoint/restart (BLCR)

    # s2n-tls for internal TLS support (tls/s2n plugin) - required for slurm >= 25.11
    # Ref: https://slurm.schedmd.com/tls.html
    depends_on("s2n-tls", when="@25-11-2-1:", type=("build", "link", "run"))

    # Dependencies
    depends_on("c", type="build")

    # Build-only dependencies (not linked, not needed at runtime)
    depends_on("pkgconfig", type="build")

    # Link-only dependencies (headers + static libs, compiled in, not needed as runtime packages)
    # librdkafka is needed for the Kafka job scheduler - usually linked statically
    depends_on("librdkafka", type="link")
    # http-parser needed for slurmrestd and influxdb plugin - static library
    depends_on("http-parser", type="link")
    depends_on("libyaml", type="link")

    # Build+Link dependencies (linked but not needed as separate runtime packages)
    # Cgroup plugin needs dbus
    depends_on("dbus", type=("build", "link"))
    # Linux PAM is needed for PAM support
    depends_on("linux-pam", type=("build", "link"))
    # IPMI support via FreeIPMI
    depends_on("freeipmi", type=("build", "link"))
    depends_on("json-c", type=("build", "link"))
    depends_on("lz4", type=("build", "link"))
    depends_on("ncurses", type=("build", "link"))
    depends_on("lua", type=("build", "link"))
    depends_on("readline", type=("build", "link"))
    depends_on("hwloc", type=("build", "link"))

    # Full runtime dependencies (needed at runtime as separate packages)
    # curl with LDAP support is REQUIRED for Slurm's WITH_CURL conditional to be set
    # Without LDAP, libslurm_curl won't be built and influxdb plugin will fail with undefined symbols
    depends_on("curl libs=shared,static +nghttp2 +libssh2 +ldap", type=("build", "link", "run"))
    # MySQL client library is REQUIRED for Slurm accounting support
    depends_on("mysql@8.0.35 +client_only", type=("build", "link", "run"))
    depends_on("openssl", type=("build", "link", "run"))
    depends_on("glib", type=("build", "link", "run"))
    depends_on("munge", type=("build", "link", "run"))
    depends_on("libssh2", type=("build", "link", "run"))
    # JWT library is needed for auth plugins, not just REST daemon
    depends_on("libjwt", type=("build", "link", "run"))
    depends_on("pmix@:5", type=("build", "link", "run"))
    depends_on("zlib-api", type=("build", "link", "run"))
    depends_on("hdf5", type=("build", "link", "run"))

    # Conditional dependencies
    depends_on("gtkplus", when="+gtk", type=("build", "link"))
    depends_on("cuda", when="+nvml")
    depends_on("rocm-smi-lib", when="+rsmi")

    # Apply custom patches
    # NOTE: We don't patch Makefile.am because it requires autoreconf, which causes
    # AM_CONDITIONAL errors. Instead, we manually build libslurm_curl.so in install phase.

    executables = ["^srun$", "^salloc$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str).rstrip()
        match = re.search(r"slurm(?:-wlm)?\s*([0-9.]+)", output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        wrapper_flags = None

        if name == "cflags":
            if self.spec.satisfies("@:20-02-1 %gcc@10:"):
                wrapper_flags = ["-fcommon"]

        return (wrapper_flags, None, flags)

    def setup_build_environment(self, env):
        """Set up build environment including creating missing libcurl.pc file."""
        spec = self.spec
        curl_prefix = spec["curl"].prefix

        tty.msg(f"Setting up build environment for Slurm with curl at {curl_prefix}")

        # Create libcurl.pc file in a writable temporary location
        # since the curl installation directory is read-only
        build_dir = self.stage.path if hasattr(self, "stage") else "/tmp"
        temp_pkgconfig_dir = os.path.join(build_dir, "temp_pkgconfig")
        libcurl_pc = os.path.join(temp_pkgconfig_dir, "libcurl.pc")

        tty.msg(f"Creating temporary libcurl.pc at {libcurl_pc}")

        try:
            os.makedirs(temp_pkgconfig_dir, exist_ok=True)
            tty.msg(f"Created temporary pkgconfig directory at {temp_pkgconfig_dir}")

            # Create libcurl.pc content similar to Ubuntu's version
            pc_content = f"""prefix={curl_prefix}
exec_prefix=${{prefix}}
libdir=${{prefix}}/lib
includedir=${{prefix}}/include

Name: libcurl
URL: https://curl.se/
Description: Library to transfer files with ftp, http, etc.
Version: 8.15.0
Libs: -L${{libdir}} -lcurl
Cflags: -I${{includedir}}
"""

            with open(libcurl_pc, "w") as f:
                f.write(pc_content)

            tty.msg(f"SUCCESS: Created libcurl.pc at {libcurl_pc}")

            # Verify the file was created and is readable
            if os.path.exists(libcurl_pc):
                with open(libcurl_pc, "r") as f:
                    content = f.read()
                    tty.msg(f"Verified libcurl.pc content ({len(content)} chars)")
            else:
                tty.error(f"FAILED to create libcurl.pc at {libcurl_pc}")

        except Exception as e:
            tty.error(f"ERROR creating libcurl.pc: {e}")

        # Ensure PKG_CONFIG_PATH includes our temporary curl location FIRST
        env.prepend_path("PKG_CONFIG_PATH", temp_pkgconfig_dir)
        tty.msg(f"Added {temp_pkgconfig_dir} to PKG_CONFIG_PATH")

        # Also add the curl prefix to PATH to ensure curl-config is found
        # This is CRITICAL - the LIBCURL_CHECK_CONFIG macro in configure.ac needs
        # to find curl-config in PATH to properly set WITH_CURL conditional
        env.prepend_path("PATH", os.path.join(curl_prefix, "bin"))
        tty.msg(f"Added {curl_prefix}/bin to PATH for curl-config detection")

        # Verify curl-config is accessible and working
        curl_config = os.path.join(curl_prefix, "bin", "curl-config")
        if os.path.exists(curl_config):
            import subprocess

            try:
                version = subprocess.check_output([curl_config, "--version"], text=True).strip()
                protocols = subprocess.check_output([curl_config, "--protocols"], text=True).strip()
                tty.msg(f"curl-config check: {version}")
                tty.msg(f"curl protocols: {protocols[:100]}...")
                if "LDAP" in protocols:
                    tty.msg("✓ LDAP protocol confirmed in curl")
                else:
                    tty.warn("✗ LDAP protocol NOT found in curl!")
            except Exception as e:
                tty.error(f"Failed to run curl-config: {e}")

        # Add HDF5 include paths for HDF5 profiling plugin
        if "hdf5" in spec:
            hdf5_prefix = spec["hdf5"].prefix
            tty.msg(f"Adding HDF5 include path: {hdf5_prefix}/include")
            env.prepend_path("CPATH", os.path.join(hdf5_prefix, "include"))
            env.prepend_path("C_INCLUDE_PATH", os.path.join(hdf5_prefix, "include"))
            env.prepend_path("CPLUS_INCLUDE_PATH", os.path.join(hdf5_prefix, "include"))

        # DO NOT set LIBCURL or LIBCURL_CPPFLAGS environment variables!
        # The configure script's LIBCURL_CHECK_CONFIG macro needs to run curl-config
        # itself to properly detect features and set the WITH_CURL conditional.
        # Setting these variables prevents proper detection and breaks influxdb plugin.

    def configure_args(self):
        spec = self.spec
        args = [
            "--enable-multiple-slurmd",
            "--enable-pam",
            "--disable-developer",
            "--disable-debug",
            "--with-json={0}".format(spec["json-c"].prefix),
            "--with-lz4={0}".format(spec["lz4"].prefix),
            "--with-munge={0}".format(spec["munge"].prefix),
        ]

        # Build comprehensive CPPFLAGS and LDFLAGS
        cppflags = []
        ldflags = []

        # Curl configuration (always included)
        curl_prefix = spec["curl"].prefix

        # Verify curl headers are available
        curl_header = os.path.join(curl_prefix, "include", "curl", "curl.h")
        if not os.path.exists(curl_header):
            raise RuntimeError(
                f"curl headers not found at {curl_header}. "
                "Please ensure curl was built with headers included."
            )

        # The key fix: ensure curl-config is in PATH and force WITH_CURL conditional
        curl_config_path = os.path.join(curl_prefix, "bin", "curl-config")
        if not os.path.exists(curl_config_path):
            raise RuntimeError(
                f"curl-config not found at {curl_config_path}. "
                "Please ensure curl was built with config script."
            )

        # Pass --with-libcurl to trigger LIBCURL_CHECK_CONFIG macro
        # The macro will find curl-config in PATH (set in setup_build_environment)
        # and properly set LIBCURL, LIBCURL_CPPFLAGS, and WITH_CURL conditional
        args.append("--with-libcurl={0}".format(curl_prefix))

        # Add curl paths to general CPPFLAGS and LDFLAGS for fallback
        cppflags.append("-I{0}/include".format(curl_prefix))
        ldflags.extend(["-L{0}/lib".format(curl_prefix), "-Wl,-rpath,{0}/lib".format(curl_prefix)])

        # slurmrestd support
        args.append("--enable-slurmrestd")
        args.append("--with-http-parser={0}".format(spec["http-parser"].prefix))

        # HDF5 support
        args.append("--with-hdf5={0}".format(spec["hdf5"].prefix.bin.h5cc))

        # PMIx support
        args.append("--with-pmix={0}".format(spec["pmix"].prefix))

        # Always include JWT since auth plugins need it
        args.append("--with-jwt={0}".format(spec["libjwt"].prefix))

        # Hwloc support
        args.append("--with-hwloc={0}".format(spec["hwloc"].prefix))

        # FreeIPMI support
        args.append(f"--with-freeipmi={spec['freeipmi'].prefix}")

        # Slurm's configure uses pkg-config for Lua detection
        lua_prefix = spec["lua"].prefix
        args.append("--with-lua")
        cppflags.append("-I{0}/include".format(lua_prefix))
        ldflags.extend(["-L{0}/lib".format(lua_prefix), "-Wl,-rpath,{0}/lib".format(lua_prefix)])

        # PAM support
        args.append(f"--with-pam_dir={spec['linux-pam'].prefix}")

        # Kafka configuration
        kafka_prefix = spec["librdkafka"].prefix
        args.append("--with-rdkafka={0}".format(kafka_prefix))
        cppflags.append("-I{0}/include".format(kafka_prefix))
        ldflags.extend(["-L{0}/lib".format(kafka_prefix), "-Wl,-rpath,{0}/lib".format(kafka_prefix)])

        # MySQL configuration (required for accounting)
        mysql_prefix = spec["mysql"].prefix
        cppflags.append("-I{0}/include".format(mysql_prefix))
        ldflags.extend(["-L{0}/lib".format(mysql_prefix), "-Wl,-rpath,{0}/lib".format(mysql_prefix)])

        if "~gtk" in spec:
            args.append("--disable-gtktest")

        if spec.satisfies("+nvml"):
            args.append(f"--with-nvml={spec['cuda'].prefix}")

        if spec.satisfies("+rsmi"):
            args.append(f"--with-rsmi={spec['rocm-smi-lib'].prefix}")

        # s2n-tls for internal TLS support (tls/s2n plugin) - enabled for slurm >= 25.11
        # Ref: https://slurm.schedmd.com/tls.html
        if spec.satisfies("@25-11-2-1:"):
            s2n_prefix = spec["s2n-tls"].prefix
            args.append("--with-s2n={0}".format(s2n_prefix))
            cppflags.append("-I{0}/include".format(s2n_prefix))
            ldflags.extend(
                ["-L{0}/lib".format(s2n_prefix), "-Wl,-rpath,{0}/lib".format(s2n_prefix)]
            )

        sysconfdir = spec.variants["sysconfdir"].value
        if sysconfdir != "PREFIX/etc":
            args.append("--sysconfdir={0}".format(sysconfdir))

        # Add RPATH for lib/slurm directory where libslurmfull.so resides
        # This ensures slurmstepd and other binaries can find Slurm internal libraries
        # Using $ORIGIN for relocatability - binaries in sbin/ will resolve to ../lib/slurm
        ldflags.append("-Wl,-rpath,$ORIGIN/../lib/slurm")

        # Add the combined flags if we have any
        if cppflags:
            args.append("CPPFLAGS={0}".format(" ".join(cppflags)))
        if ldflags:
            args.append("LDFLAGS={0}".format(" ".join(ldflags)))

        return args

    def configure(self, spec, prefix):
        """Override configure to add diagnostics for WITH_CURL detection."""
        # Run the standard autotools configure
        super().configure(spec, prefix)

        # After configure runs, check if WITH_CURL was set
        config_h = os.path.join(self.build_directory, "config.h")
        if os.path.exists(config_h):
            with open(config_h, "r") as f:
                config_content = f.read()
                if "HAVE_LIBCURL" in config_content:
                    tty.msg("✓ HAVE_LIBCURL is defined in config.h")
                else:
                    tty.error("✗ HAVE_LIBCURL is NOT defined in config.h!")

        # Check if Makefile has WITH_CURL conditional set
        makefile = os.path.join(self.build_directory, "src/curl/Makefile")
        if os.path.exists(makefile):
            with open(makefile, "r") as f:
                makefile_content = f.read()
                if "libslurm_curl.la" in makefile_content:
                    tty.msg("✓ libslurm_curl.la target found in src/curl/Makefile")
                else:
                    tty.error("✗ libslurm_curl.la target NOT found in src/curl/Makefile!")
        else:
            tty.error("✗ src/curl/Makefile does not exist!")

    @run_after("install")
    def install_curl_library(self):
        """
        Build and install libslurm_curl shared library after main installation.

        The influxdb and other plugins need slurm_curl_* symbols at runtime.
        By default, libslurm_curl is built as a convenience library (noinst_LTLIBRARIES)
        and not installed. We manually build it as a shared library and install it.

        This approach avoids patching Makefile.am which would require autoreconf and
        cause AM_CONDITIONAL errors.

        Note: We always build this since curl is always a dependency.
        """
        import subprocess

        tty.msg("Building and installing libslurm_curl shared library for influxdb plugin")

        # Build directory where slurm_curl.c is located
        build_dir = join_path(self.stage.source_path, "src", "curl")

        # Check if curl support was enabled during configure
        if not os.path.exists(join_path(build_dir, "slurm_curl.c")):
            tty.warn("slurm_curl.c not found - curl support may not be enabled")
            return

        # Get curl library flags
        curl_prefix = self.spec["curl"].prefix
        curl_libs = f"-L{curl_prefix}/lib -lcurl -Wl,-rpath,{curl_prefix}/lib"

        lib_dir = join_path(self.prefix, "lib")
        include_dir = join_path(self.stage.source_path, "src", "common")

        # Compile slurm_curl.c to object file with PIC
        obj_file = join_path(build_dir, "slurm_curl.o")
        compile_cmd = [
            self.compiler.cc,
            "-fPIC",
            "-shared",
            f"-I{self.stage.source_path}",
            f"-I{include_dir}",
            f"-I{curl_prefix}/include",
            "-c",
            join_path(build_dir, "slurm_curl.c"),
            "-o",
            obj_file,
        ]

        tty.msg(f"Compiling slurm_curl.c: {' '.join(compile_cmd)}")
        subprocess.run(compile_cmd, check=True, cwd=build_dir)

        # Link to shared library
        so_file = join_path(lib_dir, "libslurm_curl.so.0.0.0")
        link_cmd = [
            self.compiler.cc,
            "-shared",
            "-Wl,-soname,libslurm_curl.so.0",
            obj_file,
            "-o",
            so_file,
        ] + curl_libs.split()

        tty.msg(f"Linking libslurm_curl.so: {' '.join(link_cmd)}")
        subprocess.run(link_cmd, check=True, cwd=build_dir)

        # Create symlinks
        os.chdir(lib_dir)
        if os.path.exists("libslurm_curl.so.0"):
            os.remove("libslurm_curl.so.0")
        os.symlink("libslurm_curl.so.0.0.0", "libslurm_curl.so.0")

        if os.path.exists("libslurm_curl.so"):
            os.remove("libslurm_curl.so")
        os.symlink("libslurm_curl.so.0", "libslurm_curl.so")

        tty.msg("✓ libslurm_curl.so built and installed successfully")

        # Rebuild influxdb plugin now that libslurm_curl.so exists
        # The plugin needs to link against libslurm_curl.so for the slurm_curl_* symbols
        tty.msg("Rebuilding influxdb plugin with libslurm_curl.so available")
        plugin_dir = join_path(self.stage.source_path, "src", "plugins", "acct_gather_profile", "influxdb")
        if os.path.exists(plugin_dir):
            # Clean the plugin directory to force rebuild
            make("-C", plugin_dir, "clean")

            # Rebuild with LDFLAGS pointing to libslurm_curl.so
            ldflags = f"-L{lib_dir} -lslurm_curl -Wl,-rpath,{lib_dir}"
            make("-C", plugin_dir, f"LDFLAGS={ldflags}", "install")
            tty.msg("✓ influxdb plugin rebuilt and linked against libslurm_curl.so")

            # Verify the plugin was linked correctly
            plugin_so = join_path(self.prefix.lib, "slurm", "acct_gather_profile_influxdb.so")
            if os.path.exists(plugin_so):
                try:
                    ldd = exe.which("ldd")
                    if ldd:
                        output = ldd(plugin_so, output=str, error=str)
                        if "libslurm_curl" in output:
                            tty.msg("✓ Verified: influxdb plugin linked against libslurm_curl.so")
                        else:
                            tty.warn("WARNING: influxdb plugin may not be linked against libslurm_curl.so")
                except Exception as e:
                    tty.debug(f"Could not verify plugin linkage: {e}")
        else:
            tty.warn(f"influxdb plugin directory not found: {plugin_dir}")

    def install(self, spec, prefix):
        make("install")
        make("-C", "contribs/pmi2", "install")
        make("-C", "contribs/nss_slurm", "install")

        # Verify curl linkage by checking if slurmctld was built with curl support
        slurmctld_path = os.path.join(prefix.sbin, "slurmctld")
        if os.path.exists(slurmctld_path):
            # Check if the binary was linked against curl
            try:
                ldd = exe.which("ldd")
                if ldd:
                    output = ldd(slurmctld_path, output=str, error=str)
                    if "libcurl" in output:
                        tty.msg("SUCCESS: slurmctld was successfully linked against curl")
                    else:
                        tty.warn("WARNING: slurmctld may not be linked against curl")
            except Exception as e:
                tty.debug(f"Could not verify curl linkage: {e}")

        # Verify InfluxDB plugin was built (always expected since curl is always available)
        influxdb_plugin = os.path.join(prefix.lib, "slurm", "acct_gather_profile_influxdb.so")
        if not os.path.exists(influxdb_plugin):
            tty.warn(
                "InfluxDB plugin was not built. Check if curl development headers are available. "
                f"Expected plugin at: {influxdb_plugin}"
            )
        else:
            tty.msg(f"SUCCESS: InfluxDB plugin built at: {influxdb_plugin}")
            # Also verify the plugin was linked against curl
            try:
                ldd = exe.which("ldd")
                if ldd:
                    output = ldd(influxdb_plugin, output=str, error=str)
                    if "libcurl" in output:
                        tty.msg("SUCCESS: InfluxDB plugin linked against curl")
                    else:
                        tty.warn("WARNING: InfluxDB plugin may not be linked against curl")
            except Exception as e:
                tty.debug(f"Could not verify InfluxDB plugin curl linkage: {e}")

    def setup_run_environment(self, env):
        """Set up runtime environment for Slurm."""
        spec = self.spec

        # Add Slurm lib directories to library path
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", os.path.join(self.prefix.lib, "slurm"))

        # Add runtime dependency library paths
        for dep_name in ["curl", "libssh2", "openssl", "libjwt", "munge", "json-c", "lz4", "glib"]:
            if dep_name in spec:
                dep_spec = spec[dep_name]
                if hasattr(dep_spec.prefix, "lib"):
                    env.prepend_path("LD_LIBRARY_PATH", dep_spec.prefix.lib)
                if hasattr(dep_spec.prefix, "lib64"):
                    env.prepend_path("LD_LIBRARY_PATH", dep_spec.prefix.lib64)

        # Add Slurm binaries to PATH
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("PATH", self.prefix.sbin)

        # Set SLURM_ROOT for tools that need it
        env.set("SLURM_ROOT", self.prefix)
