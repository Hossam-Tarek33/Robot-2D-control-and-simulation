# Robot-2D-control-and-simulation
https://user-images.githubusercontent.com/68400719/148757766-b15d4632-2a73-420d-86ea-f418a693982d.mp4
## Overview
<p align="center">
    <img src="https://user-images.githubusercontent.com/68400719/148756248-94311fa8-1d31-414e-b85a-387a8166607b.png"/>
</p>
This repo contains a ROS package that simulates the control of a robot in a 2D-environment
The package contains a publisher-node "Controller" and other node that works as a publisher and a subscriber at the same time "Robot".
The controller node recieves the target position(s) as well the desired velocity(ies) from the used and publish them to the robot node. The robot node on the other side subscribes the data from the controller and publishes its current state simultaneously. 

## Launch the package
```
roslaunch robot_zal launch.launch
```
