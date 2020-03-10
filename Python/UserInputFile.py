#!/usr/bin/env python3.8


def get_file_name(repromte=False):
    if repromte:
        print("Please entre a file name")

    file_name = input("Destination file name:").strip()

    return file_name or get_file_name(True)


file_name = get_file_name()

print(
    f"Please enter your content. Entering an empty line will write the content to {file_name}:\n")

with open(file_name, "w") as f:
    eof = False
    lines = []

    while not eof:
        line = input()
        if line.strip():
            lines.append(f"{line}\n")
        else:
            eof = True

    f.writelines(lines)
    print(f"lines written to {file_name}")
