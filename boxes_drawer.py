import cv2 as cv
from contrast_stretcher import ContrastStretcher


class BoxesDrawer:
    def __init__(self, snapshots, image):
        self.snapshots = snapshots
        self.image = image

    def draw(self):
        # Convert to color
        color_image = cv.cvtColor(self.image, cv.COLOR_GRAY2RGB)

        # Draw all
        for snapshot in self.snapshots:
            color_image = BoxesDrawer.draw_box(snapshot, color_image)
        return color_image

    def draw_box(snapshot, image):
        if snapshot.is_mitosis:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)

        return cv.rectangle(
            image, tuple(snapshot.top_left[::-1]),
            tuple(snapshot.bottom_right[::-1]),
            color, 1
        )
