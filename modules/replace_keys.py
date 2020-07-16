# Simple Minecraft Server Manager
# By Doomlad
# 07/14/2020

import os
import tempfile


def replace_key(filename, key, value):
    with open(filename, 'rU') as f_in, tempfile.NamedTemporaryFile(
            'w', dir=os.path.dirname(filename), delete=False) as f_out:
        for line in f_in.readlines():
            if line.startswith(key):
                line = '='.join((line.split('=')[0], '{}'.format(str(value) + "\n")))
            f_out.write(line)

    # remove old version
    os.unlink(filename)

    # rename new version
    os.rename(f_out.name, filename)
