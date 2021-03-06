#!/usr/bin/env python

###############################################################################
# File: darwin_plot_joint_angles.py
# Description: Generates plots for the joint angle trajectories
# Execution: rosrun robot_walking darwin_plot_joint_angles.py
###############################################################################

import rospy
import math
import time
import matplotlib.pyplot as plt
import numpy as np
# Import messages
from gazebo_msgs.msg import ModelStates
from gazebo_msgs.msg import ModelState
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Pose, Twist
# Import services
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.srv import SetModelState
from controller_manager_msgs.srv import ListControllers
# Import models
from darwin_gazebo.darwin import Darwin

class Darwin_Plot_Joint_Angles():
    
    def __init__(self):
    
        self.model_name = 'darwin'
        self.relative_entity_name = 'world'
        
        rospy.init_node('darwin_plot_joint_angles', anonymous=False)
        #rospy.rate(100)
        
        # Subscribe to the /darwin/joint_states topic
        rospy.Subscriber("/darwin/joint_states", JointState, self.subscriber_callback_jointstate)
        
        # Register the client for service /darwin/controller_manager/list_controllers
        rospy.wait_for_service('/darwin/controller_manager/list_controllers')
        get_joint_state = rospy.ServiceProxy('/darwin/controller_manager/list_controllers', ListControllers)

        # Service call to get joint states
        try:
             response = get_joint_state()
             controllers = response.controller
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        
        # Initialize map to store joint positions over time
        self.joint_plots = {}
        for controller in controllers:
            # Remove '_position_controller' to obtain joint name
            jointname = controller.name.replace('_position_controller', '')
            self.joint_plots[jointname] = []
          
        print self.joint_plots   
        print self.initiate_walk(20,[1,0,0])
        #self.plot_joints()
        
    def initiate_walk(self, walk_seconds,walk_velocity):
        darwin = Darwin()
        darwin.set_walk_velocity(walk_velocity[0],walk_velocity[1],walk_velocity[2])
        rospy.sleep(walk_seconds)
        darwin.set_walk_velocity(0,0,0)
        
    def subscriber_callback_jointstate(self, jointstate):
        t = time.time()
        for jointname in jointstate.name:
            self.joint_plots[jointname].append((t,jointstate.position[jointstate.name.index(jointname)]))
            
    
    def plot_joints(self):
        
        plt.figure(1)
        
        for jointname in self.joint_plots.keys():
            for tuplelist in self.joint_plots[jointname]:
                x =  np.array([])
                y =  np.array([])
                for atuple in tuplelist:
                    np.append(x,atuple[0])
                    np.append(y,atuple[1])
                    plt.plot(x,y)
                    plt.show()
    
if __name__ == '__main__':

    Darwin_Plot_Joint_Angles()
            
        
    
        
        
        
        
        
        
