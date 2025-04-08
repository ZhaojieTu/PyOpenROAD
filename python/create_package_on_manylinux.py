import os
import shutil


def create_openroad_core_package(destination):
    core_lib_path = "python/pyopenroad.so"
    package_full_path = os.path.join(destination,"openroad_core")
    os.makedirs(package_full_path,exist_ok=True)

    setup_file_path = os.path.join(destination, "setup.py")
    with open(setup_file_path, "w") as f:
        f.write("""
from setuptools import setup, find_packages
import os
import stat
from setuptools.command.install import install

class MakeExecutable(install):
    def run(self):
        install.run(self)
        exe = os.path.join(self.install_lib, "openroad_core", "bin", "openroad")
        if os.path.exists(exe):
            st = os.stat(exe)
            os.chmod(exe, st.st_mode | stat.S_IEXEC)

setup(
    name='openroad-full',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'openroad_core': ['lib/*.so*', 'bin/openroad',"tcl/*"],  
    },
    entry_points={
        "console_scripts": [
            "openroad=openroad_core.__main__:main"  
        ]
    },
    install_requires=[],
    zip_safe=False,
    cmdclass={
        'install': MakeExecutable
    }
)
                """)

    manifest_file_path = os.path.join(destination, "MANIFEST.in")
    with open(manifest_file_path, "w") as f:
        f.write(f"""
recursive-include openroad_core *.so
include openroad_core/bin/openroad
include openroad_core/lib/*
recursive-include openroad_core/tcl *
""")

#     inner_package_full_path = os.path.join(package_full_path, "openroad_core")
    inner_package_full_path = package_full_path
    os.makedirs(inner_package_full_path,exist_ok=True)

    init_file_path = os.path.join(inner_package_full_path, "__init__.py")
    with open(init_file_path, "w") as f:
        f.write("")    

    main_file_path = os.path.join(inner_package_full_path, "__main__.py")
    with open(main_file_path, "w") as f:
        f.write("""
import os
import subprocess
import pathlib
import sys

def main():
    here = pathlib.Path(__file__).parent.resolve()
    tcl_dir = here / "tcl" / "tcl8.6"
    tclreadline_dir = here / "tcl" / "tclreadline2.1.0"
    lib_dir = here / "lib"
    bin_path = here / "bin" / "openroad"

    os.environ["TCL_LIBRARY"] = str(tcl_dir)
    os.environ["TCLLIBPATH"] = str(tclreadline_dir)
    os.environ["LD_LIBRARY_PATH"] = f"{lib_dir}:{os.environ.get('LD_LIBRARY_PATH', '')}"

    os.execv(str(bin_path), [str(bin_path)] + sys.argv[1:])
""")

    inner_core_lib_path = os.path.join(inner_package_full_path, "pyopenroad.so") 
    inner_bin_path = os.path.join(inner_package_full_path, "bin")   
    os.makedirs(inner_bin_path,exist_ok=True)
    shutil.copy(core_lib_path, inner_core_lib_path)

    openroad_exe_path = "OpenROAD/src/openroad"
    shutil.copy(openroad_exe_path, inner_bin_path)

    inner_lib_path = os.path.join(inner_package_full_path, "lib")
    os.makedirs(inner_lib_path,exist_ok=True)

    tcl_path = "/usr/local/lib/tcl8.6"
    tcl_lib_path = "/usr/local/lib/libtcl8.6.so"
    
    tclreadline_path = "/usr/lib64/tcl8.5/tclreadline2.1.0"
    tclreadline_lib_path = "/usr/lib64/tcl8.5/tclreadline2.1.0/libtclreadline.so"

    inner_tcl_path = os.path.join(inner_package_full_path, "tcl")
    os.makedirs(inner_tcl_path,exist_ok=True)
    inner_tcl_path_tcl8_6 = os.path.join(inner_tcl_path, "tcl8.6")
    inner_tcl_path_tclreadline2_1_0 = os.path.join(inner_tcl_path, "tclreadline2.1.0")
    shutil.copytree(tcl_path, inner_tcl_path_tcl8_6)
    shutil.copytree(tclreadline_path, inner_tcl_path_tclreadline2_1_0)

    shutil.copy(tcl_lib_path, inner_lib_path)
    shutil.copy(tclreadline_lib_path, inner_lib_path)



def create_openroad_package(package_name,python_wrapper,destination):
    package_full_path = os.path.join(destination,package_name)
    os.makedirs(package_full_path,exist_ok=True)

