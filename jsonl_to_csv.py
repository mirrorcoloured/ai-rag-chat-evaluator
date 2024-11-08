import sys
import os

import pandas


def jsonl_to_csv(filepath: str, verbose: bool = True):
    filename = os.path.basename(filepath)
    folder = os.path.dirname(filepath)
    new_filename = os.path.splitext(filename)[0] + ".csv"
    new_filepath = os.path.join(folder, new_filename)
    if verbose:
        print(f"Creating {new_filepath} from {filepath}")
    try:
        pandas.read_json(filepath, lines=True).to_csv(new_filepath, index=False)
    except PermissionError:
        print(f"Cannot write to {new_filepath} . Please close the file or allow write permissions.")
        retry = ""
        while "n" not in retry and "y" not in retry:
            retry = input("Retry (y/n)? ")
            if "n" in retry:
                if verbose:
                    print(f"Skipping {filepath}")
                return
            elif "y" in retry:
                jsonl_to_csv(filepath, verbose)


if __name__ == "__main__":
    args = sys.argv[1:]
    for arg in args:
        assert os.path.exists(arg), f"{arg} does not exist"
        if os.path.isfile(arg):
            jsonl_to_csv(arg)
        elif os.path.isdir(arg):
            for root, folders, files in os.walk(arg):
                for file in files:
                    if os.path.splitext(file)[-1] == ".jsonl":
                        jsonl_to_csv(os.path.join(root, file))
