#!/usr/bin/env python3

import os
import re

import click as click
import requests

globally_confirmed = False


def convert_all(path, silent=False,):
    if path is None or not os.path.exists(path):
        print('Invalid path:', path)
        return
    count = 0
    invalid_urls = []
    for filename in [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames]:
        if filename.endswith('.webloc'):
            # if validate:
            #     with open(filename) as f:
            #         url = extract_url(f.read())
            #         if url and not is_valid(url):
            #             print('Warning:', url, 'is not reachable')
            #             invalid_urls.append(filename)
            if not silent:
                global globally_confirmed
                if not globally_confirmed:
                    confirm = input('Want to convert ' + filename + '? (y/n/a): ')
                    if confirm.lower() == 'a':
                        globally_confirmed = True
                    elif confirm.lower() != 'y':
                        continue
                # check if a html file already exists
                base, _ = os.path.splitext(filename)
                if os.path.exists(base + '.html'):
                    confirm = input('DANGER: File ' + base + '.html already exists. Overwrite? (y/n): ')
                    if confirm.lower() != 'y':
                        continue
            convert(filename)
            count += 1

    print('Converted', count, 'files')
    # if len(invalid_urls) > 0:
    #     print('Invalid URLs:', invalid_urls)
    #     delete = input('Do you want to delete invalid files? (y/n): ')
    #     if delete.lower() == 'y':
    #         for filename in invalid_urls:
    #             os.remove(filename)
    #             print('Deleted:', filename)


def extract_url(data):
    pattern = re.compile(r'<key>URL</key>\s*<string>(.*)</string>')
    match = pattern.search(data)
    if match:
        return match.group(1)
    return None


def is_valid(url):
    try:
        r = requests.head(url)
        return r.status_code == 200
    except:
        # yellow warning
        print('Warning:', url, 'is not reachable')
        return False


def create_html_link_file(url, filename):
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename + '.html', 'w') as f:
        f.write('<html>\n<head>\n<meta http-equiv="refresh" content="0; url=' + url + '" />\n</head>\n</html>')


def convert(filename):
    with open(filename) as f:
        data = f.read()
    url = extract_url(data)
    if url:
        # Properly remove the extension and append .html
        base, _ = os.path.splitext(filename)
        create_html_link_file(url, base)
        print('Converted:', filename)
        os.remove(filename)
    else:
        print('No URL found in:', filename)


@click.command()
@click.argument('path')
@click.option('--silent', is_flag=True, default=False, help="don't ask for confirmation (DANGER!)")
#@click.option('--validate', is_flag=True, default=False, help='Validate URLs are reachable') # todo: implement
# @click.option("--delete-unreachable", is_flag=True, default=False, help="delete unreachable URLs") # todo: implement
def cli(path, silent):
    convert_all(path=path, silent=silent)


if __name__ == '__main__':
    cli()
