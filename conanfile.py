from conans import ConanFile
from conans.tools import download, unzip, check_sha256
from conans import CMake, ConfigureEnvironment

class DuktapeConan(ConanFile):
    name = "google-benchmark"
    version = "1.0.0"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    url="http://github.com/TyRoXx/conan-google-benchmark"
    license="Apache License 2.0"
    source_root = "benchmark-1.0.0"

    def source(self):
        zip_name = "v1.0.0.zip"
        download("https://github.com/google/benchmark/archive/%s" % zip_name, zip_name)
        check_sha256(zip_name, "5560358bf31e0478fa052de10c353cff809b8d2352bdfe695887e410ec593044")
        unzip(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        self.run("mkdir _build")
        configure_command = 'cd _build && cmake ../%s %s' % (self.source_root, cmake.command_line)
        self.run(configure_command)
        self.run("cd _build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy(pattern="*.h", dst="include", src="%s/include" % self.source_root, keep_path=True)
        self.copy(pattern="*.lib", dst="lib", src="_build", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="_build", keep_path=False)

    def package_info(self):  
        self.cpp_info.libs = ["benchmark"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(["Shlwapi"]) 
