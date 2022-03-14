# Names:

* Aleksandr Makarov
* Raimo Koidam
* Illimar Laanisto
* Dmytro Fedorenko

# Demo files:
> The folder squid_demo is a ROS package created on the robot. It might be moved to the laptop which is currently considered. The logic of the script is the following: robot turns 180° to humans and searches for motion within 200 frames. If motion is detected a bounding box is created and human is considered to be eliminated and robot turns 180° from humans. Another script is there to work with motion detection without robot and ROS but with a usb camera.

> In order to run demo use ``roslaunch squid_demo demo.launch``

> To run final ```roslaunch squid_demo laser_sound_drone.launch```

# Overview:
When a robot positioned with a back to humans and its' LEDs are green it says "green light" and the humans are allowed to move. The task for humans is to cross the line near a robot. Robot randomly rotates facing humans and says "red light" and its LEDs turn red. Humans aren't allowed to move. Robot then looks for motion with a certain threshold depending on how close the person is(if the person is far away then less motion(in terms of moving pixels) is needed to trigger it). If somebody moves more than a certain threshold a "killer" drone is engaged. It just takes off and flies to the person who moved, stopping at a safe distance(1m) indicating that this person is out. 
Also, for the beginning instead of a killer drone the image from the robot can be displayed on a monitor with an overlay GUI which will show the robot's perspective on how it detects movement + the area near the person who moved becomes red and he leaves the game(also bounding box may be used).

# List of components:
| Item | Link to the item | We will provide | Need from instructors | Total |
| -------------- | -------------- | --------------: | ----------------: | :----------------: |
| Clearbot(robotont) | - | 0 | 1 | 1 |
| DJI tello | - | 1(mine is almost dead) | 1 | 2 |

# Schedule:
https://trello.com/b/vHrJl9qC/squid-game