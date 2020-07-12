#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import shlex
import shutil
import subprocess

import dropbox

HOME_DIR = Path('/Users/jeremander')
SLIDES_DIR = '/Silver Solutions/Slide Samples'
SITE_DIR = HOME_DIR / 'Programming/silversolutions/site'
PPT_DIR = SITE_DIR / 'ppt'
SLIDE_IMG_DIR = SITE_DIR / 'templates/static/images/slides'

def get_dropbox_token():
    with open('/Users/jeremander/.dropbox/access_token') as f:
        return f.read().rstrip()

def normalize_path(path):
    p = Path(path)
    return p.name.split('.')[0].strip().lower().replace(' ', '_') + p.suffix

def run(cmd):
    cmd = [str(tok) for tok in cmd]
    print(' '.join(map(shlex.quote, cmd)))
    subprocess.run(cmd, stderr = subprocess.DEVNULL)

def ppt_to_png(path):
    p = Path(path)
    run(['soffice', '--headless', '--convert-to', 'pdf', path, '--outdir', p.parent])
    pdf_path = p.with_suffix('.pdf')
    img_dir = SLIDE_IMG_DIR / p.stem
    if (not img_dir.exists()):
        img_dir.mkdir(parents = True)
    subprocess.run(['convert', pdf_path, f'{img_dir}/Slide%d.jpg'])
    pdf_path.unlink()


if __name__ == '__main__':

    token = get_dropbox_token()
    dbx = dropbox.Dropbox(token)
    slide_files = [entry.name for entry in dbx.files_list_folder(SLIDES_DIR).entries]
    for slide_file in slide_files:
        dbx_path = f'{SLIDES_DIR}/{slide_file}'
        ppt_path = PPT_DIR / normalize_path(dbx_path)
        if ('.' in slide_file):
            continue
            metadata, res = dbx.files_download(path = dbx_path)
            if ppt_path.exists():
                dbx_mtime = metadata.client_modified
                local_mtime = datetime.fromtimestamp(ppt_path.stat().st_mtime)
                if (dbx_mtime < local_mtime):  # no need to re-download
                    print(f'{ppt_path} (no updates)')
                    continue
            print(f'{dbx_path} -> {ppt_path}')
            if res.ok:
                with open(ppt_path, 'wb') as f:
                    f.write(res.content)
            else:
                raise IOError(f'download error')
            ppt_to_png(ppt_path)
        else:  # a folder of PNG or JPG
            print(f'{slide_file} -> {ppt_path}')
            if (not ppt_path.exists()):
                ppt_path.mkdir()
            slide_names = [entry.name for entry in dbx.files_list_folder(dbx_path).entries]
            for slide_name in slide_names:
                _, res = dbx.files_download(path = f'{dbx_path}/{slide_name}')
                slide_path = ppt_path / slide_name
                if res.ok:
                    with open(slide_path, 'wb') as f:
                        f.write(res.content)
                else:
                    raise IOError('download error')
                if slide_name.endswith('.png'):  # convert to JPG
                    run(['convert', slide_path, slide_path.with_suffix('.jpg')])
                    slide_path.unlink()
            dest_dir = SLIDE_IMG_DIR / slide_file
            shutil.copytree(ppt_path, dest_dir)