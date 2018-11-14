
from ev3dev.ev3 import *
from time import sleep

light_left = ColorSensor('in2')
light_right = ColorSensor('in1')
touch_sensor = TouchSensor('in4')
lcd = Screen()

right_engine = LargeMotor('outB')
left_engine = LargeMotor('outA')
medium=MediumMotor('outC')

white_left = 328
white_right = 377
black_left = 15
black_right = 15

#kolory na czerwonym
green_left=19
green_right=17
blue_left=52
blue_right=48
red_left=275
red_right=220

#kolory na niebieskim
blue_green_left=79
blue_green_right=68
blue_blue_left=230
blue_blue_right=210
blue_red_left=30
blue_red_right=30

lcd.clear()


#czarne
#while not touch_sensor.is_pressed:
 #       black_left = light_left.reflected_light_intensity
 #       black_right = light_right.reflected_light_intensity
#print("black left:"+str(black_left)+"\n"+"black right:"+str(black_right))
#lcd.draw.text((48,13),"black left:"+str(black_left)+"\n"+"black right:"+str(black_right))
#lcd.update()
#while touch_sensor.is_pressed:
# continue

#biale
#lcd.clear()
#while not touch_sensor.is_pressed:
#  white_left = light_left.reflected_light_intensity
#  white_right = light_right.reflected_light_intensity
#print("white left:"+str(white_left)+"\nwhite right:"+str(white_right))
#lcd.draw.text((48,13),"white left:"+str(white_left)+"\nwhite right:"+str(white_right))
#lcd.update()
#while touch_sensor.is_pressed:
#continue



#lcd.clear()
#lcd.update()

#wcczytanie czerwonego
#while not touch_sensor.is_pressed:
 #  red_left=light_left.red
 #  red_right=light_right.red
  # blue_left=light_left.blue
   #blue_right=light_right.blue
  # green_left=light_left.green
  #green_right=light_right.green

#print("czerwony")
#print("lewy red:"+(str)(red_left)+" green "+(str)(red_green)+" blue "+(str)(red_blue))
#while touch_sensor.is_pressed:
#       continue


#wcczytanie niebieskiego
#while not touch_sensor.is_pressed:
 # blue_red_left=light_left.red
 # blue_red_right=light_right.red
  #blue_blue_left=light_left.blue
  #blue_blue_right=light_right.blue
  #blue_green_left=light_left.green
  #blue_green_right=light_right.green

#print("niebieski")
#print("lewy red:"+(str)(red_left)+" green "+(str)(red_green)+" blue "+(str)(red_blue))
#while touch_sensor.is_pressed:
#       continue

#sleep(1)

predkosc_bazowa=150
diff=40
Kp=5
Kd=1
srodek_l = (white_left + black_left) // 2
srodek_r = (white_right + black_right) // 2

#follow line do niebieskiego
while not touch_sensor.is_pressed:
        print("to blue")
        blad_l = light_left.reflected_light_intensity - srodek_l
        blad_r = light_right.reflected_light_intensity - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)
       
        left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
        right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")

        poprzedni_blad = blad
        sleep(0.1)
       

        #wykrywanie czy najechal na niebieska
        if (light_left.red<blue_red_left+diff and light_left.red>(blue_red_left-diff)):
          if(light_left.green< blue_green_left-diff and light_left.green> blue_green_left-diff):
             if(light_left.blue< blue_blue_left+diff and light_left.blue> blue_blue_left-diff):
                   left_engine.stop(stop_action="coast")
                   right_engine.stop(stop_action="coast")
                   break

        if (light_right.red<blue_red_left+diff and light_right.red>(blue_red_left-diff)):
          if(light_right.green< blue_green_left-diff and light_right.green> blue_green_left-diff):
            if(light_right.blue< blue_blue_left+diff and light_right.blue> blue_blue_left-diff):
                   left_engine.stop(stop_action="coast")
                   right_engine.stop(stop_action="coast")
                   break

print("find blue")
print("turn")

#obrot
sleep(2)

angle_forward=80
angle_turn=80
sleep_time=1
speed=100

