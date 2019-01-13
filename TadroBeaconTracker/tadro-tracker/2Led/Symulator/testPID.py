import sys
from RobotSim2Led import RobotSim2Led
''' Import custom modules '''
# add local path to make interpreter able to obtain custom modules. (when u run  py from glob scope)
sys.path.insert(0, r'C:/Users/barte/Documents/Studia VII/Image_processing/TadroBeaconTracker/tadro-tracker/2Led/')
from PID import PID

import time
import matplotlib.pyplot as plt
import numpy as np
from math import *
#from scipy.interpolate import spline
from scipy.interpolate import BSpline, make_interp_spline #  Switched to BSpline

def angle(A, B):
    return atan2(B[1]-A[1], B[0]-A[0])

def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class
    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    TARGET_POS = (0.0, 10.0)
    TARGET_HEADING = np.pi
    robot = RobotSim2Led(0, 0, 0, 10, 10, None, None, 10)
    pid1 = PID(P, I, D)
    pid2 = PID(P, I, D)

    pid1.SetPoint=0
    pid1.setSampleTime(0.01)

    pid2.SetPoint= 0
    pid2.setSampleTime(0.01)

    END = L
    robot.simulate_robot_process(0, 0, 10)
    feedback1 = 0# sqrt( (robot.x_pos-TARGET_POS[0])**2 + (robot.y_pos-TARGET_POS[1]) **2)
    feedback2 = 0# robot.heading

    feedback_list1 = []
    time_list1 = []
    setpoint_list1 = []

    feedback_list2 = []
    time_list2 = []
    setpoint_list2 = []

    for i in range(1, END):
        pid1.update(feedback1)
        pid2.update(feedback2)
        print(f'feedback1:{feedback1}, feedback2:{feedback2}')

        output1 = pid1.output #* 0.02
        output2 = pid2.output #* 0.02 #output ~= 23 dla roznicy pi w stosunku do target = pi, robot 0
        print(f'output1:{output1}, output2:{output2}')
        '''
        if pid.SetPoint > 0:
            feedback += (output - (1/i))
        '''

        if i==2:
            pid1.SetPoint = sqrt( (robot.x_pos-TARGET_POS[0])**2 + (robot.y_pos-TARGET_POS[1]) **2)
            pid2.SetPoint = TARGET_HEADING
        
        vel1 = output2*cos(output2)
        vel2 =  output2*sin(output2)
        print(f'vel1:{vel1}, vel2:{vel2}')
        #if output2 != 0:
            #robot.simulate_robot_process(output2*cos(TARGET_HEADING-robot.heading), output2*sin(TARGET_HEADING-robot.heading), 10)
        #robot.simulate_robot_process(0, 0, 10)
        poz = (robot.x_pos, robot.y_pos)
        ang = angle(TARGET_POS, poz)
        robot.simulate_robot_process(-output2 * (robot.heading - ang), output2 * (robot.heading - ang), 0.1)
        feedback1 = sqrt( (TARGET_POS[0] - robot.x_pos)**2 + (TARGET_POS[1] - robot.y_pos) **2)
        feedback2 = robot.heading - ang
        time.sleep(0.01)

        feedback_list1.append(feedback1)
        setpoint_list1.append(pid1.SetPoint)
        time_list1.append(i)

        feedback_list2.append(feedback2)
        setpoint_list2.append(pid2.SetPoint)
        time_list2.append(i)

    time_sm1 = np.array(time_list1)
    time_smooth1 = np.linspace(time_sm1.min(), time_sm1.max(), 300)
    time_sm2 = np.array(time_list2)
    time_smooth2 = np.linspace(time_sm2.min(), time_sm2.max(), 300)

    # feedback_smooth = spline(time_list, feedback_list, time_smooth)q
    # Using make_interp_spline to create BSpline
    helper_x31 = make_interp_spline(time_list1, feedback_list1)
    feedback_smooth1 = helper_x31(time_smooth1)

    helper_x32 = make_interp_spline(time_list2, feedback_list2)
    feedback_smooth2 = helper_x32(time_smooth2)

    f = plt.figure(1)
    plt.plot(time_smooth1, feedback_smooth1)
    plt.plot(time_list1, setpoint_list1)
    plt.xlim((0, L))
    #plt.ylim((min(feedback_list1)-0.5, max(feedback_list1)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('dist (PV)')
    plt.title('TEST PID')
    #plt.ylim((1-0.5, 1+0.5))
    plt.grid(True)
    
    theta = plt.figure(2)
    plt.plot(time_smooth2, feedback_smooth2)
    plt.plot(time_list2, setpoint_list2)
    plt.xlim((0, L))
    #plt.ylim((min(feedback_list2)-0.5, max(feedback_list2)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('theta (PV)')
    plt.title('TEST PID')
   
    #plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    f.show()
    theta.show()
    input()
if __name__ == "__main__":
    #test_pid(1.2, 1, 0.001, L=200)
    test_pid(4, 0, 0.001, L=200)
#    test_pid(0.8, L=50)