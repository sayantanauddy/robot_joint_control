#!/usr/bin/env python

###############################################################################
# File: darwin_walk_demo.py
# Description: Executes walk_limit number of walks for the Darwin OP in gazebo
#              and records the distance travelled and average height for each
#              walk. The walking algorithm is the default one provided.
# Execution: rosrun robot_walking darwin_walk_demo.py
###############################################################################

import rospy
import math
# Import messages
from gazebo_msgs.msg import ModelStates
from gazebo_msgs.msg import ModelState
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Pose, Twist
# Import services
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.srv import SetModelState

# Import models
from darwin_gazebo.darwin import Darwin


class Darwin_Walk_Demo():

    
    def __init__(self):
    
        self.model_name = 'darwin'
        self.relative_entity_name = 'world'
        
        # List to store the average model z coordinate
        self.model_avg_z_list = []
        
        # List to store the total distance covered during the walk
        self.model_distance_list = []
        
        # List to store the polled z coordinates during a walk
        self.model_polled_z = []
        
        rospy.init_node('darwin_walk_demo', anonymous=False)
        #rospy.rate(100)
        
        # Subscribe to the /gazebo/model_states topic
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.subscriber_callback_modelstate)
        
        # Register the client for service gazebo/get_model_state
        rospy.wait_for_service('/gazebo/get_model_state')
        self.get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

        # Register the client for service gazebo/set_model_state
        rospy.wait_for_service('/gazebo/set_model_state')
        self.set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        
        self.start_run()
        
        
    def subscriber_callback_modelstate(self, dummymodelstate):
        try:
            modelstate = self.get_model_state(self.model_name,self.relative_entity_name)
            
            # Retrieve model x,y and z coordinates
            self.current_model_x = modelstate.pose.position.x
            self.current_model_y = modelstate.pose.position.y
            self.current_model_z = modelstate.pose.position.z
            
            # Store the current z coordinate in the list
            self.model_polled_z.append(self.current_model_z)
              
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        
    def start_run(self):
        # How many times to walk
        walk_limit = 3;
        walk_counter = 0;
        # How many seconds to walk each time
        walk_time = 10;
        
        self.reset_simulation()
        
        # For each walk
        while(walk_counter < walk_limit):
            
            rospy.loginfo("Starting walk number " + str(walk_counter))
            # Walk for 20 seconds
            self.initiate_walk(walk_time, [1,0,0])
            
            rospy.loginfo("Starting evaluation for walk number " + str(walk_counter))
            # Perform evaluation using the logged data for the walk
            self.evaluate_walk()
            
            rospy.loginfo("Resetting simulation")
            self.reset_simulation()
            
            walk_counter = walk_counter + 1
        
        rospy.loginfo("Printing results")
        
        # Print results
        self.report()
        
        
    def initiate_walk(self, walk_seconds,walk_velocity):
        darwin = Darwin()
        darwin.set_walk_velocity(walk_velocity[0],walk_velocity[1],walk_velocity[2])
        rospy.sleep(walk_seconds)
        darwin.set_walk_velocity(0,0,0)
        
    
    def evaluate_walk(self):
    
        # Evaluate the average of self.model_polled_z
        average_z = sum(self.model_polled_z) / float(len(self.model_polled_z))
        
        # Append this value to the self.model_avg_z_list
        self.model_avg_z_list.append(average_z)
        
        # Calculate the distance travelled by the robot
        distance = math.sqrt((self.current_model_x)*(self.current_model_x) + (self.current_model_y)*(self.current_model_y))
        
        # Append the distance to the list self.model_distance_list
        self.model_distance_list.append(distance)
    
    def reset_simulation(self):
        # Empty the self.model_polled_z list
        self.model_polled_z = []
        
        # Send model to x=0,y=0
        model_name = 'darwin'
        pose = Pose()
        pose.position.z = 0.31
        twist = Twist()
        reference_frame = 'world'
        
        md_state = ModelState()
        md_state.model_name = model_name
        md_state.pose = pose
        md_state.twist = twist
        md_state.reference_frame = reference_frame

        # Service call to reset model
        try:
            response = self.set_model_state(md_state)             
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
            
        rospy.loginfo("Result of model reset: " + str(response))
        
        # Reset the joints - Not implemented for now
        
    def report(self):
        rospy.loginfo("Average height:")
        rospy.loginfo(self.model_avg_z_list)
        rospy.loginfo("Distance travelled:")
        rospy.loginfo(self.model_distance_list)
        
if __name__ == '__main__':
    try:
        Darwin_Walk_Demo()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")
        
        
