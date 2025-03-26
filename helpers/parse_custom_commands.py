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


with open("custom_commands.sh", "w+") as custom_commands:
    for cc in cc_lines:
        cc = cc.replace(" COMMAND = ", "").strip()
        cc = cc + " && \\\n"

        custom_commands.write(cc)
