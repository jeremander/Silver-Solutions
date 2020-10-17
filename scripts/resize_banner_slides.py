#!/usr/bin/env python3

from pathlib import Path
import subprocess

if __name__ == '__main__':

    p1 = Path('/Users/jeremander/Dropbox/Silver Solutions/Images/banners')
    p2 = Path('/Users/jeremander/Programming/silversolutions/site/templates/static/images/banners')

    for src in p1.glob('*.jpg'):
        dest = p2 / src.name
        cmd = ['convert', '-strip', '-interlace', 'Plane', '-gaussian-blur', '0.05', '-resize', '33%', '-quality', '80%', str(src.resolve()), str(dest.resolve())]
        print(' '.join(cmd))
        subprocess.run(cmd)
