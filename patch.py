#!/usr/bin/env python3

import os

PATCH= '<script defer data-domain="nondocumentation.garambrogne.net" src="https://plausible.garambrogne.net/js/script.js"></script>\n'


def patch(before, after):
    for line in before.readlines():
        after.write(line)
        if line.strip().startswith("<head"):
            after.write(PATCH)

if __name__ == "__main__":
    patch(open('output/index.html', 'r'), open('output/index_patched.html','w'))
