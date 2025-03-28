#!/usr/bin/python3

import json
from os import system
from os.path import relpath, dirname
from contextlib_chdir import chdir

def extract_header(include, source_path):
    include = include.split("\"")[1]

    if "/" in include:
        include = f"include/{include}"
    else:
        include = dirname(relpath(source_path, "..")) + "/" + include

    return include

def register_header(libs_names, libs_makefiles, output, file):
    with chdir("qemu-8.1.2/build"):
        lib_name = "unknown"
        for n in libs_names:
            if f"lib{n}" in output:
                lib_name = n
                break

        try:
            with open(file, "r") as source_file:
                include_lines = [l.strip() for l in source_file.readlines() if "#include \"" in l]

                for i in include_lines:
                    header = extract_header(i, file)
                    libs_makefiles[lib_name].write(f"LIBQEMU_{lib_name.upper()}_HDRS-y += $(LIBQEMU)/{header}\n")
        except FileNotFoundError:
            print(f"The file '{file}' was not found.")


def register_source(libs_names, libs_makefiles, output, file):
    if ".." in file:
        file = file.strip("../")
    else:
        file = f"build/{file}"

    lib_name = "unknown"
    for n in libs_names:
        if f"lib{n}" in output:
            lib_name = n
            break

    libs_makefiles[lib_name].write(f"LIBQEMU_{lib_name.upper()}_SRCS-y += $(LIBQEMU)/{file}\n")


def register_sublib(libs_makefiles):
    for n, f in libs_makefiles.items():
        f.write(f"\n$(eval $(call _libqemu_import_lib,{n},$(LIBQEMU_{n.upper()}_HDRS-y),$(LIBQEMU_{n.upper()}_SRCS-y)))\n")


if __name__ == "__main__":
    libs_names = [l.strip() for l in open("libs", "r").readlines()]
    libs_makefiles = {n : open(f"Makefile.uk.qemu.{n}", "w+") for n in libs_names}

    with open("compile_commands.json") as data:
        cc = json.load(data)
    
    for c in cc:
        register_header(libs_names, libs_makefiles, c["output"], c["file"])

    for f in libs_makefiles.values():
        f.write("\n")

    for c in cc:
        register_source(libs_names, libs_makefiles, c["output"], c["file"])

    register_sublib(libs_makefiles)
