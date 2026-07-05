#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


class StaticLidarTF(Node):

    def __init__(self):
        super().__init__('static_lidar_tf')

        self.tf_static_broadcaster = StaticTransformBroadcaster(self)

        self.publish_static_transform()

        self.get_logger().info("Static LiDAR TF published")

    def publish_static_transform(self):

        t = TransformStamped()

        # Static transform timestamp
        t.header.stamp.sec = 0
        t.header.stamp.nanosec = 0

        # Parent and child frames
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'sim_lidar'

        # LiDAR position
        t.transform.translation.x = -0.01655
        t.transform.translation.y = -0.00382
        t.transform.translation.z = 0.30

        # Yaw = -7 degrees
        yaw = math.radians(-7)

        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = math.sin(yaw / 2.0)
        t.transform.rotation.w = math.cos(yaw / 2.0)

        # Publish static transform
        self.tf_static_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)

    node = StaticLidarTF()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
