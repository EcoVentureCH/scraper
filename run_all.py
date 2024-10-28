import os
import time
import sys
import requests
from os import listdir
from os.path import isfile, join
from importlib import import_module

import src.csv_manager as manager

def main():
    time_out_after_job = 7 * 60 # in seconds

    csv_filename = "projects.csv"

    # first commandline argument is the base path where the data is stored
    # if not provided, the base path is where this file is.
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
        csv_filename = base_path + "/" + csv_filename

    print("using csv filename:", csv_filename)

    path = "./sites"
    sites = [f for f in listdir(path) if not isfile(join(path, f))]

    for site in sites:
        site_path = join(path,site)
        py_files = [f for f in listdir(site_path) if isfile(join(site_path, f)) and f.endswith(".py")]

        if py_files:
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
                if not project_datas:
                    raise AttributeError(f"\nmake sure your script's ({script_path}) main() function returns a list of Project!")
        
                changed = manager.update_csv(project_datas, csv_filename=csv_filename)
                if changed:
                    print("(*)", end="")
                else:
                    print("( )", end="")

            print()
        else:
            print(f"{site}: no scripts found!")


    response = requests.post('http://web:8000/api/reload-projects')        
    try:
        response.raise_for_status()
        print(f"INFO: reloaded projects successfully: {response.json()}")
    except requests.RequestException as e:
        print(response.content)
        print(f"ERROR: Failed to execute command: {e}")

    time.sleep(time_out_after_job)

if __name__ == "__main__":
    main()