if (light_left.red<blue_red_left+diff and light_left.red>(blue_red_left-diff)):
      if(light_left.green< blue_green_left-diff and light_left.green> blue_green_left-diff):
         if(light_left.blue< blue_blue_left+diff and light_left.blue> blue_blue_left-diff):
               right_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               print("przed")

               #obrot przez pierwszy fragment czarnej
               right_engine.run_to_rel_pos(position_sp=angle_turn, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=-angle_turn, speed_sp=300, stop_action="coast")
               sleep(sleep_time)

               right_engine.run_forever(speed_sp=speed,stop_action="coast")
               left_engine.run_forever(speed_sp=-speed,stop_action="coast")
               print("po")
               while light_left.reflected_light_intensity >50:
                 contiue
               print("stop")
               left_engine.stop(stop_action="coast")
               right_engine.stop(stop_action="coast")
            

if (light_right.red<blue_red_left+diff and light_right.red>(blue_red_left-diff)):
      if(light_right.green< blue_green_left-diff and light_right.green> blue_green_left-diff):
         if(light_right.blue< blue_blue_left+diff and light_right.blue> blue_blue_left-diff):
               right_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               print("przed")

               #obrot przez pierwszy fragment czarnej
               right_engine.run_to_rel_pos(position_sp=-angle_turn, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=angle_turn, speed_sp=300, stop_action="coast")
               sleep(sleep_time)

               right_engine.run_forever(speed_sp=-speed,stop_action="coast")
               left_engine.run_forever(speed_sp=speed,stop_action="coast")
               print("po")
               while light_right.reflected_light_intensity >50:
                 continue

               print("stop")
               left_engine.stop(stop_action="coast")
               right_engine.stop(stop_action="coast")


print("po obrocie")
sleep(1)

#po klocek
angle_big=100
angle_turn=100
angle_turn=100
angle_medium=25

medium.run_to_rel_pos(position_sp=45,speed_sp=100,stop_action="coast")
sleep(3)

while not touch_sensor.is_pressed:
        print("to blue")
        blad_l = light_left.reflected_light_intensity - srodek_l
        blad_r = light_right.reflected_light_intensity - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)
       
        left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
        right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")

        poprzedni_blad = blad
        sleep(0.1)
        if (infrared.proximity>40 and infrared.proximity<60):
            left_engine.stop(stop_action="coast")
            right_engine.stop(stop_action="coast")
            break

medium.run_to_rel_pos(position_sp=-angle_medium,speed_sp=300,stop_action="coast")
sleep(1)
right_engine.run_to_rel_pos(position_sp=-angle_big, speed=300,stop_action="coast")
left_engine.run_to_rel_pos(position_sp=-angle_big,speed=300,stop_action="coast")
sleep(1)
medium.run_to_rel_pos(position_sp=angle_medium,speed_sp=300,stop_action="hold")

sleep(1)
right_engine.run_to_rel_pos(position_sp=angle_back, speed=300,stop_action="coast")
left_engine.run_to_rel_pos(position_sp=angle_back,speed=300,stop_action="coast")
sleep(1)

right_engine.run_to_rel_pos(position_sp=angle_turn, speed=300,stop_action="coast")
left_engine.run_to_rel_pos(position_sp=-angle_turn,speed=300,stop_action="coast")
sleep(1)

right_engine.run_forever(speed_sp=100,stop_action="coast")
left_engine.run_forever(speed_sp=-100,stop_action="coast")

while light_left.reflected_light_intensity>35:
    continue

left_engine.stop(stop_action="coast")
right_engine.stop(stop_action="coast")
medium.stop(stop_action="coast")

#obrócony

#powrot na czarna


while not touch_sensor.is_pressed:
        print("to blue")
        blad_l = light_left.reflected_light_intensity - srodek_l
        blad_r = light_right.reflected_light_intensity - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)
       
        left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
        right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")

        poprzedni_blad = blad
        sleep(0.1)
        if light_left.reflected_light_intensity<40 and light_right.reflected_light_intensity<40:
            left_engine.stop(stop_action="coast")
            right_engine.stop(stop_action="coast")
            break


#obrot na czarnej
angle_forward=100

right_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
left_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
sleep(sleep_time)
#obrac sie az naptka czarna
while light_right.reflected_light_intesity>100:
                right_engine.run_forever(speed_sp = -100, stop_action = "coast")
                left_engine.run_forever(speed_sp=100,stop_action="coast")
                sleep(0.1)
                

