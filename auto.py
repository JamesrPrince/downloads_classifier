import os

source_dir = "/Users/james/Downloads"

with os.scandir(source_dir) as entries:
    for entry in entries:
        print(entry.name)
