import cv2 as cv
import sys
import matplotlib.pyplot as plt
import cell_db
from matplotlib.widgets import Button

from processor import Processor
from cell_identifier import CellIdentifier
from matplotlib import cm


class Application:
    # STATE constant
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3

    def __init__(self, sequence_files, mode):
        # Files
        self.sequence_files = sequence_files
        self.file_count = len(sequence_files)
        # Preprocessing Mode
        self.mode = mode
        # States
        self.time_point = 0
        self.state = Application.RUNNING
        # Plot objects
        self.figure = None
        self.plot_image = None
        self.subplot = None
        self.button = None
        self.button_ax = None
        self.counts_text = None
        self.clicked_cell_text = None
        self.metrics_text = None
        # Snapshots
        self.prev_snapshots = None
        self.curr_snapshots = None

    def run(self):
        self.figure = self.init_figure()  # Get figure

        plt.axis(False)    # Turn off axis

        # Process initial image
        image, self.curr_snapshots = self.process_current_image()

        # Setup plot_image and counts text
        self.plot_image = plt.imshow(image)
        self.counts_text = plt.text(0, -10, self.produce_counts_text())
        self.clicked_cell_text = plt.text(300, -10, '')
        self.metrics_text = plt.text(500, -10, '')

        # Get subplot for the image
        self.subplot = self.figure.get_axes()[0]

        # Initialize button.
        # Note: the instance has to be returned. If doesn't, it won't work
        self.button, self.button_ax = self.init_button()

        # Start timer
        self.create_timer().start()

        # Click event handler
        cid = self.figure.canvas.mpl_connect('button_press_event',
                                             self.click_image)

        # Show plot
        plt.show()

    def init_figure(self):
        # Read first image
        first_image = cv.imread(self.sequence_files[0], cv.IMREAD_GRAYSCALE)
        # Detemine figsize
        height, width = first_image.shape
        if self.mode == 1:
            dpi = 120.0
        else:
            dpi = 80.0
        figsize = width / dpi, height / dpi

        return plt.figure(num='Cell Tracking', figsize=figsize)

    def process_current_image(self):
        # Note: Processing is slow: you can switch the comment to try
        # return cv.imread(self.sequence_files[self.time_point], cv.IMREAD_GRAYSCALE)
        # return plt.imread(self.sequence_files[self.time_point])
        return Processor(
            self.sequence_files[self.time_point], self.mode, self.prev_snapshots
        ).process()

    def produce_counts_text(self):
        return (
            f'Cell Count: {len(self.curr_snapshots)}\n'
            f'Mitosis Count: {self.count_mitosis()}\n'
            f'Frame: {self.time_point}'
        )

    def count_mitosis(self):
        return sum(1 for snapshot in self.curr_snapshots
                   if snapshot.is_mitosis)

    def init_button(self):
        button_ax = plt.axes([0.45, 0.01, 0.15, 0.075])  # Button position
        button = Button(button_ax, 'Pause')
        button.on_clicked(self.click_button)
        return button, button_ax

    def click_button(self, event):
        if self.state == Application.RUNNING:
            self.state = Application.PAUSED
            self.button.label.set_text('Continue')
            plt.draw()
        else:   # PAUSED or STOPPED
            if self.state == Application.STOPPED:
                self.time_point = -1    # Reset to beginning
            self.state = Application.RUNNING
            self.button.label.set_text('Pause')

    def create_timer(self):
        timer = self.figure.canvas.new_timer(interval=200)
        timer.add_callback(self.next_step)
        return timer

    def next_step(self):
        # if self.time_point == 1:
        #     sys.exit()
        if not (self.state == Application.RUNNING):
            return  # If not running, does nothing

        if self.time_point + 1 == self.file_count:  # At the end of sequence
            self.state = Application.STOPPED
            self.button.label.set_text('Rerun')
            plt.draw()
            return

        if self.time_point + 1 == 0:    # Rerun
            self.curr_snapshots = None  # Remove all snapshots
            cell_db.cells = list()      # Reset all cells
            self.subplot.lines = list()  # Remove all lines
            # Reset text
            self.counts_text.set_text('')
            self.clicked_cell_text.set_text('')
            self.metrics_text.set_text('')

        self.time_point += 1    # Increase time point
        # Replace prev snapshots to current, and current to new ones
        self.prev_snapshots = self.curr_snapshots
        image, self.curr_snapshots = self.process_current_image()

        self.update_plot(image)         # Update image
        plt.draw()                              # Redraw plot

    def update_plot(self, image):
        self.plot_image.set_data(image)
        self.counts_text.set_text(self.produce_counts_text())
        self.draw_tracks()              # Draw tracks for current snapshots

    def draw_tracks(self):
        cmap = cm.get_cmap('viridis')
        for c in self.curr_snapshots:
            if c.prev_snapshot is not None and c.cell is not None:
                p = c.prev_snapshot
                self.subplot.plot(
                    [p.centroid[1], c.centroid[1]],
                    [p.centroid[0], c.centroid[0]],
                    linewidth=1, color=cmap(c.cell.id)
                )

    def click_image(self, event):
        if not (event.inaxes == self.subplot):
            return
        if event.ydata == None or event.xdata == None:
            return

        # print('xdata=%f, ydata=%f' % (event.xdata, event.ydata))
        snapshot = self.identify_cell(event.ydata, event.xdata)
        self.update_cell_metrics(snapshot)

    def identify_cell(self, y, x):
        return CellIdentifier(self.curr_snapshots, y, x).identify()

    def update_cell_metrics(self, snapshot):
        if snapshot is None:
            self.clicked_cell_text.set_text('')
            self.metrics_text.set_text('')
            return

        cell_text = (
            f'Cell ID: {snapshot.cell.id}\n'
            f'Click Frame: {self.time_point}'
        )
        self.clicked_cell_text.set_text(cell_text)

        metrics_text = (
            f'Speed: {snapshot.get_speed_display()}\n'
            f'Total Distance: {snapshot.get_total_distance()}\n'
            f'Net Distance: {snapshot.calc_net_distance()}'
        )
        self.metrics_text.set_text(metrics_text)
