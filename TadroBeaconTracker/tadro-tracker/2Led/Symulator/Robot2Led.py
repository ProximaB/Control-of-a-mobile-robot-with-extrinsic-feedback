from math import sin, cos
import numpy as np

class Robot2Led:
    def __init__(self, x_init, y_init, heading_init, diamater, axle_len, clr_led1, clr_led2, round_pos):
        self.x_pos = x_init
        self.y_pos = y_init
        self.heading = heading_init

        self.diamater = diamater
        self.axle_len = axle_len

        self.clr_led1 = clr_led1
        self.clr_led2 = clr_led2

        self.round_pos = round_pos

    def draw_robot(self, x_pos, y_pos, heading):
        pass
    
    #def simulate_path(self, velocity, trun, time_diff):
        # model - > x,y heading
    
    def simulate_robot(self, vel_0, vel_1, time_diff):
        vel = 1/2 * (vel_0 + vel_1)
        if vel_1 - vel_0 == 0:
            self.x_pos += sin(self.heading) * vel * time_diff
            self.y_pos += cos(self.heading) * vel * time_diff
            return
        #angular_vel = 1/self.axle_len(vel_0 - vel_1)

        #distance = vel * time_diff
        radius = self.axle_len / 2 * (vel_0 + vel_1) / (vel_1 - vel_0)

        # theta
        self.heading += (time_diff / self.axle_len) * (vel_1 - vel_0)

        th = self.heading
        self.x_pos += cos(th / 2) * ( 2 * radius * sin(th/2) )
        self.y_pos += sin(th / 2) * ( 2 * radius * sin(th/2) )

    def round_robot_properties(self):
        self.x_pos = round(self.x_pos, self.round_pos) 
        self.y_pos = round(self.y_pos, self.round_pos) 
        self.heading = np.round(self.heading, self.round_pos)

    def simulate_process(self, vel_0, vel_1, time_diff):
        self.simulate_robot(vel_0, vel_1, time_diff)
        self.round_robot_properties()
        #dead_zones()
        #interpolation_linear()
        #draw_robot()'''
      #  pass
        
if __name__ == "__main__":
    robot = Robot2Led(0,0,np.pi,2,2, (255,0,0), (0,0,255), 5)
    #robot.simulate_robot(20, 20, 10)
    robot.simulate_process(20, 20, 10)
    print(f"|x_pos:{robot.x_pos}| y_pos:{robot.y_pos}| heading:{robot.heading}|")
    robot.simulate_process(0, 0, 0)
    print(f"|x_pos:{robot.x_pos}| y_pos:{robot.y_pos}| heading:{robot.heading}|")