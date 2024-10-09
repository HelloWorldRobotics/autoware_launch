from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch.substitutions import FindExecutable

def generate_launch_description():
    return LaunchDescription([
        # Add a 3-second delay
        TimerAction(
            period=3.0,
            actions=[
                ExecuteProcess(
                    cmd=[
                        FindExecutable(name='ros2'),
                        'run',
                        'system_monitor',
                        'traffic_reader'
                    ],
                    output='screen'
                )
            ]
        )
    ])
