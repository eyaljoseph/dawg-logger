from pathlib import Path

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import copy


class DawgLogConan(ConanFile):
    name = "dawg-logger"
    version = "1.1.0"
    author = "eyaljoseph"
    url = "https://github.com/eyaljoseph/dawg-logger"
    description = "A lightweight and flexible C++ logging library"
    topics = ("logging", "logger", "file sink")

    settings = "os", "compiler", "build_type", "arch"

    # Files to export with the recipe and to send to the build
    exports_sources = (
        "CMakeLists.txt",
        "src/*",
        "include/*",
        "README.md",
        "conanfile.py",
    )

    generators = "CMakeToolchain", "CMakeDeps"

    def layout(self):
        cmake_layout(self)

    def build_requirements(self):
        self.tool_requires("cmake/3.16.9")

    def requirements(self):
        self.requires("fmt/*")
        self.requires("nlohmann_json/3.12.0")

    def build(self):
        cmake = CMake(self)
        cmake.configure()

        cmake.build(target="dawg-logger")

        # install target will place artifacts into the package folder
        cmake.install()

    def package(self):
        # Copy license if present
        copy(self, "LICENSE*", src=self.source_folder, dst=self.package_folder, keep_path=False)

    def package_info(self):
        # Consumers should link to `dawg-logger` library
        self.cpp_info.libs = ["dawg-logger"]
        # Provide a CMake package name for downstream consumers
        self.cpp_info.set_property("cmake_file_name", "dawg-logger")
        self.cpp_info.set_property("cmake_target_name", "DawgLog::dawg-logger")
