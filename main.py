import cv2 as cv
import sys

from application import Application
from directory_reader import DirectoryReader

if __name__ == '__main__':
    # Check argv
    if len(sys.argv) < 2:
        sys.exit(
            'Please provide the path to images sequence directory.\n'
            f'Example: python3 {sys.argv[0]} path/to/images'
        )

    # Get files
    sequence_files = DirectoryReader(sys.argv[1]).get_sequence_files()
    if len(sequence_files) == 0:
        sys.exit(f"There are no files in '{sys.argv[1]}'.")

    # Run App
    Application(sequence_files).run()
