import sys  # noqa: F401
from dataclasses import dataclass
import draccus

from lerobot.robots import (  # noqa: F401
    RobotConfig,
    make_robot_from_config,
    so_follower,
)
from lerobot.teleoperators import (  # noqa: F401
    TeleoperatorConfig,
    make_teleoperator_from_config,
    so_leader,
)


@dataclass
class CheckConfig:
    teleop: TeleoperatorConfig | None = None
    robot: RobotConfig | None = None

    def __post_init__(self):
        if bool(self.teleop) == bool(self.robot):
            raise ValueError("Choose exactly one: either a teleop or a robot.")

        self.device = self.robot if self.robot else self.teleop


@draccus.wrap()
def check_motors(cfg: CheckConfig):
    print(f"Connecting to {cfg.device.type}...")

    if isinstance(cfg.device, RobotConfig):
        device = make_robot_from_config(cfg.device)
    else:
        device = make_teleoperator_from_config(cfg.device)

    try:
        # connect to motorbus
        device.connect()
        print("\n SUCCESS: All configured motors were found \
              on the physical hardware bus!")
    except Exception as e:
        print("\n HARDWARE MISMATCH ERROR:")
        print(e)
        print("\nThe actual IDs on your hardware do not match the \
            expected configuration.")
        return

    # Print the motor ID - joint name relationships dynamically
    print(f"\n--- Motor Setup for: {cfg.device.type} ---")
    for joint_name, motor_obj in device.bus.motors.items():
        print(f"Motor ID: {motor_obj.id:<3} | Joint Name: {joint_name}")

    device.disconnect()


def main():
    check_motors()


if __name__ == "__main__":
    # --- DEBUG MODE ---
    # sys.argv = [
    #     "check_motors.py",
    #     "--teleop.type", "so101_leader",
    #     "--teleop.port", "/dev/ttyACM1",
    #     "--teleop.id", "my_leader"
    # ]

    # run script: python own_scripts/check_motors.py --teleop.type so101_leader --teleop.port /dev/ttyACM1 --teleop.id my_leader  # noqa: E501

    main()
