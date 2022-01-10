#!/usr/bin/env python
import rospy 
import math
from tkinter import *
from robot_zal.msg import position_list

##Creating the GUI using tkinter lib
main = Tk()
main.geometry("260x260")
enviroment = Canvas(main, width=250, heigh=250, bg="white")
enviroment.pack(pady=10)
robot_obj = enviroment.create_oval(125,125,130,130, fill="black")
speed = 0
time = 0

#This function returns the current position of the robot from the GUI
def robot_current_position():
    current_x= float(enviroment.coords(robot_obj)[0])
    current_y= float(enviroment.coords(robot_obj)[1])
    return current_x, current_y

#This function computes the distance between the robot and the desired target
def distance(target_x, target_y, data):
    current_x , current_y = robot_current_position()
    pos_x = target_x - current_x
    pos_y = target_y - current_y 
    dist = math.sqrt((pos_x**2) + (pos_y**2))
    return pos_x, pos_y, dist

##This is the callback function that performs the movement of the robot  
def move(data):
    for i in range(len(data.x)):
        rospy.loginfo("Moving to target position: %d %d", data.x[i], data.y[i])
        current_x , current_y = robot_current_position()
        target_x = data.x[i]
        target_y = data.y[i]
        pos_x, pos_y, dist = distance(target_x, target_y, data)

        global speed
        speed = data.vel[i]
        global time
        time = int((dist * 1/speed) / 1000)  
        while (abs(current_x - target_x) > 0.001 or abs(current_y - target_y) > 0.001):       
            enviroment.move(robot_obj, pos_x*speed, pos_y*speed)
            current_x = round(float(enviroment.coords(robot_obj)[0]),2)
            current_y = round(float(enviroment.coords(robot_obj)[1]),2)
            publish_data()
            main.after(time, publish_data)  ##This line aims to keep publishing the robot state during robot movement (For visualization only)
        speed = 0  

##This function publishes the robot current data back
def publish_data():
    pub = rospy.Publisher("robot_status", position_list, queue_size=10)
    msg = position_list()
    msg.x = [round(float(enviroment.coords(robot_obj)[0]),2)]
    msg.y = [round(float(enviroment.coords(robot_obj)[1]),2)]
    msg.vel = [speed]
    pub.publish(msg)
    rospy.loginfo("Robot current position X: %s Y: %s -- Robot velocity: %s", msg.x, msg.y, msg.vel)

##Here is the robot node, note that this node works as a subscriber and a publisher at same time
def robot():
    rospy.init_node('robot', anonymous=True)
    rospy.loginfo("Robot intial Position: %s", enviroment.coords(robot_obj)[:2])
    sub = rospy.Subscriber("position", position_list, move)
    pub = rospy.Publisher("robot_status", position_list, queue_size=10)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()
        main.mainloop()

if __name__ == '__main__':
    try:
        robot()
    except rospy.ROSInitException:
        pass
