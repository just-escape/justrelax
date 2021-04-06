# -*- coding: utf-8 -*-

import argparse
import json
import time

import logging
import logging.config
import logging.handlers

import yaml
import websocket

import rospy

from niryo_one_python_api.niryo_one_api import NiryoOne, TOOL_ELECTROMAGNET_1_ID, GPIO_1A


logger = logging.getLogger('justrelax')


def init_logging(level='INFO', file='/dev/null'):
    logger.setLevel(level)

    line_formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(line_formatter)
    logger.addHandler(stream_handler)

    rotating_file_handler = logging.handlers.RotatingFileHandler(file, maxBytes=10485760, backupCount=10)
    rotating_file_handler.setFormatter(line_formatter)
    logger.addHandler(rotating_file_handler)


class Niryo(object):
    def __init__(self, host, port, config=None):
        self.host = host
        self.port = port
        self.config = config if config is not None else {}

        raw_positions = self.config.get('positions', {})
        self.positions = {
            p_name: [float(j.strip()) for j in p_joints.split(',')] for p_name, p_joints in raw_positions.items()
        }

        self.magnetized = False

        self.niryo = None

    def on_message(self, ws, message):
        logger.info(message)

        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            logger.warning("Cannot load {}: ignoring".format(message))
            return

        # message could be validated here with something like pydantic

        try:
            logger.info("{} <<< {}".format(message['channel'], message['event']))

            self.process_event(message['event'])
        except Exception:
            logger.error("Error while trying to process message={}".format(message), exc_info=True)

    def process_event(self, event):
        if 'category' not in event:
            logger.error("Event has no category: skipping")
            return

        if event['category'] == 'calibrate':
            self.calibrate()
        elif event['category'] == 'magnetize':
            self.magnetize()
        elif event['category'] == 'toggle_magnetize':
            if self.magnetized:
                self.demagnetize()
            else:
                self.magnetize()
        elif event['category'] == 'demagnetize':
            self.demagnetize()
        elif event['category'] == 'learning_mode':
            activate = event.get('activate', True)
            self.learning_mode(activate)
        elif event['category'] == 'move_position':
            position = event.get('position', None)
            self.move_position(position)
        elif event['category'] == 'log_joints':
            self.log_joints()
        else:
            logger.warning("Unknown category {}: ignoring".format(event['category']))

    def calibrate(self):
        logger.info("Calibrating")
        rospy.init_node('justrelax')
        self.niryo = NiryoOne()
        self.niryo.calibrate_auto()
        logger.info("Calibration finished")
        logger.info("Equipping electromagnet")
        self.niryo.change_tool(TOOL_ELECTROMAGNET_1_ID)
        self.niryo.setup_electromagnet(TOOL_ELECTROMAGNET_1_ID, GPIO_1A)

    def magnetize(self):
        self.niryo.activate_electromagnet(TOOL_ELECTROMAGNET_1_ID, GPIO_1A)
        self.magnetized = True

    def demagnetize(self):
        self.niryo.deactivate_electromagnet(TOOL_ELECTROMAGNET_1_ID, GPIO_1A)
        self.magnetized = False

    def learning_mode(self, activate):
        self.niryo.activate_learning_mode(activate)

    def move_position(self, position):
        joints = self.positions.get(position, None)
        if joints is None:
            logger.error("Unknown position {}: skipping".format(position))
            return
        self.niryo.move_joints(joints)

    def log_joints(self):
        logger.info("Joints: {}".format(self.niryo.get_joints()))

    def on_error(self, ws, error):
        logger.error(error)

    def on_close(self, ws):
        logger.info("Connection lost: trying to reconnect in 10 seconds")
        time.sleep(10)
        self.run_forever()

    def on_open(self, ws):
        logger.info("Connection opened")

        for subscription in self.config.get('subscriptions', []):
            logger.info("Subscribing to channel {}".format(subscription))
            ws.send(json.dumps({"action": "subscribe", "channel": subscription}))

    def run_forever(self):
        try:
            logger.info("Connecting to broker at {}:{}".format(self.host, self.port))
            ws = websocket.WebSocketApp(
                "ws://{}:{}/".format(self.host, self.port),
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close)

            ws.run_forever()
        except Exception:
            logger.error("Error while trying to connect: retrying in 10 seconds", exc_info=True)
            time.sleep(10)
            self.run_forever()


def run_node():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', help='localhost by default')
    parser.add_argument('-p', '--port', type=int, default=3031, help='3031 by default')
    parser.add_argument('-c', '--config', type=str, help='Path to a config file')
    parser.add_argument('-l', '--log-level', type=str, default='INFO', help='INFO by default')
    parser.add_argument('-f', '--log-file', type=str, default='/dev/null', help='/dev/null by default (no file)')
    args = parser.parse_args()

    init_logging(level=args.log_level, file=args.log_file)

    if args.config:
        with open(args.config, "rt") as f:
            config = yaml.safe_load(f.read())

    kwargs = {'config': config} if args.config else {}
    kwargs['host'] = args.host
    kwargs['port'] = args.port

    logger.info("Initializing node")
    n = Niryo(**kwargs)

    n.run_forever()