left_engine.stop(stop_action="coast")
right_engine.stop(stop_action="coast") 
                    

#follow line do czerwonego
while not touch_sensor.is_pressed:
        print("to blue")
        blad_l = light_left.reflected_light_intensity - srodek_l
        blad_r = light_right.reflected_light_intensity - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)
       
        left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
        right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")

        poprzedni_blad = blad
        sleep(0.1)

        #wykrywanie czy najechal na czerwona
        if (light_left.red<red_left+diff and light_left.red>(red_left-diff)):
          if(light_left.green< green_left-diff and light_left.green> green_left-diff):
             if(light_left.blue< blue_left+diff and light_left.blue> blue_left-diff):
                   left_engine.stop(stop_action="coast")
                   right_engine.stop(stop_action="coast")
                   break

        if (light_right.red<red_left+diff and light_right.red>(red_left-diff)):
          if(light_right.green< green_left-diff and light_right.green> green_left-diff):
            if(light_right.blue< blue_left+diff and light_right.blue> blue_left-diff):
                   left_engine.stop(stop_action="coast")
                   right_engine.stop(stop_action="coast")
                   break


if (light_left.red<red_left+diff and light_left.red>(red_left-diff)):
          if(light_left.green< green_left-diff and light_left.green> green_left-diff):
             if(light_left.blue< blue_left+diff and light_left.blue> blue_left-diff):
               right_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               print("przed")

               #obrot przez pierwszy fragment czarnej
               right_engine.run_to_rel_pos(position_sp=angle_turn, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=-angle_turn, speed_sp=300, stop_action="coast")
               sleep(sleep_time)

               right_engine.run_forever(speed_sp=100,stop_action="coast")
               left_engine.run_forever(speed_sp=-100,stop_action="coast")
               print("po")
               while light_left.reflected_light_intensity >50:
                 contiue
               print("stop")
               left_engine.stop(stop_action="coast")
               right_engine.stop(stop_action="coast")

             

if (light_right.red<red_left+diff and light_right.red>(red_left-diff)):
          if(light_right.green< green_left-diff and light_right.green> green_left-diff):
            if(light_right.blue< blue_left+diff and light_right.blue> blue_left-diff):
               right_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               print("przed")

               #obrot przez pierwszy fragment czarnej
               right_engine.run_to_rel_pos(position_sp=-angle_turn, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=angle_turn, speed_sp=300, stop_action="coast")
               sleep(sleep_time)

               right_engine.run_forever(speed_sp=-100,stop_action="coast")
               left_engine.run_forever(speed_sp=100,stop_action="coast")
               print("po")
               while light_right.reflected_light_intensity >50:
                 continue

               print("stop")
               left_engine.stop(stop_action="coast")
               right_engine.stop(stop_action="coast")

#jazda do czerwonego
diff=30

while not touch_sensor.is_pressed:
        print("to blue")
        blad_l = light_left.reflected_light_intensity - srodek_l
        blad_r = light_right.reflected_light_intensity - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)
       
        left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
        right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")

        poprzedni_blad = blad
        sleep(0.1)
       
        #wykrywanie czy najechal na czerwona
        if (light_left.red<red_left+diff and light_left.red>(red_left-diff)):
           if( light_left.green< blue_green_left-diff and light_left.green> green_left-diff):
               if(light_left.blue< blue_left+diff and light_left.blue> blue_left-diff):
                      if (light_right.red<red_right+diff and light_left.red>(red_right-diff)):
                         if( light_left.green< green_right-diff and light_left.green> green_right-diff):
                                if(light_left.blue< blue_right+diff and light_left.blue> blue_right-diff):
                                   left_engine.stop(stop_action="coast")
                                   right_engine.stop(stop_action="coast")
                                   break


sleep(1)
medium.run_to_rel_pos(position_sp=angle_medium,speed_sp=300,stop_action="hold")

sleep(1)
angle_back=100
right_engine.run_to_rel_pos(position_sp=angle_back, speed=300,stop_action="coast")
left_engine.run_to_rel_pos(position_sp=angle_back,speed=300,stop_action="coast")
sleep(1)