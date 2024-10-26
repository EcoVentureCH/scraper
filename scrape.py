#!/usr/bin/env python3
import sys
import os
import argparse
from os import listdir
from os.path import isfile, join
from importlib import import_module

from rich import print

path = "./sites"

def find_available_sites():
    sites = [f for f in listdir(path) if not isfile(join(path, f))]
    ret_val = {}
    for site in sites:
        site_path = join(path,site)
        py_files = [f for f in listdir(site_path) if isfile(join(site_path, f)) and f.endswith(".py")]
        ret_val[site] = py_files
    return ret_val

def print_available(sites):
    print("we have the following scrapers:")
    for k, v in sites.items():
        print(f"    {k}")
        if len(v) == 0:
            print(f"       <no scripts found!>")
        for script_name in v:
            print(f"       {script_name}")

def run_site(sites, site_name):
    if site_name not in sites:
        print(f"{site_name}: no directory in sites/ found with name {site_name}")
        return False
    scripts = sites[site_name]
    if (len(scripts) == 0):
        print(f"{site_name}: no python scrape scripts found")
        return False

    site = site_name
    site_path = join(path, site)
    py_files = [f for f in listdir(site_path) if isfile(join(site_path, f)) and f.endswith(".py")]

    print(f"{site}: starting!")
    print(f"{site}:", end=" ")
    for f in sorted(py_files):
        script_path = join(site_path, f)
        import_str = script_path[:-3].replace("./", "").replace(os.sep, ".")
        imp = import_module(import_str)
        try:
            main_func = getattr(imp, "main")
        except AttributeError as e:
            print()
            raise AttributeError(f"\nmake sure your script ({script_path}) has a main() function that returns a list of Project!") from e
        print(f"{f}", end=" ")
        project_datas = main_func()
        if not isinstance(project_datas, list):
            raise AttributeError(f"\nmake sure your script's ({script_path}) main() function returns a list of Project!")

        print()
        print(project_datas)
    return True
    
def main():
    parser = argparse.ArgumentParser(
        description='scraper command line interface',
    )
    subparsers = parser.add_subparsers(
        title='subcommand',
        help='chose one',
        dest='subcommand_name'
    )
    subparsers.required = True
    
    list_parser = subparsers.add_parser('list', help='list available sites')
    site_parser = subparsers.add_parser('run', help='run the scraper of a site')
    site_parser.add_argument('site', nargs='+', help='specific site to run')
    
    args = parser.parse_args()
    sites = find_available_sites()
    
    if args.subcommand_name == 'list':
        print_available(sites)
    elif args.subcommand_name == 'run':
        for s in args.site:
            success = run_site(sites, s)
            if not success:
                exit(1)

if __name__ == "__main__":
    main()
