#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
from geometry_msgs.msg import Twist, Vector3, Point, Quaternion
import tf
import PyKDL
from math import *

v = 0.3  # Velocidade linear
w = 0.5  # Velocidade angular]
w_slow = 0.2

class Quadrado():
    def __init__(self):
        rospy.init_node("roda_exemplo", anonymous=False)
     
        r = rospy.Rate(50)
        self.cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size=3)
        rospy.on_shutdown(self.shutdown)
      
        r = rospy.Rate(50)
        goal_distance = rospy.get_param("~goal_distance", 1) # Distância em metros
        goal_angle = rospy.get_param("~goal_angle", radians(90)) # Angulo em radianos
        angular_max_tolerance = rospy.get_param("~angular_max_tolerance", radians(0.1)) # Tolerância em radianos
        linear_speed = rospy.get_param("~linear_speed", v)
        angular_speed = rospy.get_param("~angular_speed", w_slow)
        angular_speed_fast = rospy.get_param("~angular_speed_fast", w)
        self.base_frame = rospy.get_param("~base_frame", "/base_footprint") # Frame de referência
        self.odom_frame = rospy.get_param("~odom_frame", "/odom") # Frame de referência

        self.tf_listener = tf.TransformListener()
        self.odom_frame = "/odom"
        self.tf_listener.waitForTransform(self.odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(1.0))
        self.base_frame = '/base_footprint'


        position = Point()

        # Desenha o quadrado
        for i in range(4):
            move_cmd  = Twist()
            move_cmd.linear.x = linear_speed

            # Posição inicial 
            (position, rotation) = self.get_odom()
            x_start = position.x
            y_start = position.y

            distance = 0
            while distance < goal_distance and not rospy.is_shutdown():
                self.cmd_vel.publish(move_cmd)
                r.sleep()

                (position, rotation) = self.get_odom()
                distance = sqrt(pow((position.x - x_start), 2) + pow((position.y - y_start), 2))

            move_cmd = Twist()
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1.0)

            # Inicia a rotação 
            move_cmd.angular.z = angular_speed_fast
            last_angle = rotation
            turned_angle = 0
            slowSpeed = False
            while abs(turned_angle + angular_max_tolerance) < abs(goal_angle) and not rospy.is_shutdown():
                
                if degrees(goal_angle) - (degrees(turned_angle) + degrees(angular_max_tolerance)) < 40 and not slowSpeed:
                    move_cmd.angular.z = angular_speed
                    slowSpeed = True
                self.cmd_vel.publish(move_cmd)
                r.sleep()
                (position, rotation) = self.get_odom()
                delta_angle = normalize_angle(rotation - last_angle)
                print("DELTA ANGLE: ", delta_angle)
                turned_angle += delta_angle
                print(degrees(turned_angle))
                last_angle = rotation

            move_cmd = Twist()
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1.0)
        
        self.cmd_vel.publish(Twist())


    def get_odom(self):
        try:
            (transform, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
        except (tf.Exception, tf.ConnectivityException, tf.LookupException):
            rospy.loginfo("TF Exception")
            return 

        return (Point(*transform), quat_to_angle(Quaternion(*rot)))
    
    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

def quat_to_angle(quat):
    rot = PyKDL.Rotation.Quaternion(quat.x, quat.y, quat.z, quat.w)
    return rot.GetRPY()[2]



def normalize_angle(angle):
    res = angle
    while res > pi:
        res -= 2.0 * pi
    while res < -pi:
        res += 2.0 * pi
    return res

if __name__ == "__main__":
    try:
        Quadrado()
    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")
