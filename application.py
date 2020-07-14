import cv2 as cv
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from processor import Processor


class Application:
    def __init__(self, sequence_files):
        # Files
        self.sequence_files = sequence_files
        self.file_count = len(sequence_files)
        # States
        self.time_point = 0
        self.paused = False
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
        return cv.imread(self.file, cv.IMREAD_GRAYSCALE)
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
        self.paused = not self.paused   # Toggle state
        if self.paused:  # Pause
            self.button.label.set_text('Continue')
        else:            # Play
            self.button.label.set_text('Pause')
            self.next_step()

        plt.draw()

    def next_step(self):
        if self.paused:  # If paused, next step does nothing
            return

        if self.time_point + 1 == self.file_count:  # At the end of sequence
            self.paused = True
            self.button_ax.set_visible(False)   # Remove button
            plt.draw()
            return

        self.time_point += 1    # Increase state
        image = self.process_current_image()    # Process image
        self.plot_image.set_data(image)         # Replace image
        plt.draw()                              # Redraw plot

        print(self.time_point)

        # Start timer
        self.create_timer().start()  # Start timer
