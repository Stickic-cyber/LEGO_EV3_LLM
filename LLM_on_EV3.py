#!/usr/bin/env pybricks-micropython
"""
EV3 Remote Control Server (English Version)

A TCP server running on the EV3 brick to receive text commands
from a remote client and control the robot accordingly.

Supported Commands:
- forward
- backward
- stop
- left
- right
- auto
- distance
- exit

Author: YourName
Date: 2025-04-20
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.media.ev3dev import Font
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import socket
import random


def initialize_robot():
    """Initialize EV3 hardware and robot configuration."""
    ev3 = EV3Brick()
    left_motor = Motor(Port.B)
    right_motor = Motor(Port.D)
    distance_sensor = UltrasonicSensor(Port.S4)
    robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

    english_font = Font(size=24)
    ev3.screen.set_font(english_font)
    ev3.speaker.set_speech_options(language="en", voice="m1")  # English voice

    return ev3, robot, distance_sensor


def start_tcp_server(host="0.0.0.0", port=12345):
    """Start a TCP server socket and return it."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    return server_socket


def handle_command(command, ev3, robot, distance_sensor):
    """Interpret and execute a received command string."""
    ev3.screen.clear()
    ev3.screen.print(command)

    if command.lower().startswith("forward"):
        robot.straight(200)
        ev3.speaker.say("Moving forward")

    elif command.lower().startswith("backward"):
        robot.straight(-200)
        ev3.speaker.say("Moving backward")

    elif command.lower().startswith("stop"):
        robot.stop()
        ev3.speaker.say("Stopped")

    elif command.lower().startswith("left"):
        robot.turn(-90)
        ev3.speaker.say("Turning left")

    elif command.lower().startswith("right"):
        robot.turn(90)
        ev3.speaker.say("Turning right")

    elif command.lower().startswith("auto"):
        ev3.speaker.say("Entering auto mode")
        while True:
            robot.drive(200, 0)
            while distance_sensor.distance() > 300:
                wait(10)
            robot.straight(-300)
            angle = random.randint(-120, 120)
            robot.turn(angle)

    elif command.lower().startswith("distance"):
        dist = distance_sensor.distance()
        ev3.screen.print(f"Distance: {dist} mm")
        ev3.speaker.say(f"Current distance is {dist} millimeters")

    elif command.lower().startswith("exit"):
        robot.stop()
        ev3.speaker.say("Exiting program")
        return False

    else:
        ev3.speaker.say("Command not recognized")

    return True


def main():
    """Main program loop for the TCP command server."""
    ev3, robot, distance_sensor = initialize_robot()
    server_socket = start_tcp_server()

    ev3.screen.clear()
    ev3.screen.print("Waiting for connection...")
    ev3.speaker.say("Ready for connection")

    running = True

    while running:
        try:
            conn, addr = server_socket.accept()
            ev3.screen.clear()
            ev3.screen.print("Client connected")

            data = conn.recv(1024)
            if data:
                command = data.decode('utf-8').strip()
                running = handle_command(command, ev3, robot, distance_sensor)

            conn.close()
            wait(100)

        except Exception as e:
            ev3.screen.print("Error")
            ev3.speaker.say("An error occurred")
            break

    server_socket.close()
    ev3.speaker.say("Connection closed")


if __name__ == "__main__":
    main()
