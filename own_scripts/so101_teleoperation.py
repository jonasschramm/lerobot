from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.teleoperators.so_leader import SO101LeaderConfig, SO101Leader
from lerobot.robots.so_follower import SO101FollowerConfig, SO101Follower

camera_config = {
    "gripper": OpenCVCameraConfig(index_or_path=0,
                                  width=640,
                                  height=480,
                                  fps=30.0)
}

robot_config = SO101FollowerConfig(
    port="/dev/ttyACM0",
    id="my_follower",
    cameras=camera_config,
)

teleop_config = SO101LeaderConfig(
    port="/dev/ttyACM1",
    id="my_leader",
)

robot = SO101Follower(robot_config)
teleoperator = SO101Leader(teleop_config)
robot.connect()
teleoperator.connect()

while True:
    observation = robot.get_observation()
    action = teleoperator.get_action()
    robot.send_action(action)
