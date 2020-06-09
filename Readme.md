Allow/Deny access to specified directory using icacls.exe

usage: pyaccess.py [-h]  (-d DIR | -l) (-a | -y) [-r | -f]

optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  Directory path

  -l, --list         list remembered paths

  -a, --allow        Allow access

  -y, --deny         Deny access

  -r, --remember     remember path

  -f, --forget       forget path