#     # Create setup.py file
#     setup_file_path = os.path.join(package_full_path, "setup.py")
#     with open(setup_file_path, "w") as f:
#         f.write(f"""
# from setuptools import setup, find_packages

# setup(
#     name='{package_name}',
#     version='0.1.0',
#     packages=find_packages(),
#     install_requires=[
#         'openroad_core>=0.1.0',
#     ],
#     zip_safe=False,
#     author='Zhaojie Tu'
#     )
#                 """)

#     inner_package_full_path = os.path.join(package_full_path,package_name)
    inner_package_full_path = package_full_path
    os.makedirs(inner_package_full_path,exist_ok=True)

    # Create __init__.py file
    init_file_path = os.path.join(inner_package_full_path, "__init__.py")
    python_wrapper_name = os.path.splitext(os.path.basename(python_wrapper))[0]
    with open(init_file_path, "w") as f:
        f.write(f"""
from .{python_wrapper_name} import *
""")

    # Copy python_wrapper file to inner_package_full_path directory
    inner_python_wrapper_full_path = os.path.join(inner_package_full_path,f"{python_wrapper_name}.py")
    shutil.copy(python_wrapper, inner_python_wrapper_full_path)



    with open(inner_python_wrapper_full_path, "r") as file:
        content = file.read()

    content = content.replace(
        f"""
if __package__ or "." in __name__:
    from . import _{package_name}_py
else:
    import _{package_name}_py
""",
        f"""
from openroad_core import pyopenroad
_{package_name}_py = pyopenroad._{package_name}_py
"""
    )

    with open(inner_python_wrapper_full_path, "w") as file:
        file.write(content)

def create_openroad_special_package(destination):
    package_name = "openroad"
    python_wrapper = "OpenROAD/src/openroad_swig_py.py"
    package_full_path = os.path.join(destination,package_name)
    os.makedirs(package_full_path,exist_ok=True)

#     # Create setup.py file
#     setup_file_path = os.path.join(package_full_path, "setup.py")
#     with open(setup_file_path, "w") as f:
#         f.write(f"""
# from setuptools import setup, find_packages

# setup(
#     name='{package_name}',
#     version='0.1.0',
#     packages=find_packages(),
#     install_requires=[
#         'openroad_core>=0.1.0',
#     ],
#     zip_safe=False,
#     author='Zhaojie Tu'
#     )
#                 """)

#     inner_package_full_path = os.path.join(package_full_path,package_name)
    inner_package_full_path = package_full_path
    os.makedirs(inner_package_full_path,exist_ok=True)

    # Create __init__.py file
    init_file_path = os.path.join(inner_package_full_path, "__init__.py")
    python_wrapper_name = os.path.splitext(os.path.basename(python_wrapper))[0]
    with open(init_file_path, "w") as f:
        f.write(f"""
from .{python_wrapper_name} import *
""")

    # Copy python_wrapper file to inner_package_full_path directory
    inner_python_wrapper_full_path = os.path.join(inner_package_full_path,f"{python_wrapper_name}.py")
    shutil.copy(python_wrapper, inner_python_wrapper_full_path)



    with open(inner_python_wrapper_full_path, "r") as file:
        content = file.read()

    content = content.replace(
        f"""
if __package__ or "." in __name__:
    from . import _openroad_swig_py
else:
    import _openroad_swig_py
""",
        f"""
from openroad_core import pyopenroad
_openroad_swig_py = pyopenroad._openroad_swig_py
"""
    )

    with open(inner_python_wrapper_full_path, "w") as file:
        file.write(content)

if __name__ == "__main__":

    src_path = "OpenROAD/src/"
    destination_core = "python"
    destination_tools = os.path.join(destination_core,"openroad-full")
    os.makedirs(destination_tools,exist_ok=True)

    create_openroad_core_package(destination_tools)   


    create_openroad_special_package(destination_tools)

    first_level_dirs = [d for d in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, d))]
    
    for subdir in first_level_dirs:
        subdir_path = os.path.join(src_path, subdir)
        for root, dirs, files in os.walk(subdir_path):
            for file in files:
                if file.endswith("_py.py"):
                    python_wrapper = os.path.join(root, file)
                    print(f"copy module: {subdir}, file: {python_wrapper}")
                    create_openroad_package(subdir, python_wrapper, destination_tools)
