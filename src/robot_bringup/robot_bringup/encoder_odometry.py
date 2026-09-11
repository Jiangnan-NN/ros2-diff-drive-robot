import math

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int64MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class EncoderOdometry(Node):

    def __init__(self):
        super().__init__('encoder_odometry')

        # Real values will be filled in when the physical robot is available
        self.declare_parameter('wheel_radius', 0.0)
        self.declare_parameter('wheel_separation', 0.0)
        self.declare_parameter('encoder_cpr', 0)

        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.wheel_separation = self.get_parameter('wheel_separation').value
        self.encoder_cpr = self.get_parameter('encoder_cpr').value

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.prev_left = None
        self.prev_right = None
        self.prev_time = None

        self.create_subscription(
            Int64MultiArray,
            '/encoder_ticks',
            self.encoder_callback,
            10
        )

        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10
        )

        self.tf_broadcaster = TransformBroadcaster(self)

        self.get_logger().info('Encoder odometry node started')


    def encoder_callback(self, msg):
        if len(msg.data) < 2:
            return

        left_ticks = msg.data[0]
        right_ticks = msg.data[1]
        now = self.get_clock().now()

        if self.prev_left is None:
            self.prev_left = left_ticks
            self.prev_right = right_ticks
            self.prev_time = now
            return

        dt = (now - self.prev_time).nanoseconds / 1e9

        if (
            dt <= 0.0 or
            self.encoder_cpr <= 0 or
            self.wheel_radius <= 0.0 or
            self.wheel_separation <= 0.0
        ):
            return

        delta_left_ticks = left_ticks - self.prev_left
        delta_right_ticks = right_ticks - self.prev_right

        meters_per_tick = (
            2.0 * math.pi * self.wheel_radius / self.encoder_cpr
        )

        delta_left = delta_left_ticks * meters_per_tick
        delta_right = delta_right_ticks * meters_per_tick

        delta_s = (delta_left + delta_right) / 2.0
        delta_theta = (
            delta_right - delta_left
        ) / self.wheel_separation

        self.x += delta_s * math.cos(
            self.theta + delta_theta / 2.0
        )

        self.y += delta_s * math.sin(
            self.theta + delta_theta / 2.0
        )

        self.theta += delta_theta

        linear_velocity = delta_s / dt
        angular_velocity = delta_theta / dt

        qz = math.sin(self.theta / 2.0)
        qw = math.cos(self.theta / 2.0)

        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        odom.twist.twist.linear.x = linear_velocity
        odom.twist.twist.angular.z = angular_velocity

        self.odom_pub.publish(odom)

        transform = TransformStamped()
        transform.header.stamp = now.to_msg()
        transform.header.frame_id = 'odom'
        transform.child_frame_id = 'base_footprint'

        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.rotation.z = qz
        transform.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(transform)

        self.prev_left = left_ticks
        self.prev_right = right_ticks
        self.prev_time = now


def main(args=None):
    rclpy.init(args=args)
    node = EncoderOdometry()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
