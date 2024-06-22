from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define directories
source_dir = "/Users/james/Downloads"
dest_dirs = {
    "images": "/Users/james/Classif_Downs/Images_",
    "videos": "/Users/james/Classif_Downs/Videos_",
    "audio": "/Users/james/Classif_Downs/Music_",
    "documents": "/Users/james/Classif_Downs/Docs_",
    "programs": "/Users/james/Classif_Downs/Programs_",
    "compressed": "/Users/james/Classif_Downs/Compressed_",
}

# Define file extensions
file_extensions = {
    "images": {
        ".jpg",
        ".jpeg",
        ".jpe",
        ".jif",
        ".jfif",
        ".jfi",
        ".png",
        ".gif",
        ".webp",
        ".tiff",
        ".tif",
        ".psd",
        ".raw",
        ".arw",
        ".cr2",
        ".nrw",
        ".k25",
        ".bmp",
        ".dib",
        ".heif",
        ".heic",
        ".ind",
        ".indd",
        ".indt",
        ".jp2",
        ".j2k",
        ".jpf",
        ".jpf",
        ".jpx",
        ".jpm",
        ".mj2",
        ".svg",
        ".svgz",
        ".ai",
        ".eps",
        ".ico",
    },
    "videos": {
        ".webm",
        ".mpg",
        ".mp2",
        ".mpeg",
        ".mpe",
        ".mpv",
        ".ogg",
        ".mp4",
        ".mp4v",
        ".m4v",
        ".avi",
        ".wmv",
        ".mov",
        ".qt",
        ".flv",
        ".swf",
        ".avchd",
    },
    "audio": {".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"},
    "documents": {
        ".doc",
        ".docx",
        ".odt",
        ".pdf",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".csv",
        ".ods",
        ".epub",
        ".txt",
    },
    "programs": {".dmg", ".pkg", ".img", ".rar"},
    "compressed": {".zip", ".gz"},
}


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(join(dest, name)):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


def move_file(dest, entry, name):
    if exists(join(dest, name)):
        unique_name = make_unique(dest, name)
        rename(join(dest, name), join(dest, unique_name))
    move(entry.path, join(dest, name))
    logging.info(f"Moved {name} to {dest}")


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    self.check_and_move(entry)

    def check_and_move(self, entry):
        name = entry.name
        for category, extensions in file_extensions.items():
            if any(name.lower().endswith(ext) for ext in extensions):
                move_file(dest_dirs[category], entry, name)
                break


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
