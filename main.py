import cv2 as cv
import sys

from application import Application
from directory_reader import DirectoryReader
import global_vars

if __name__ == '__main__':
    # Check argv
    if len(sys.argv) < 3:
        sys.exit(
            'Wrong number of arguments.\n'
            'Parameters: sequence_directory mode\n'
            f'Example: python3 {sys.argv[0]} path/to/images 1\n'
            'Modes are 0: DIC, 1: Fluo, 2: PhC'
        )

    # Segmentation mode
    if len(sys.argv) >= 4:
        segment_mode = int(sys.argv[3])  # if not zero, then watershed
    else:
        segment_mode = 0

    # Get files
    sequence_files = DirectoryReader(sys.argv[1]).get_sequence_files()
    if len(sequence_files) == 0:
        sys.exit(f"There are no files in '{sys.argv[1]}'.")

    # Init global vars
    global_vars.init()

    # Show pre-processed flag
    if len(sys.argv) >= 4 and int(sys.argv[3]) == 1:
        global_vars.show_preprocessed = True

    # Run App
    Application(sequence_files, int(sys.argv[2]), segment_mode).run()
