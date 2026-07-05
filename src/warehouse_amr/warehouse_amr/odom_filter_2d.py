#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry

from tf_transformations import euler_from_quaternion
from tf_transformations import quaternion_from_euler


class OdomFilter2D(Node):

    def __init__(self):
        super().__init__('odom_filter_2d')

        self.sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.pub = self.create_publisher(
            Odometry,
            '/odom_filtered',
            10
        )

        self.get_logger().info("2D Odom Filter Started")

    def odom_callback(self, msg):

        new_msg = Odometry()

        # keep header
        new_msg.header = msg.header
        new_msg.child_frame_id = msg.child_frame_id

        # ------------------------
        # POSITION
        # ------------------------

        new_msg.pose.pose.position.x = msg.pose.pose.position.x
        new_msg.pose.pose.position.y = msg.pose.pose.position.y
        new_msg.pose.pose.position.z = 0.0

        # ------------------------
        # ORIENTATION → keep yaw only
        # ------------------------

        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w

        roll, pitch, yaw = euler_from_quaternion(
            [qx, qy, qz, qw]
        )

        q = quaternion_from_euler(0.0, 0.0, yaw)

        new_msg.pose.pose.orientation.x = q[0]
        new_msg.pose.pose.orientation.y = q[1]
        new_msg.pose.pose.orientation.z = q[2]
        new_msg.pose.pose.orientation.w = q[3]

        # ------------------------
        # LINEAR VELOCITY
        # ------------------------

        new_msg.twist.twist.linear.x = msg.twist.twist.linear.x
        new_msg.twist.twist.linear.y = 0.0
        new_msg.twist.twist.linear.z = 0.0

        # ------------------------
        # ANGULAR VELOCITY
        # ------------------------

        new_msg.twist.twist.angular.x = 0.0
        new_msg.twist.twist.angular.y = 0.0
        new_msg.twist.twist.angular.z = msg.twist.twist.angular.z

        self.pub.publish(new_msg)


def main(args=None):

    rclpy.init(args=args)

    node = OdomFilter2D()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
