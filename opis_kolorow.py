from ev3dev.ev3 import *
from time import sleep
light_left = ColorSensor('in2')
light_right = ColorSensor('in1')
touch_sensor = TouchSensor('in4')
lcd = Screen()
right_engine = LargeMotor('outB')
left_engine = LargeMotor('outA')
medium=MediumMotor('outC')
white_left =77
white_right = 77
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
diff=50
value=200
Kp=5
Kd=1
srodek_l = (white_left + black_left) // 2
srodek_r = (white_right + black_right) // 2
licznik=0
#follow line do niebieskiego
while not touch_sensor.is_pressed:
        l=light_left.reflected_light_intensity
        r= light_right.reflected_light_intensity
        blad_l =  l- srodek_l
        blad_r =r - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)       
        poprzedni_blad = blad
        sleep(0.1)
        if(l<50 and blad<20 and licznik<2) :  
           licznik=licznik+1
           left_engine.stop(stop_action="coast")
           right_engine.stop(stop_action="coast")
           if(light_left.red>value):
               print("red")
               Sound.speak('red').wait()
           elif(light_left.blue>value):
               print("blue")
               Sound.speak('blue').wait()
           elif(light_left.green>value):
               print("green")
               Sound.speak('green').wait()
           elif (light_left.yellow>value):
               print("zolty")
               Sound.speak('yellow').wait()
           else:
               print("czarny")
           sleep(2)
           left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
           right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")
        elif(r<50 and blad<20 and licznik<2) : 
           licznik=licznik+1
           left_engine.stop(stop_action="coast")
           right_engine.stop(stop_action="coast") 
           if(light_right.red>value):
               print("red")
               Sound.speak('red').wait()
           elif(light_right.blue>value):
               print("blue")
               Sound.speak('blue').wait()
           elif(light_right.green>value):
               print("green")
               Sound.speak('green').wait()
           elif (light_right.yellow>value):
               print("zolty")
               Sound.speak('yellow').wait()
           else:
               print("czarny")
           sleep(2)
           left_engine.run_forever(speed_sp =-predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
           right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")
        if licznik<8:
            licznik=licznik+1
        else:
            licznik=0
left_engine.stop(stop_action="coast")
right_engine.stop(stop_action="coast")
          
      