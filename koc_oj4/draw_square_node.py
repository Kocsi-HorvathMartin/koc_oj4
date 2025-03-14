import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time

class CmdGen(Node):

    def __init__(self):
        super().__init__('draw_square_node')
        
        # 5Hz-es loop létrehozása
        self.timer = self.create_timer(0.2, self.loop)
        
        # Publisher létrehozása a turtle1/cmd_vel topic Twist üzenetére
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Feliratkozás a turtle1/pose topicra
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # Pose init
        self.pose = Pose()
        
        # Loop control variables
        self.loop_count = 0
        self.get_logger().info("draw_square_node has been started")