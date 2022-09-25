#! /usr/bin/env python3
# -*- coding:utf-8 -*-

from dis import dis
import rospy
import tf
from math import *
import PyKDL
import numpy as np

from geometry_msgs.msg import Twist, Vector3, Point, Quaternion
from sensor_msgs.msg import LaserScan


class Indeciso():
	def __init__(self):
		rospy.init_node("roda_exemplo")
		self.cmd_vel = rospy.Publisher("cmd_vel", Twist, queue_size=3)
		self.distancia = None
		self.rate = rospy.get_param("~rate", 10)
		goal_distance = rospy.get_param("~goal_distance", 0.1) # Distância em metros
		r = rospy.Rate(self.rate) 
		self.base_frame = rospy.get_param("~base_frame", "/base_footprint") # Frame de referência
		self.odom_frame = rospy.get_param("~odom_frame", "/odom") # Frame de referência

		self.tf_listener = tf.TransformListener()
		self.odom_frame = "/odom"
		self.tf_listener.waitForTransform(self.odom_frame, '/base_footprint', rospy.Time(), rospy.Duration(1.0))
		self.base_frame = '/base_footprint'

		while not rospy.is_shutdown():
			rospy.wait_for_message("/scan", LaserScan)
			self.recebe_scan = rospy.Subscriber("/scan", LaserScan, self.scaneou)
			position = Point()
			x_start = position.x
			y_start = position.y
			if self.distancia is not None and self.distancia <= 0.95:
				distance = 0
				move_cmd  = Twist()
				move_cmd.linear.x = -0.5
				self.cmd_vel.publish(move_cmd)
				r.sleep()

			if self.distancia is not None and self.distancia > 0.95 and self.distancia < 2:
				position = Point()
				move_cmd  = Twist()
				move_cmd.linear.x = -0.5
				(position, _) = self.get_odom()
				x_start = position.x
				y_start = position.y
				distance = 0
				while distance < goal_distance and not rospy.is_shutdown():
						self.cmd_vel.publish(move_cmd)
						r.sleep()

						(position, _) = self.get_odom()
						distance = sqrt(pow((position.x - x_start), 2) + pow((position.y - y_start), 2))


		

			if self.distancia is not None and self.distancia > 0.95:
				while self.distancia > 0.95:
					move_cmd  = Twist()
					move_cmd.linear.x = 1
					self.cmd_vel.publish(move_cmd)
					r.sleep()




	def scaneou(self, dado):
		# print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
		# print("Leituras:")
		distancia = np.array(dado.ranges[0]).round(decimals=2)
		print(distancia)
		self.distancia = distancia

	def get_odom(self):
			try:
					(transform, rot) = self.tf_listener.lookupTransform(self.odom_frame, self.base_frame, rospy.Time(0))
			except (tf.Exception, tf.ConnectivityException, tf.LookupException):
					rospy.loginfo("TF Exception")
					return 

			return (Point(*transform), quat_to_angle(Quaternion(*rot)))


def quat_to_angle(quat):
    rot = PyKDL.Rotation.Quaternion(quat.x, quat.y, quat.z, quat.w)
    return rot.GetRPY()[2]

if __name__ == '__main__':
    try:
        Indeciso()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Object tracking node terminated.")

