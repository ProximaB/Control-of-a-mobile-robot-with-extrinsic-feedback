class Robot2Led:
    def __init__(self, x_init, y_init, diamater, axle_len, clr_led1, clr_led2):
        self.x_init = x_init
        self.y_init = y_init

        self.diamater = diamater
        self.axle_len = axle_len

        self.clr_led1 = clr_led1
        self.clr_led2 = clr_led2

    def draw_robot(self, x_pos, y_pos, heading):
        pass
    
    #def simulate_path(self, velocity, trun, time_diff):
        # model - > x,y heading
    
    def simulate_robot(self, vel_0, vel_1, time_diff):
        vel = 1/2 * (vel_0 + vel_1)
        angular_vel = 1/self.axle_len(vel_0 - vel_1)

        distance = vel * time_diff
        radius = self.axle_len/2 * (vel_0 + vel_1) / (vel_1 / vel_0)