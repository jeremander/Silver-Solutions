#!/usr/bin/env python3

import argparse
import subprocess

from staticjinja import Site

PAGES = {
    'Home' : 'index.html',
    'Our Services' : {
        'Slide Presentations' : 'presentations.html',
        'Graphic Design' : 'graphics.html',
        'Résumés' : 'resumes.html',
    },
    'About Us' : 'about.html',
    'Contact' : 'contact.html'
}

SLIDE_CATEGORIES = {
    'Sales and Marketing Pitches' : ['WF', 'sat_prep'],
    'Training and Webinars' : ['the_business_of_medicine', 'holistic_dentistry'],
    'User Conferences' : ['alayacare_conference', 'patient_experience'],
    'Product Design' : ['nike'],
    'Roasts, Toasts, and Celebrations' : ['new_year_invitation_2020', '50th_anniversary']
}

CONTEXT = {
    'SITENAME' : 'Silver Solutions',
    'YEAR' : 2020,
    'SITEURL' : '.',
    'STATIC' : 'static',
    'IMAGE' : 'static/images',
    'SLIDES' : 'static/images/slides',
    'SLIDE_CATEGORIES' : SLIDE_CATEGORIES,
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