import cv2 as cv
import sys

from application import Application
from directory_reader import DirectoryReader
import global_vars

if __name__ == '__main__':
    # Check argv
    if len(sys.argv) < 3:
        sys.exit(
            'Missing required arguments!\n'
            'Parameters: sequence_directory mode [is_watershed?|default: 0] '
            '[show_preprocessed?|default: 0]\n'
            'Modes: 0 -> DIC, 1 -> Fluo, 2 -> PhC\n'
            'Examples:\n'
            f'python3 {sys.argv[0]} path/to/images 1\n'
            f'python3 {sys.argv[0]} path/to/images 2 0 1'
        )

    # Get files
    sequence_files = DirectoryReader(sys.argv[1]).get_sequence_files()
    if len(sequence_files) == 0:
        sys.exit(f"There are no files in '{sys.argv[1]}'.")

    # Init global vars
    global_vars.init()

    # Segmentation mode
    if len(sys.argv) >= 4 and int(sys.argv[3]) > 0:
        global_vars.is_watershed = True

    # Show pre-processed flag
    if len(sys.argv) >= 5 and int(sys.argv[4]) > 0:
        global_vars.show_preprocessed = True    # If not zero show

    # Run App
    Application(sequence_files, int(sys.argv[2])).run()
