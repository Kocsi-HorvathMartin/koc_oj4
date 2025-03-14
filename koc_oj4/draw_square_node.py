import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class CmdGen(Node):

    def __init__(self):
        super().__init__('draw_square_node')
        
        # 10Hz-es loop létrehozása
        self.timer = self.create_timer(0.1, self.loop)
        
        # Publisher létrehozása a turtle1/cmd_vel topic Twist üzenetére
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Feliratkozás a turtle1/pose topicra
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # Pose init
        self.pose = Pose()
        
        # Loop control variables
        self.loop_count = 0
        self.is_turning = False
        self.turn_start_angle = None  # Fordulás kezdetekor a szög eltárolása
        self.get_logger().info("draw_square_node has been started")

    # turtle1 jelenlegi pozíció adatainak frissítése
    def pose_callback(self, msg):
        self.pose = msg

    def loop(self):
        cmd_msg = Twist()
        
        # Mozgás előre 3 másodpercig
        if self.loop_count < 30:
            cmd_msg.linear.x = 1.0
            cmd_msg.angular.z = 0.0

        # Fordulás
        elif self.loop_count >= 20 and not self.is_turning:
            self.is_turning = True
            self.turn_start_angle = self.pose.theta
            cmd_msg.linear.x = 0.0
            cmd_msg.angular.z = 1.0

        # Fordulás, amíg 90 fokot nem fordult
        elif self.is_turning:
            if abs(self.pose.theta - self.turn_start_angle) >= math.pi/2:
                self.is_turning = False
                self.loop_count = 0 
            else:
                cmd_msg.linear.x = 0.0
                cmd_msg.angular.z = 1.0

        self.cmd_pub.publish(cmd_msg)
        self.loop_count += 1
    
def main(args=None):
    rclpy.init(args=args)
    cmd_gen = CmdGen()
    rclpy.spin(cmd_gen)
    cmd_gen.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()