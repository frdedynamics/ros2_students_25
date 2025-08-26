#!/usr/bin/env python3

from adatools import config_generator as cg
from adatools import plotting_tools as pt


my_conf2_robot = cg.get_robot_config_2(link1=0.3, link1_offset=0.0,
                                       link2=0.3, link2_offset=0.0)

# Plot the robot on base plate
robot_plot = my_conf2_robot.plot(my_conf2_robot.q, backend='pyplot')
pt.plot_baseplate(robot_plot)
# robot_plot.hold()

# Jog the robot on base plate
robot_teach = my_conf2_robot.teach(my_conf2_robot.q, backend='pyplot', block=False)
pt.plot_baseplate(robot_teach)
robot_teach.hold()