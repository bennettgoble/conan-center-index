import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, get, replace_in_file


class XMLRPCEPIRecipe(ConanFile):
    name = "xmlrpc-epi"
    description = "An implementation of the xmlrpc protocol in C"
    license = "MIT"
    homepage = "https://xmlrpc-epi.sourceforge.net/"
    topics = ("xml-rpc", "http")
    package_type = "library"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    exports_sources = "*.patch", "CMakeLists.txt"

    def requirements(self):
        self.requires("expat/2.5.0")
        if self.settings.os == "Windows":
            self.requires("libiconv/1.17")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def source(self):
        get(self, **self.conan_data["sources"][self.version])

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        apply_conandata_patches(self)
        if self.settings.build_type == "Debug":
            # Hack: remove inlines from source files so that we can link the debug build
            replace_in_file(self, os.path.join(self.source_folder, "src/xml_to_soap.c"), "inline", "")
            replace_in_file(self, os.path.join(self.source_folder, "src/xmlrpc_introspection.c"), "inline", "")
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="COPYING", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        copy(self, pattern="AUTHORS", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["xmlrpc-epi"]
