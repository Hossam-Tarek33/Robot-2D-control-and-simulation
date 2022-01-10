#!/usr/bin/env python
import rospy
from robot_zal.msg import position_list

##Function to check if the inputs are valid
def check_user_input(x,y,vel):
    if (len(x) != len(y)):
        print("The number of the enetered X-positions are not equal to the Y-positions!!")
        return False
    if (len(x) != len(vel) or len(y) != len(vel)):
        print("The number of the enetered positions are not equal to the velocities!!")
        return False
    for i in range(len(x)):
        if (x[i] > 250 or x[i] < 0):
            print("You have entered an invalid X-value --- Please add a valid position values")
            return False
    for i in range(len(y)):
        if (y[i] > 250 or y[i] < 0):
            print("You have entered an invalid Y-value --- Please add a valid position values")
            return False
    for i in range(len(vel)):
        if (vel[i] == 0):
            print("The robot will not move as the entered velocity value is 0.0")
            return False
    return True

##Function recieves the target positions from the user
def position_inputs():
    x = []
    y = []
    inputs = raw_input("positions: ").split()
    for i in range (len(inputs)):
        if i%2 == 0:
            point_x = float(inputs[i])
            x.append(point_x)
        else:
            point_y = float(inputs[i])
            y.append(point_y)  
    return x, y  

##Function recieves the velocity from the user
def velocity_input():
    vel = []
    inputs_vel = raw_input("velocities: ").split()
    for i in range (len(inputs_vel)):
        point_vel = float(inputs_vel[i])
        vel.append(point_vel)
    return vel

##Here is the controller node that publishes the position and velocity values to the robot
def controller():
    pub = rospy.Publisher('position', position_list, queue_size=10) 
    rospy.init_node('controller', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo("Enter the X and Y positions seperated by a space (values between 0 and 250)")
        
        x, y = position_inputs()
        vel = velocity_input()
        
        if check_user_input(x,y,vel):
            msg = position_list()
            msg.x = x
            msg.y = y
            msg.vel = vel
            pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInterruptException:
        pass

