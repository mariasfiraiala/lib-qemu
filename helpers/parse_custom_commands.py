#!/usr/bin/python3

# with open("build.ninja", "r") as source_file:
#     lines = source_file.readlines()
#     cc_lines = [lines[i + 1] for i, l in enumerate(lines) if "CUSTOM_COMMAND" in l]
with open("custom_commands", "r") as source_file:
    cc_lines = source_file.readlines()
    new_cc = []
    for cc in cc_lines:
        cc = cc.replace("""/home/maria/catalog-core/c-hello/workdir/build/libqemu/origin/qemu-8.1.2""", "$(LIBQEMU)")

        words = cc.split(" ")
        new_words = []
        for w in words:
            if "." in w and "LIBQEMU" not in w:
                if w[:2] == "..":
                    w = "$(LIBQEMU)" + w[2:]
                else:
                    w = "$(LIBQEMU)/build/" + w
            new_words.append(w)
            
        cc = " ".join(new_words)
        new_cc.append(cc)

    cc_lines = new_cc


with open("Makefile.uk.qemu.cc.meson", "w+") as meson:
    meson_cc = [m for m in cc_lines if "pyvenv/bin/meson" in m]

    for cc in meson_cc:
        cc = cc.replace(" COMMAND ", "LIBQEMU_MESON_CC-y +").strip()
        cc = cc + " && \\\n\n"

        meson.write(cc)

    meson.write("$(eval $(call _libqemu_custom_commands,MESON,$(LIBQEMU_MESON_CC-y)))\n")

with open("Makefile.uk.qemu.cc.python", "w+") as python:
    python_cc = [p for p in cc_lines if "pyvenv/bin/python3" in p and "pyvenv/bin/meson" not in p]

    for cc in python_cc:
        cc = cc.replace(" COMMAND ", "LIBQEMU_PYTHON_CC-y +").strip()
        cc = cc + " && \\\n\n"

        python.write(cc)

    python.write("$(eval $(call _libqemu_custom_commands,PYTHON,$(LIBQEMU_PYTHON_CC-y)))\n")
