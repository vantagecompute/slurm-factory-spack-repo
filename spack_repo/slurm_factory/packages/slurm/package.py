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
import re
import os

import spack.util.executable as exe
import spack.llnl.util.tty as tty
from spack.package import *

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage


class Slurm(AutotoolsPackage):
    """Slurm is an open source, fault-tolerant, and highly scalable cluster
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
    url = "https://github.com/SchedMD/slurm/archive/slurm-21-08-8-2.tar.gz"

    license("GPL-2.0-or-later")

    version("25-05-3-1", sha256="a24d9a530e8ae1071dd3865c7260945ceffd6c65eea273d0ee21c85d8926782e")
    version("25-05-1-1", sha256="b568c761a6c9d72358addb3bb585456e73e80a02214ce375d2de8534f9ddb585")
    version("24-11-6-1", sha256="282708483326f381eb001a14852a1a82e65e18f37b62b7a5f4936c0ed443b600")
    version(
        "23-11-11-1", sha256="e9234e664ce30be206f73c0ff1a5f33e0ce32be35ece812eac930fcaa9da2c2f"
    )
    version("23-11-1-1", sha256="31506df24c6d24e0ea0329cac1395ab9b645bbde1518f5c469f7711df5e22c11")
    version("23-11-0-1", sha256="3780773a80b73ea2edb4353318b4220188f4eda92c31ab3a2bdd3a4fdec76be9")
    version("23-02-7-1", sha256="3f60ad5b5a492312d1febb9f9167caa3aee7f8438bb032590a993f5a65c5e4db")
    version("23-02-6-1", sha256="ed44d4e591c0f91874d535cb8c9ea67dd2a38bfa4e96fa6c71687293f6a1d3bb")
    version("23-02-5-1", sha256="4fee743a34514d8fe487080048256f5ee032374ed5f42d0eae342110dcd59edf")
    version("23-02-4-1", sha256="7290143a71ce2797d0df3423f08396fd5c0ae4504749ff372d6860b2d6a3a1b0")
    version("23-02-3-1", sha256="c41747e4484011cf376d6d4bc73b6c4696cdc0f7db4f64174f111bb9f53fb603")
    version("23-02-2-1", sha256="71edcf187a7d68176cca06143adf98e8f332d42cdf000cb534b03b13834ad537")
    version("23-02-1-1", sha256="d827553496ee9158bbf6a862b563cfd48566e6d815ad2f8349950fe6f04934da")
    version("22-05-9-1", sha256="c9aaa2362b5bf7a4745c8bf90e8dd2ca50802f1241dd1f5220aec8448c09b514")
    version("22-05-8-1", sha256="8c8f6a26a5d51e6c63773f2e02653eb724540ee8b360125c8d7732314ce737d6")
    version("22-05-7-1", sha256="2ad7e8a415d54d45977ab64b4e73c891154d2f41a04505fedf6f8d3df385acb1")
    version("21-08-8-2", sha256="876d7dfa716990d7e579cfb9c6ffc123258e03a1450e993ade596d2ee90afcdd")
    version("21-08-8-1", sha256="47d4dd2f391abcb856ecfddb51145c86ead89554f24efb586c59f0e38491ff36")
    version("20-11-9-1", sha256="98d36f3487e95af610db305a3ee1c1a7d370a3e1efef9fabee8b0edb98a6604b")
    # Due to CVE 2022-29500, CVE 2022-29501, and CVE 2022-29502, prior to 21.08.8 and
    # 20.11.9 are deprecated
    version(
        "21-08-1-1",
        sha256="23321719101762b055a6b1da6ff4261f5e6c469bce038c6c23549840453862e7",
        deprecated=True,
    )
    version(
        "21-08-0-1",
        sha256="c8caf9b5f715c02b6f9e55e9737ee7b99f93c5efc8dcc34c2ce40bed0aea5402",
        deprecated=True,
    )
    version(
        "20-11-8-1",
        sha256="1cafed56ae9d90387a5dc6092090c174e144a6e5a31330f748d1fd3a616ae92f",
        deprecated=True,
    )
    version(
        "20-11-7-1",
        sha256="7d92babd97d0b8750b8c25eced4507323aff32a9d85af3a644c1acedbddb9d2f",
        deprecated=True,
    )
    version(
        "20-02-7-1",
        sha256="060acf966af53e75c7eaae83c4f42abdcc60702838c2dcd35cb01468b45a68a1",
        deprecated=True,
    )
    # Due to CVE-2021-31215, all versions prior to 20.11.7 or 20.02.7 are deprecated.
    version(
        "20-11-5-1",
        sha256="d0634c6c6cc79bde38d19f0ef0de0de3b07907830f5e45be6f4a9ca4259f8f67",
        deprecated=True,
    )
    version(
        "20-11-4-1",
        sha256="06c5333e85f531730bf1c6eb48a8d48a551d9090540ce37b78181024273fb6bd",
        deprecated=True,
    )
    version(
        "20-11-0-1",
        sha256="404f72c287c5aad887a5b141304e4962548c12f79b04fc9c88550bc024604228",
        deprecated=True,
    )
    version(
        "20-02-4-1",
        sha256="d32a39df20a99430973de6692870269f38443d8b963c32b4d6475c9d5e92cd73",
        deprecated=True,
    )
    version(
        "19-05-6-1",
        sha256="1b83bce4260af06d644253b1f2ec2979b80b4418c631e9c9f48c2729ae2c95ba",
        deprecated=True,
    )
    version(
        "19-05-5-1",
        sha256="e53e67bd0bb4c37a9c481998764a746467a96bc41d6527569080514f36452c07",
        deprecated=True,
    )
    version(
        "18-08-9-1",
        sha256="32eb0b612ca18ade1e35c3c9d3b4d71aba2b857446841606a9e54d0a417c3b03",
        deprecated=True,
    )
    version(
        "18-08-0-1",
        sha256="62129d0f2949bc8a68ef86fe6f12e0715cbbf42f05b8da6ef7c3e7e7240b50d9",
        deprecated=True,
    )
    version(
        "17-11-9-2",
        sha256="6e34328ed68262e776f524f59cca79ac75bcd18030951d45ea545a7ba4c45906",
        deprecated=True,
    )
    version(
        "17-02-6-1",
        sha256="97b3a3639106bd6d44988ed018e2657f3d640a3d5c105413d05b4721bc8ee25e",
        deprecated=True,
    )

    variant("gtk", default=False, description="Enable GTK+ support")
    variant("mariadb", default=False, description="Use MariaDB instead of MySQL")

    variant("hwloc", default=False, description="Enable hwloc support")
    variant("hdf5", default=False, description="Enable hdf5 support")
    variant("readline", default=True, description="Enable readline support")
    variant("pmix", default=False, description="Enable PMIx support")
    variant(
        "sysconfdir",
        default="PREFIX/etc",
        values=any,
        description="Set system configuration path (possibly /etc/slurm)",
    )
    variant("restd", default=False, description="Enable the slurmrestd server")
    variant("nvml", default=False, description="Enable NVML autodetection")
    variant("cgroup", default=False, description="Enable cgroup plugin")
    variant("pam", default=False, description="Enable PAM support")
    variant("rsmi", default=False, description="Enable ROCm SMI support")
    variant("influxdb", default=True, description="Enable InfluxDB profiling plugin")
    variant("kafka", default=False, description="Enable Kafka profiling plugin")
    variant("lua", default=False, description="Enable Lua scripting support")
    variant("mcs", default=False, description="Enable MCS support for K8S integration")
    variant("certs", default=False, description="Enable certificate generation support for slurm>=24.11.")
  
    # TODO: add variant for BG/Q and Cray support

    # TODO: add variant for TLS (slurm@25-05:)

    # TODO: add variant for RRD (librrd) (slurm@23-02:)

    # TODO: add support for checkpoint/restart (BLCR)

    # TODO: add support for lua

    depends_on("c", type="build")  # generated

    depends_on("librdkafka", when="+kafka")

    depends_on("mysql@8.0.35 +client_only", type=("build", "link", "run"))
    # curl with LDAP support is REQUIRED for Slurm's WITH_CURL conditional to be set
    # Without LDAP, libslurm_curl won't be built and influxdb plugin will fail with undefined symbols
    depends_on("curl libs=shared,static +nghttp2 +libssh2 +ldap", type=("build", "link", "run"))
    depends_on("libssh2", type=("build", "link", "run"))
    depends_on("glib", type=("build", "link", "run"))
    depends_on("json-c", type=("build", "link", "run"))
    depends_on("lz4", type=("build", "link", "run"))
    depends_on("munge", type=("build", "link", "run"))
    depends_on("ncurses", type=("build", "link", "run"))
    depends_on("lua", when="+lua", type=("build", "link", "run"))
    depends_on("openssl", type=("build", "link", "run"))
    depends_on("pkgconfig", type="build")
    depends_on("readline", when="+readline", type=("build", "link", "run"))
    depends_on("zlib-api", type=("build", "link", "run"))

    depends_on("gtkplus", when="+gtk", type=("build", "link", "run"))
    depends_on("hdf5", when="+hdf5", type=("build", "link", "run"))
    depends_on("hwloc", when="+hwloc", type=("build", "link", "run"))
    depends_on("mariadb", when="+mariadb", type=("build", "link", "run"))

    # JWT library is needed for auth plugins, not just REST daemon
    depends_on("libjwt", type=("build", "link", "run"))
    
    depends_on("pmix@:5", when="@22-05:+pmix", type=("build", "link", "run"))
    depends_on("pmix@:3", when="@20-11:21-08+pmix", type=("build", "link", "run"))
    depends_on("pmix@:2", when="@19-05:20-02+pmix", type=("build", "link", "run"))
    depends_on("pmix@:1", when="@:18+pmix", type=("build", "link", "run"))

    depends_on("http-parser", when="+restd")
    depends_on("http-parser", when="+influxdb")  # InfluxDB plugin needs http-parser for REST API
    depends_on("libyaml", when="+restd")
    # Note: libjwt dependency moved to unconditional above since auth plugins need it

    depends_on("cuda", when="+nvml")
    depends_on("dbus", when="+cgroup")
    depends_on("linux-pam", when="+pam")
    depends_on("rocm-smi-lib", when="+rsmi")

    # Apply custom patches
    # NOTE: We don't patch Makefile.am because it requires autoreconf, which causes
    # AM_CONDITIONAL errors. Instead, we manually build libslurm_curl.so in install phase.
    # patch("build-libslurm-curl-shared.patch", when="+influxdb")

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
        """Setup build environment including creating missing libcurl.pc file"""
        spec = self.spec
        curl_prefix = spec["curl"].prefix
        
        tty.msg(f"Setting up build environment for Slurm with curl at {curl_prefix}")
        
        # Create libcurl.pc file in a writable temporary location
        # since the curl installation directory is read-only
        build_dir = self.stage.path if hasattr(self, 'stage') else "/tmp"
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
                 f"curl headers not found at {curl_header}. Please ensure curl was built with headers included."
            )

        # The key fix: ensure curl-config is in PATH and force WITH_CURL conditional
        curl_config_path = os.path.join(curl_prefix, "bin", "curl-config")
        if not os.path.exists(curl_config_path):
            raise RuntimeError(
                f"curl-config not found at {curl_config_path}. Please ensure curl was built with config script."
            )

        # Pass --with-libcurl to trigger LIBCURL_CHECK_CONFIG macro
        # The macro will find curl-config in PATH (set in setup_build_environment)
        # and properly set LIBCURL, LIBCURL_CPPFLAGS, and WITH_CURL conditional
        args.append("--with-libcurl={0}".format(curl_prefix))

        # Add curl paths to general CPPFLAGS and LDFLAGS for fallback
        cppflags.append("-I{0}/include".format(curl_prefix))
        ldflags.extend(["-L{0}/lib".format(curl_prefix), "-Wl,-rpath,{0}/lib".format(curl_prefix)])
        
        # Note: influxdb plugin will automatically work once WITH_CURL is properly set
        # The plugin depends on libslurm_curl.la which provides slurm_curl_* functions

        if "+lua" in spec:
            # Slurm's configure uses pkg-config for Lua detection
            # Pass --with-lua (not a path) and let pkg-config find it via CPPFLAGS/LDFLAGS
            lua_prefix = spec["lua"].prefix
            args.append("--with-lua")
            cppflags.append("-I{0}/include".format(lua_prefix))
            ldflags.extend(["-L{0}/lib".format(lua_prefix), "-Wl,-rpath,{0}/lib".format(lua_prefix)])
        else:
            args.append("--without-lua")

        if "+kafka" in spec:
            kafka_prefix = spec["librdkafka"].prefix
            args.append("--with-rdkafka={0}".format(kafka_prefix))
            cppflags.append("-I{0}/include".format(kafka_prefix))
            ldflags.extend(["-L{0}/lib".format(kafka_prefix), "-Wl,-rpath,{0}/lib".format(kafka_prefix)])

        # MySQL configuration (required for accounting)
        if "mysql" in spec:
            mysql_prefix = spec["mysql"].prefix
            cppflags.append("-I{0}/include".format(mysql_prefix))
            ldflags.extend(["-L{0}/lib".format(mysql_prefix), "-Wl,-rpath,{0}/lib".format(mysql_prefix)])

        # Add RPATH for lib/slurm directory where libslurmfull.so resides
        # This ensures slurmstepd and other binaries can find Slurm internal libraries
        # Using $ORIGIN for relocatability - binaries in sbin/ will resolve to ../lib/slurm
        ldflags.append("-Wl,-rpath,$ORIGIN/../lib/slurm")
        
        # Add the combined flags if we have any
        if cppflags:
            args.append("CPPFLAGS={0}".format(" ".join(cppflags)))
        if ldflags:
            args.append("LDFLAGS={0}".format(" ".join(ldflags)))

        if "~gtk" in spec:
            args.append("--disable-gtktest")

        if "~readline" in spec:
            args.append("--without-readline")

        if "+hdf5" in spec:
            args.append("--with-hdf5={0}".format(spec["hdf5"].prefix.bin.h5cc))
        else:
            args.append("--without-hdf5")

        if "+pmix" in spec:
            args.append("--with-pmix={0}".format(spec["pmix"].prefix))
        else:
            args.append("--without-pmix")

        # Always include JWT since auth plugins need it
        args.append("--with-jwt={0}".format(spec["libjwt"].prefix))

        # Explicitly enable InfluxDB support with curl when variant is enabled
        if "+influxdb" in spec:
            args.append("--with-libcurl={0}".format(spec["curl"].prefix))
        else:
            args.append("--without-libcurl")

        if "+restd" in spec:
            args.append("--enable-slurmrestd")
            args.append("--with-http-parser={0}".format(spec["http-parser"].prefix))
        else:
            args.append("--disable-slurmrestd")
   
        if "+hwloc" in spec:
            args.append("--with-hwloc={0}".format(spec["hwloc"].prefix))
        else:
            args.append("--without-hwloc")

        if spec.satisfies("+nvml"):
            args.append(f"--with-nvml={spec['cuda'].prefix}")

        if spec.satisfies("+pam"):
            args.append(f"--with-pam_dir={spec['linux-pam'].prefix}")

        if spec.satisfies("+rsmi"):
            args.append(f"--with-rsmi={spec['rocm-smi-lib'].prefix}")

        sysconfdir = spec.variants["sysconfdir"].value
        if sysconfdir != "PREFIX/etc":
            args.append("--sysconfdir={0}".format(sysconfdir))

        return args
    
    def configure(self, spec, prefix):
        """Override configure to add diagnostics for WITH_CURL detection"""
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
            tty.error(f"✗ src/curl/Makefile does not exist!")
    
    @run_after('install')
    def install_curl_library(self):
        """Build and install libslurm_curl shared library after main installation
        
        The influxdb and other plugins need slurm_curl_* symbols at runtime.
        By default, libslurm_curl is built as a convenience library (noinst_LTLIBRARIES)
        and not installed. We manually build it as a shared library and install it.
        
        This approach avoids patching Makefile.am which would require autoreconf and
        cause AM_CONDITIONAL errors.
        """
        import glob
        import shutil
        import subprocess
        
        if not self.spec.satisfies("+influxdb"):
            return
        
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
            obj_file
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


    def install(self, spec, prefix):
        make("install")
        make("-C", "contribs/pmi2", "install")

        # Note: Following SchedMD approach - InfluxDB plugin should be built automatically
        # as part of main build process when curl is available, not manually built
        # See https://github.com/SchedMD/slurm/blob/master/debian/control - libcurl4-openssl-dev
        # is build dependency and plugins are integrated into main package

        if spec.satisfies("+influxdb"):
            make("-C", "src/plugins/acct_gather_profile/influxdb", "install")

        if self.spec.satisfies("@:24-11-6-1"):
            if spec.satisfies("+certs"):
                make("-C", "src/plugins/certmgr", "install")

        if self.spec.satisfies("@:25-05-1-1"):
            if spec.satisfies("+mcs"):
                make("-C", "src/plugins/mcs", "install")

            if spec.satisfies("+certs"):
                make("-C", "src/plugins/certmgr", "install")
                make("-C", "src/plugins/certgen", "install")

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

        # Verify InfluxDB plugin was built if requested
        if "+influxdb" in spec:
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
        """Set up runtime environment for Slurm"""
        spec = self.spec
        
        # Add Slurm lib directories to library path
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", os.path.join(self.prefix.lib, "slurm"))
        
        # Add runtime dependency library paths
        for dep_name in ["curl", "libssh2", "openssl", "libjwt", "munge", "json-c", "lz4", "glib"]:
            if dep_name in spec:
                dep_spec = spec[dep_name]
                if hasattr(dep_spec.prefix, 'lib'):
                    env.prepend_path("LD_LIBRARY_PATH", dep_spec.prefix.lib)
                if hasattr(dep_spec.prefix, 'lib64'):
                    env.prepend_path("LD_LIBRARY_PATH", dep_spec.prefix.lib64)
        
        # Add Slurm binaries to PATH
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("PATH", self.prefix.sbin)
        
        # Set SLURM_ROOT for tools that need it
        env.set("SLURM_ROOT", self.prefix)
