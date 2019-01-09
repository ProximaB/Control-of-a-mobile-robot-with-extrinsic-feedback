import numpy as np

class Robot():
    def __init__(self, time, robot_center, heading):
        self.time = time if time != None else ''
        self.robot_center = robot_center if robot_center != None else ''
        self.heading = heading if heading != None else ''

    def update(self, time, robot_center, heading):
        self.time = time if time != None else ''
        self.robot_center = robot_center if robot_center != None else ''
        self.heading = heading if heading != None else ''


    def print(self):
        try:
            print("|Time: {0:7.3f}, Position: ({1[0]:4}, {1[1]:4}), Heading: {2:7.4f}, {3:6.2f}|"
                .format(self.time, self.robot_center, self.heading, self.heading*180.0/np.pi))
        except Exception as e:
            raise e
    
class Robot2Led(Robot):
    def __init__(self, time, robot_center, led1_pos, led2_pos, heading):
        self.left_led_pos = led1_pos if led1_pos != None else ''
        self.right_led_pos = led2_pos if led2_pos != None else ''
        Robot.__init__(self, time, robot_center, heading)

    def update(self, time, robot_center, led1_pos, led2_pos, heading):
        self.left_led_pos = led1_pos if led1_pos != None else ''
        self.right_led_pos = led2_pos if led2_pos != None else ''
        self.time = time if time != None else ''
        self.robot_center = robot_center if robot_center != None else ''
        self.heading = heading if heading != None else ''
