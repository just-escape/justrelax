import rospy

from niryo_one_python_api.niryo_one_api import NiryoOne, TOOL_GRIPPER_1_ID

from justrelax.node.service import JustSockClientService


class Joint(object):
    def __init__(self):
        self._raw_target_position = 0.
        self._raw_current_position = 0.
        self._target_position = 0.
        self._current_position = 0.

    @property
    def raw_target_position(self):
        return self._raw_target_position

    @raw_target_position.setter
    def raw_target_position(self, value):
        self._raw_target_position = value

    @property
    def raw_current_position(self):
        return self._raw_current_position

    @raw_current_position.setter
    def raw_current_position(self, value):
        self._raw_current_position = value

    @property
    def target_position(self):
        return self._target_position

    @target_position.setter
    def target_position(self, value):
        self._target_position = value

    @property
    def current_position(self):
        return self._current_position

    @current_position.setter
    def current_position(self, value):
        self._current_position = value

    def set_position_from_raw_value(self, raw_value):
        self.raw_target_position = raw_value
        self.raw_current_position = raw_value

    def set_target(self, value):
        self.raw_target_position = value

    def get_raw_delta_target(self):
        return min(self.raw_target_position - self.current_position, 0.01)


class JointsController(object):
    JOINT_1 = 0
    JOINT_2 = 1
    JOINT_3 = 2
    JOINT_4 = 3
    JOINT_5 = 4
    JOINT_6 = 5

    def __init__(self, niryo_one_controller):
        self.noc = niryo_one_controller
        self.jcs = {
            JointsController.JOINT_1: Joint(),
            JointsController.JOINT_2: Joint(),
            JointsController.JOINT_3: Joint(),
            JointsController.JOINT_4: Joint(),
            JointsController.JOINT_5: Joint(),
            JointsController.JOINT_6: Joint(),
        }

    def set_positions_from_raw_values(self, raw_values):
        # Using enumerate is a shortcut because joint ids have been chosen
        # to match the index of the values provided in the list returned by
        # the NiryoOne.get_joints method.
        for joint_id, raw_value in enumerate(raw_values):
            self.jcs[joint_id].set_position_from_raw_value(raw_value)

    def set_joint_target(self, joint_id, value):
        self.jcs[joint_id].set_target(value)

        joints = [j.raw_current_position() for j in self.jcs.values()]

        delta = self.jcs[joint_id].get_raw_delta_target()
        while delta > 0.01:
            delta = self.jcs[joint_id].get_raw_delta_target()
            joints[joint_id] = delta
            self.noc.move_joints(joints)

        # over time
        # raw_delta_targets = [j.get_raw_delta_target() for j in self.jcs.values()]
        # self.noc.move_joints(raw_delta_targets)


class NiryoOneController(NiryoOne):
    GRIPPER = TOOL_GRIPPER_1_ID
    GRIPPER_SPEED = 500

    def __init__(self):
        NiryoOne.__init__(self)
        self.joc = JointsController(self)

    @property
    def need_calibration(self):
        return bool(self.get_hardware_status().calibration_needed)

    def activate_motors(self):
        self.activate_learning_mode(False)
        raw_values = self.get_joints()
        self.joc.set_positions_from_raw_values(raw_values)

    def deactivate_motors(self):
        self.activate_learning_mode(True)

    def init_gripper(self):
        self.change_tool(self.GRIPPER)

    def open_gripper(self):
        self.instance.open_gripper(self.GRIPPER, self.GRIPPER_SPEED)

    def close_gripper(self):
        self.instance.close_gripper(self.GRIPPER, self.GRIPPER_SPEED)

    def move_joint(self, joint_id, target):
        self.joc.set_joint_target(joint_id, target)


class Niryo(JustSockClientService):
    def __init__(self, name, channel, *args, **kwargs):
        super(Niryo, self).__init__(*args, **kwargs)
        rospy.init_node('{}@{}'.format(name, channel))
        self.noc = NiryoOneController()

        if self.noc.need_calibration:
            self.noc.calibrate_auto()

        if self.noc_need_calibration:
            self.noc.calibrate_manual()

        if self.noc_need_calibration:
            """problem"""

        self.init_gripper()

    def start(self):
        self.noc.activate_motors()

    def process_event(self, event):
        self.factory.send_message(event)
        self.move_joint(JointsController.JOINT_1, )

    def stop(self):
        self.noc.deactivate_motors()
