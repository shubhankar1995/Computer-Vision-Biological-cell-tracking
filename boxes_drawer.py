import cv2 as cv
from contrast_stretcher import ContrastStretcher


class BoxesDrawer:
    def __init__(self, segments, image):
        self.segments = segments
        self.image = image

    def draw(self):
        # Convert to color
        color_image = cv.cvtColor(self.image, cv.COLOR_GRAY2RGB)

        # Draw all
        for segment in self.segments:
            color_image = BoxesDrawer.draw_segment(segment, color_image)
        return color_image

    def draw_segment(segment, image):
        top_left, bottom_right, _ = segment
        return cv.rectangle(
            image, tuple(top_left[::-1]), tuple(bottom_right[::-1]),
            (0, 0, 255), 2
        )
