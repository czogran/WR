from ev3dev.ev3 import *
from time import sleep


touch_sensor = TouchSensor('in4')
light_left = ColorSensor('in2')
light_right = ColorSensor('in1')


right_engine = LargeMotor('outB')
left_engine = LargeMotor('outA')


while not touch_sensor.is_pressed:
    continue

sleep(0.5)
angle_forward=100
angle_turn=100
sleep_time=1

#obrot- wykryl lewym czujnikiem, ktory znajduje sie z prawej strony
right_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
left_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")

#obrot przez pierwszy fragment czarnej
right_engine.run_to_rel_pos(position_sp=-angle_turn, speed_sp=300, stop_action="coast")
left_engine.run_to_rel_pos(position_sp=angle_turn, speed_sp=300, stop_action="coast")
sleep(sleep_time)
#obrac sie az naptka czarna
while True:
    right_engine.run_forever(speed_sp = -100, stop_action = "coast")
    left_engine.run_forever(speed_sp=100,stop_action="coast")
    sleep(0.1)
    #obraca sie az napotka czarna linie
    if light_right.reflected_light_intesity>100:
        left_engine.stop(stop_action="coast")
        right_engine.stop(stop_action="coast")
        break