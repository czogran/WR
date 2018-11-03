from ev3dev.ev3 import *
from time import sleep

light_left = ColorSensor('in2')
light_right = ColorSensor('in1')
touch_sensor = TouchSensor('in4')
lcd = Screen()

right_engine = LargeMotor('outB')
left_engine = LargeMotor('outA')

white_left = 0
white_right = 0
black_left = 0
black_right = 0

green_left=0
green_right=0
blue_left=0
blue_right=0
red_left=0
red_right=0

red_left_travel=0
red_right_travel=0
blue_left_travel=0
blue_right_travel=0
green_left_travel=0
green_right_travel=0

diff=40


lcd.clear()
while not touch_sensor.is_pressed:
    black_left = light_left.reflected_light_intensity
    black_right = light_right.reflected_light_intensity
print("black left:"+str(black_left)+"\n"+"black right:"+str(black_right))
lcd.draw.text((48,13),"black left:"+str(black_left)+"\n"+"black right:"+str(black_right))
lcd.update()
while touch_sensor.is_pressed:
    continue
lcd.clear()
while not touch_sensor.is_pressed:
    white_left = light_left.reflected_light_intensity
    white_right = light_right.reflected_light_intensity
print("white left:"+str(white_left)+"\nwhite right:"+str(white_right))
lcd.draw.text((48,13),"white left:"+str(white_left)+"\nwhite right:"+str(white_right))
lcd.update()
while touch_sensor.is_pressed:
    continue
lcd.clear()
#lcd.draw.text((48,13),"wcisnij przycisk aby wystartowac")
lcd.update()
#wcczytanie czerwonego
while not touch_sensor.is_pressed:
    red_left=light_left.red
    red_right=light_right.red
    blue_left=light_left.blue
    blue_right=light_right.blue
    green_left=light_left.green
    green_right=light_right.green

print("lewy")
print("lewy red:"+(str)(red_left)+" green "+(str)(red_green)+" blue "+(str)(red_blue))
while touch_sensor.is_pressed:
    continue
while touch_sensor.is_pressed:
    continue
while not touch_sensor.is_pressed:
    continue
while touch_sensor.is_pressed:
    continue
lcd.clear()
#lcd.draw.text((48,13),"wcisnij przycisk aby wystartowac")
lcd.update()
lcd.draw.text((48,13),"wcisnij przycisk aby zakonczyc dzialanie programu")
lcd.update()


Kp = 5.0
Kd = 2.0
predkosc_bazowa = 100.0
srodek_l = (white_left + black_left) // 2
srodek_r = (white_right + black_right) // 2
blad = 0
poprzedni_blad = 0
blad_l = 0
blad_r = 0
blad_prop = 0.0
blad_deri = 0.0

while not touch_sensor.is_pressed:
    blad_l = light_left.reflected_light_intensity - srodek_l
    blad_r = light_right.reflected_light_intensity - srodek_r
    blad = blad_l - blad_r
    blad_prop = Kp * float(blad)
    blad_deri = Kd * (blad - poprzedni_blad)
    #left_engine.run_timed(time_sp = 20, speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
    #right_engine.run_timed(time_sp = 20, speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")

    left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
    right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")

    poprzedni_blad = blad
    sleep(0.1)
    red_left_travel=light_left.red
    red_right_travel=light_right.red
    blue_left_travel=light_left.blue
    blue_right_travel=light_right.blue
    green_left_travel=light_left.green
    green_right_travel=light_right.green
    #wykrywanie czy najechal na czerwona
    if (red_left_travel<red_left+diff and red_left_travel>(red_left-diff)):
       if( green_left_travel< green_left-diff and green_left_travel> green_left-diff):
           if(blue_left_travel< blue_left+diff and blue_left_travel> blue_left-diff):
               break
    if (red_right_travel<red_right+diff and red_right_travel>(red_right-diff)):
       if( green_right_travel< green_right-diff and green_right_travel> green_right-diff):
           if(blue_right_travel< blue_right+diff and blue_right_travel> blue_right-diff):
               break
    

lcd.clear()
print("to jest juz koniec")
lcd.draw.text((48,13),"koniec dzialania programu")
lcd.update()
left_engine.stop(stop_action="coast")
right_engine.stop(stop_action="coast")
