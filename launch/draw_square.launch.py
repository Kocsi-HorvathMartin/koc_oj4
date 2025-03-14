from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
                package='koc_oj4',
                executable='draw_square_node',
            ),
            Node(
                package='turtlesim',
                executable='turtlesim_node',
            ),
    ])