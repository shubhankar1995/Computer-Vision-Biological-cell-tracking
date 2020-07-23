import cv2 as cv
import sys

from application import Application
from directory_reader import DirectoryReader
import cell_db

if __name__ == '__main__':
    # Check argv
    if len(sys.argv) < 3:
        sys.exit(
            'Wrong number of arguments.\n'
            'Parameters: sequence_directory mode\n'
            f'Example: python3 {sys.argv[0]} path/to/images 1\n'
            'Modes are 0: DIC, 1: Fluo, 2: PhC'
        )

    # Get files
    sequence_files = DirectoryReader(sys.argv[1]).get_sequence_files()
    if len(sequence_files) == 0:
        sys.exit(f"There are no files in '{sys.argv[1]}'.")

    # Init cell db
    cell_db.init()

    # Run App
    Application(sequence_files, int(sys.argv[2])).run()
