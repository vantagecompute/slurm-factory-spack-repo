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

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage


class S2nTls(CMakePackage):
    """
    s2n-tls is a C99 implementation of the TLS/SSL protocols.

    s2n-tls is Amazon Web Services' implementation of the TLS/SSL protocols,
    designed to be simple, small, fast, and with security as a priority.
    It is released and licensed under the Apache License 2.0.

    This library is used by Slurm for internal TLS communication via the
    tls/s2n plugin. Ref: https://slurm.schedmd.com/tls.html
    """

    homepage = "https://github.com/aws/s2n-tls"
    url = "https://github.com/aws/s2n-tls/archive/refs/tags/v1.5.14.tar.gz"
    git = "https://github.com/aws/s2n-tls.git"

    license("Apache-2.0")

    # Latest stable releases
    version("1.5.14", sha256="3f65f1eca85a8ac279de204455a3e4940bc6ad4a1df53387d86136bcecde0c08")
    version("1.5.13", sha256="ea4b0ea3585be97bb31ced70ba6190f29ddefec32d102e47b2906d402ec4b8df")
    version("1.5.12", sha256="718866ea8276f4d5c78a4b6506561599a4ff5c05b3fccee7ef7ad6198b23e660")

    # Use main branch for development
    version("main", branch="main")

    # Build variants
    variant("shared", default=True, description="Build shared libraries")

    # Dependencies
    depends_on("cmake@3.0:", type="build")
    depends_on("openssl")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("CMAKE_BUILD_TYPE", "Release"),
        ]
        return args
