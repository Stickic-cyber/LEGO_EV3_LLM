#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.media.ev3dev import Font
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import socket, random

# 初始化 EV3
ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)
distance_sensor = UltrasonicSensor(Port.S4)
chinese_font = Font(size=24, lang='zh-cn')
ev3.speaker.set_speech_options(language="zh", voice="f1")
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# 初始化 TCP 监听
HOST = "0.0.0.0"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

ev3.screen.clear()
ev3.screen.set_font(chinese_font)
ev3.screen.print("等待连接...")
ev3.speaker.say("准备好连接")

running = True

while running:
    try:
        # 每次重新等待连接
        conn, addr = server_socket.accept()
        ev3.screen.clear()
        ev3.screen.print("已连接!")

        data = conn.recv(1024)
        if data:
            command = data.decode('utf-8').strip()
            ev3.screen.clear()
            ev3.screen.print(command)

            if command.startswith("前进"):
                robot.straight(200)
                ev3.speaker.say("前进")

            elif command.startswith("后退"):
                robot.straight(-200)
                ev3.speaker.say("后退")

            elif command.startswith("停止"):
                robot.stop()
                ev3.speaker.say("停止")

            elif command.startswith("左转"):
                robot.turn(-90)
                ev3.speaker.say("左转")

            elif command.startswith("右转"):
                robot.turn(90)
                ev3.speaker.say("右转")

            elif command.startswith("自动"):
                ev3.speaker.say("进入自动模式")
                while True:
                    robot.drive(200, 0)
                    while distance_sensor.distance() > 300:
                        wait(10)
                    robot.straight(-300)
                    angle = random.randint(-120, 120)
                    robot.turn(angle)

            elif command.startswith("距离"):
                dist = distance_sensor.distance()
                ev3.screen.print("距离:%scm" % dist)
                ev3.speaker.say("当前距离是%s厘米" % dist)

            elif command.startswith("退出"):
                robot.stop()
                running = False
                ev3.speaker.say("退出程序")

            else:
                ev3.speaker.say("命令未识别")

        conn.close()
        wait(100)

    except Exception as e:
        ev3.screen.print("错误")
        ev3.speaker.say("出错了")
        break

server_socket.close()
ev3.speaker.say("连接关闭")
