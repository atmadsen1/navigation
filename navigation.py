from multi_ball_tracker import FrameProcessor

class Frame:
    """
    Starts the calculations done to locate the balls in the frame.
    :param frame: numpy array that is provided from cv2:VideoCapture:read()
    :param color_range: a dictionary in the form of
        {color_identifier : (hsv_min, hsv_max) } as calculated from
        range-detector.py
    :param frame_count: optional interger used to describe the frame number
    """
    def __init__(self, frame, color_range, frame_count=0):
        self.frame = frame
        self.frame_count = frame_count
        self.color_range = color_range
        self.frameProcessor = FrameProcessor(frame, frame_count, color_range)
        self.frameProcessor.start()

    """
    Checks to see if the frame processor has finished calculating
    the location of balls in the frame
    """
    def result_available(self):
        return self.frameProcessor.isAlive()

    """
    Get the center of the ball that is identified by the color(arg1).
    Note: This uses cv2.minEnclosingCircle(). This result can be
    different by several pixels from the moment center. The difference
    between these two methods is documented at https://docs.opencv.org/3.1.0/d3/dc0/group__imgproc__shape.html#ga8ce13c24081bbc7151e9326f412190f1.
    """
    def get_circle_center(self, color):
        if self.frameProcessor.get_balls() is not None:
            return self.frameProcessor.get_balls().get(color)[1]
        return (-1, -1)
    """
    Get the center of the ball that is identified by the color(arg1).
    Note: This uses cv2.moments(c) to calculate the center pixel of
    the ball. This will always an integer pair.
    The difference between these two methods is documented at https://docs.opencv.org/3.1.0/d3/dc0/group__imgproc__shape.html#ga8ce13c24081bbc7151e9326f412190f1.
    """
    def get_moment_center(self, color):
        if self.frameProcessor.get_balls() is not None:
            return self.frameProcessor.get_balls().get(color)[2]
        return (-1, -1)

    def get_circle_radius(self, color):
        if self.frameProcessor.get_balls() is not None:
            return self.frameProcessor.get_balls().get(color)[3]
        return -1

class CameraCapture:
    def __init__(self):
        pass

    def get_current_position(self):
        pass

class Navigation(threading.Thread):

    def __init__(self, autonomy):
        self.autonomy = autonomy
        self.run_flag = True
        self.camera = CameraCapture()

    def run(self):
        while self.run_flag:
            position = camera.get_current_position()
            autonomy.update_current_position(position)


if __name__ == "__main__":
    pass


