#!/usr/bin/env python3

HEADER= '''<script defer data-domain="nondocumentation.garambrogne.net" src="https://plausible.garambrogne.net/js/script.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">
'''

CSS='''
html, body {
  font-family: "Open Sans", serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
  font-variation-settings:
    "wdth" 100;
}

code {
  font-family: "Fira Code", serif;
  font-optical-sizing: auto;
  font-weight: 500;
  font-style: normal;
}
'''

def patch(before, after):
    for line in before.readlines():
        if line.strip()=='</style>':
            after.write(CSS)
        after.write(line)
        if line.strip().startswith("<head"):
            after.write(HEADER)

if __name__ == "__main__":
    patch(open('output/index.html', 'r'), open('output/index_patched.html','w'))
