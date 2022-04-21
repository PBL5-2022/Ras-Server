import os
import time
import traceback


class FileModified():
    def __init__(self, file_path):
        self.file_path = file_path
        self.modifiedOn = os.path.getmtime(file_path)

    def start(self):
        try:
            while (True):
                time.sleep(0.5)
                modified = os.path.getmtime(self.file_path)
                if modified != self.modifiedOn:
                    self.modifiedOn = modified
                    if self.file_modified():
                        break
        except Exception as e:
            print(traceback.format_exc())

    def file_modified(self):
        print("File Modified!")
        return False


if __name__ == "__main__":
    fileModifiedHandler = FileModified(r"testfile.txt")
    fileModifiedHandler.start()
