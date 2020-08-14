#!/usr/bin/env python3

import argparse
from datetime import datetime
from pathlib import Path
import shlex
import shutil
import subprocess

import dropbox

HOME_DIR = Path('/Users/jeremander')
SILVER_SOLNS_DIR = '/Silver Solutions'
DBX_SLIDES_DIR = f'{SILVER_SOLNS_DIR}/Slide Samples'
DBX_IMG_DIR = f'{SILVER_SOLNS_DIR}/Images'
SITE_DIR = HOME_DIR / 'Programming/silversolutions/site'
PPT_DIR = SITE_DIR / 'ppt'
IMG_DIR = SITE_DIR / 'templates/static/images'
SLIDE_IMG_DIR = IMG_DIR / 'slides'

def get_dropbox_token():
    with open('/Users/jeremander/.dropbox/access_token') as f:
        return f.read().rstrip()

def normalize_path(path):
    p = Path(path)
    return p.name.split('.')[0].strip().lower().replace(' ', '_') + p.suffix

def download_file(dbx_path, dest_path):
    if (not dest_path.parent.exists()):
        dest_path.parent.mkdir(parents = True)
    metadata, res = dbx.files_download(path = dbx_path)
    if dest_path.exists():
        dbx_mtime = metadata.client_modified
        local_mtime = datetime.utcfromtimestamp(dest_path.stat().st_mtime)
        if (dbx_mtime < local_mtime):  # no need to re-download
            print(f'{dest_path} (no updates)')
            return False
    print(f'{dbx_path} -> {dest_path}')
    if res.ok:
        with open(dest_path, 'wb') as f:
            f.write(res.content)
    else:
        raise IOError(f'download error')
    return True

def run(cmd):
    cmd = [str(tok) for tok in cmd]
    print(' '.join(map(shlex.quote, cmd)))
    subprocess.run(cmd, stderr = subprocess.DEVNULL)

def ppt_to_jpg(path):
    p = Path(path)
    run(['soffice', '--headless', '--convert-to', 'pdf', path, '--outdir', p.parent])
    pdf_path = p.with_suffix('.pdf')
    img_dir = SLIDE_IMG_DIR / p.stem
    if (not img_dir.exists()):
        img_dir.mkdir(parents = True)
    subprocess.run(['convert', pdf_path, f'{img_dir}/Slide%d.jpg'])
    pdf_path.unlink()

def img_to_jpg(path):
    p = Path(path)
    img_dir = SLIDE_IMG_DIR / p.parent.stem
    if (not img_dir.exists()):
        img_dir.mkdir(parents = True)
    if (p.suffix == '.jpg'):  # just move to dest
        shutil.copy(p, img_dir / p.name)
    else:  # convert to jpg
        run(['convert', p, (img_dir / p.name).with_suffix('.jpg')])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--slides', action = 'store_true', help = 'download slides')
    args = parser.parse_args()

    token = get_dropbox_token()
    dbx = dropbox.Dropbox(token)

    # download slides
    if args.slides:
        pres_names = [entry.name for entry in dbx.files_list_folder(DBX_SLIDES_DIR).entries]
        for pres_name in pres_names:
            dbx_path = f'{DBX_SLIDES_DIR}/{pres_name}'
            ppt_path = PPT_DIR / normalize_path(dbx_path)
            if ('.' in pres_name):  # a PowerPoint
                if download_file(dbx_path, ppt_path):
                    ppt_to_jpg(ppt_path)
            else:  # a folder of PNG or JPG
                slide_names = [entry.name for entry in dbx.files_list_folder(dbx_path).entries]
                for slide_name in slide_names:
                    dbx_slide_path = f'{dbx_path}/{slide_name}'
                    dest_path = ppt_path / slide_name
                    if download_file(dbx_slide_path, dest_path):
                        img_to_jpg(dest_path)

    # download images
    subdirs = ['banners', 'icons']
    for subdir in subdirs:
        dbx_subdir = f'{DBX_IMG_DIR}/{subdir}'
        img_names = [entry.name for entry in dbx.files_list_folder(dbx_subdir).entries]
        for img_name in img_names:
            dbx_path = f'{dbx_subdir}/{img_name}'
            dest_path = IMG_DIR / subdir / img_name
            download_file(dbx_path, dest_path)