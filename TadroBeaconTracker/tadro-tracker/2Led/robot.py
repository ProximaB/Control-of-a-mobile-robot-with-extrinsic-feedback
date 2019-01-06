import numpy as np

class Robot():
    def __init__(self, time, position, heading):
        self.time = time
        self.position = position
        self.heading = heading

    def print(self):
        print("|Time: {0:7.3f}, Position: ({1[0]:4}, {1[1]:4}), Heading: {2:7.4f}, {3:6.2f}|"
            .format(self.time, self.position, self.heading, self.heading*180.0/np.pi))
    
class Robot2Led(Robot):
    def __init__(self, time, position, left_led_pos, right_led_pos, heading):
        self.left_led_pos = left_led_pos
        self.right_led_pos = right_led_pos
        Robot.__init__(self, time, position, heading)