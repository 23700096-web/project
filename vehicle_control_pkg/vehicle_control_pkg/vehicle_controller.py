import time
import serial

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class VehicleController(Node):

    def __init__(self):
        super().__init__('vehicle_controller')

        # Serial 설정
        self.serial_port = None

        try:
            self.serial_port = serial.Serial(
                port='/dev/ttyACM0',
                baudrate=115200,
                timeout=1
            )

            time.sleep(2)

            self.get_logger().info("Arduino Connected.")

        except Exception:

            self.get_logger().warn(
                "Arduino not connected. Running in Simulation Mode."
            )

        # ROS2 Subscriber
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.get_logger().info("Vehicle Controller Started.")


    # cmd_vel Callback
    def cmd_callback(self, msg):

        linear = msg.linear.x
        angular = msg.angular.z

        command = f"{linear:.2f},{angular:.2f}\n"

        # ROS 로그 출력
        self.get_logger().info(
            f"Linear={linear:.2f} m/s | Angular={angular:.2f} rad/s"
        )

        # Arduino 연결 시
        if self.serial_port:

            self.serial_port.write(command.encode())

            self.get_logger().info(
                f"[SERIAL] {command.strip()}"
            )

        # Arduino 없으면 Simulation
        else:

            self.get_logger().info(
                f"[SIMULATION] {command.strip()}"
            )


def main(args=None):

    rclpy.init(args=args)

    node = VehicleController()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    finally:

        if node.serial_port:

            node.serial_port.close()

        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":
    main()