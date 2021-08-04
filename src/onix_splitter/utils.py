import logging
import os
import shutil


def clear_folder(folder: str) -> None:
    """Remove all the contents of the folder.

    :param folder: The folder which content should be removed
    :type folder: str
    """
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                if filename != ".gitignore":
                    os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logging.exception(f"Failed to delete {file_path}. Reason: {e}")
