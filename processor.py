import cv2 as cv
import sys
import time
import cell_db

from boxes_drawer import BoxesDrawer
from cell import Cell
from cell_associator import CellAssociator
from directory_reader import DirectoryReader
from preprocessor import Preprocessor
from watershed_cell_locator import WatershedCellLocator
from ellipse_fitter import EllipseFitter
from watershed import Watershed


class Processor:
    def __init__(self, file, mode, segment_mode, prev_snapshots):
        self.file = file
        self.mode = mode
        self.segment_mode = segment_mode
        self.prev_snapshots = prev_snapshots
        self.curr_snapshots = None

    def process(self):
        # Read image
        image = cv.imread(self.file, cv.IMREAD_GRAYSCALE)

        # Preprocess image
        preprocessed_image = Preprocessor(image, self.mode).preprocess()

        # Segment image
        if self.segment_mode != 0:
            segmented_image = Watershed(
                preprocessed_image, self.mode
            ).perform()

            # Find segments
            self.curr_snapshots = WatershedCellLocator(
                segmented_image
            ).locate()
        else:
            self.curr_snapshots = EllipseFitter(preprocessed_image).fit()

        # Associate
        self.associate_cells()

        # Draw bounding box
        if self.mode == 1:   # Fluo
            bottom_layer = preprocessed_image
        else:
            bottom_layer = image
            # bottom_layer = preprocessed_image

        boxed_image = BoxesDrawer(self.curr_snapshots, bottom_layer).draw()
        return boxed_image, self.curr_snapshots

    def associate_cells(self):
        if self.prev_snapshots is None:  # Initialize (Frame 0)
            for snapshot in self.curr_snapshots:
                new_id = len(cell_db.cells)  # ID of new cell
                cell = Cell(new_id, snapshot.centroid)  # New Cell
                cell_db.cells.append(cell)              # Add to DB

                # Associate snapshot with the new cell
                snapshot.associate(cell)
            return self.curr_snapshots
        else:
            # Association threshold
            if self.mode == 0:   # DIC
                dthreshold = 5
            elif self.mode == 1:   # Fluo
                threshold = 30
            else:  # PhC
                threshold = 10

            # Association happens here
            associator = CellAssociator(
                self.curr_snapshots, self.prev_snapshots, threshold
            )
            return associator.associate()


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

    # Run
    print(f'There are {len(sequence_files)} images.')
    mode = int(sys.argv[2])
    for i, file in enumerate(sequence_files):
        print(f'Processing file {i}...')
        image = Processor(file, mode).process()
        cv.imwrite(f'result_sequence/{i:04d}.png', image)
        print(f'File {i} done!')
