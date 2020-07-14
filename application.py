import cv2 as cv
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from processor import Processor


class Application:
    # STATE constant
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3

    def __init__(self, sequence_files):
        # Files
        self.sequence_files = sequence_files
        self.file_count = len(sequence_files)
        # States
        self.time_point = 0
        self.state = Application.RUNNING
        # Plot  objects
        self.figure = None
        self.plot_image = None
        self.button = None
        self.button_ax = None

    def run(self):
        self.figure, _ = plt.subplots(num='Cell Tracking')  # Get figure

        plt.axis(False)    # Turn off axis

        # Process initial image
        image = self.process_current_image()

        # Setup plot_image showing initial image
        self.plot_image = plt.imshow(image)

        # Initialize button.
        # Note: the instance has to be returned. If doesn't, it won't work
        self.button, self.button_ax = self.init_button()

        # Start timer
        self.create_timer().start()

        # Show plot
        plt.show()

    def process_current_image(self):
        # Note: Processing is slow: you can switch the comment to try
        return cv.imread(self.sequence_files[self.time_point], cv.IMREAD_GRAYSCALE)
        # return plt.imread(self.sequence_files[self.time_point])
        # return Processor(self.sequence_files[self.time_point]).process()

    def init_button(self):
        button_ax = plt.axes([0.45, 0.01, 0.15, 0.075])  # Button position
        button = Button(button_ax, 'Pause')
        button.on_clicked(self.click_button)
        return button, button_ax

    def create_timer(self):
        timer = self.figure.canvas.new_timer(interval=200)
        timer.add_callback(self.next_step)
        return timer

    def click_button(self, event):
        print('clicked')
        if self.state == Application.RUNNING:
            self.state = Application.PAUSED
            self.button.label.set_text('Continue')
            plt.draw()
        else:   # PAUSED or STOPPED
            if self.state == Application.STOPPED:
                self.time_point = -1    # Reset to beginning
            self.state = Application.RUNNING
            self.button.label.set_text('Pause')

    def next_step(self):
        print(self.time_point, self.state)
        if not (self.state == Application.RUNNING):
            return  # If not running, does nothing

        if self.time_point + 1 == self.file_count:  # At the end of sequence
            self.state = Application.STOPPED
            self.button.label.set_text('Rerun')
            plt.draw()
            return

        self.time_point += 1    # Increase time point
        image = self.process_current_image()    # Process image
        self.plot_image.set_data(image)         # Replace image
        plt.draw()                              # Redraw plot
