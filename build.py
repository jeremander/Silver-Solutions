#!/usr/bin/env python3

import argparse
import subprocess

from staticjinja import Site

PAGES = {
    'Home' : 'index.html',
    'Our Services' : {
        'Slide Presentations' : 'presentations.html',
        'Résumés & Interview Coaching' : 'resumes.html',
        'Facilitated Meetings' : 'meetings.html'
    },
    'About Us' : 'about.html',
    'Contact' : 'contact.html'
}

CONTEXT = {
    'SITENAME' : 'Silver Solutions',
    'YEAR' : 2020,
    'SITEURL' : '.',
    'STATIC' : 'static',
    'IMAGE' : 'static/images',
    'PAGES' : PAGES
}

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--watch', action = 'store_true', help = 'watch for file updates')
    parser.add_argument('-o', '--output-dir', default = 'docs', help = 'output directory')
    args = parser.parse_args()

    sass_args = ['sass', 'sass:templates/static/css']
    sass_args.append('--watch' if args.watch else '--update')
    print(' '.join(sass_args))

    site = Site.make_site(searchpath = 'templates', outpath = args.output_dir, env_globals = CONTEXT, staticpaths = [f'static/'])

    if args.watch:
        with subprocess.Popen(sass_args) as proc:
            # print('Rendering site from templates...')
            site.render(use_reloader = True)
            proc.terminate()
    else:
        try:
            subprocess.run(sass_args + ['--update'])
        except FileNotFoundError:
            print('WARNING: failed to run sass')
        print('Rendering site from templates...')
        site.render(use_reloader = False)