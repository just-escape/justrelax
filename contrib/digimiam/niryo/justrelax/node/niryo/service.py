# -*- coding: utf-8 -*-

import rospy

from niryo_one_python_api.niryo_one_api import NiryoOne, TOOL_GRIPPER_1_ID

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService


class Niryo(JustSockClientService):
    def start(self):
        rospy.init_node('justrelax')
        self.niryo = NiryoOne()
        self.niryo.change_tool(TOOL_GRIPPER_1_ID)

    def get_joints_from_position_name(self, name):
        positions = self.niryo.get_saved_position_list()
        for position in positions:
            if position.name == name:
                return position.joints

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))
        if type(event) is not dict:
            logger.debug("Unknown event: skipping")
            return

        if "action" not in event:
            logger.debug("Event has no action: skipping")
            return

        if event["action"] == "calibrate":
            auto = event.get("auto", False)
            if auto:
                logger.info("Start an auto calibration")
                self.niryo.calibrate_auto()
            else:
                logger.info("Start a manual calibration")
                self.niryo.calibrate_manual()
            logger.info("Calibration finished")

        elif event["action"] == "configure":
            if "learning_mode" in event:
                if event["learning_mode"]:
                    logger.info("Activate learning mode")
                    self.niryo.activate_learning_mode(True)
                else:
                    logger.info("Deactivate learning mode")
                    self.niryo.activate_learning_mode(False)
            if "velocity" in event:
                velocity = int(event["velocity"])
                assert 1 <= velocity <= 100, "Speed must be between 1 and 100"
                logger.info("Set velocity to {}".format(velocity))
                self.niryo.set_arm_max_velocity(velocity)

        elif event["action"] == "move_position":
            position_name = str(event.get("position", ""))
            joints = self.get_joints_from_position_name(position_name)
            self.niryo.move_joints(joints)

        elif event["action"] == "move_joint":
            joint = int(event.get("joint", 0))
            assert 0 <= joint <= 5, "Joint must be between 0 and 5"
            position_name = str(event.get("position", ""))

            position_joints = self.get_joints_from_position_name(position_name)
            joints = self.niryo.joints[:]

            joints[joint] = position_joints[joint]

            self.niryo.move_joints(joints)

        elif event["action"] == "open_gripper":
            self.niryo.open_gripper(TOOL_GRIPPER_1_ID, 350)

        elif event["action"] == "close_gripper":
            self.niryo.close_gripper(TOOL_GRIPPER_1_ID, 350)

        else:
            logger.debug("Unknown action type '{}': skipping".format(event["action"]))
