from ev3dev.ev3 import *
from time import sleep

med = MediumMotor('out3')

med.run_to_rel_pos(position_sp = 100, speed_sp = 50, stop_action = "coast")
