


#pobiez czarne
def black():
    global black_left
    global black_right
    global light_left
    global light_right
    global touch_sensor
    lcd.clear()
    while not touch_sensor.is_pressed:
        black_left = light_left.reflected_light_intensity
        black_right = light_right.reflected_light_intensity
    print("black left:"+str(black_left)+"\n"+"black right:"+str(black_right))
    lcd.draw.text((48,13),"black left:"+str(black_left)+"\n"+"black right:"+str(black_right))
    lcd.update()
    while touch_sensor.is_pressed:
        continue

#pobież biale
def white():
    global white_left
    global white_right
    global light_left
    global light_right
    global touch_sensor
    lcd.clear()
    while not touch_sensor.is_pressed:
        white_left = light_left.reflected_light_intensity
        white_right = light_right.reflected_light_intensity
    print("white left:"+str(white_left)+"\nwhite right:"+str(white_right))
    lcd.draw.text((48,13),"white left:"+str(white_left)+"\nwhite right:"+str(white_right))
    lcd.update()
    while touch_sensor.is_pressed:
        continue


#pobiez czerwone
def red():
    global red_left
    global red_right
    global blue_left
    global blue_right
    global green_left
    global green_right
    global touch_sensor
    lcd.clear()
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

#follow line do czerwonego
#diff zakres na ktorym ma sie zatrzymac
def drive_to_red(diff):
    global touch_sensor
    global black_left
    global blad_right
    global white_left
    global white_right
    global light_right
    global light_left
    global red_left
    global red_right
    global blue_left
    global blue_right
    global green_left
    global green_right
    global Kp
    global Kd
    global srodek_l
    global srodek_r
    global predkosc_bazowa

    #nie wiem czy silnik tez nie powinny byc

    while not touch_sensor.is_pressed:
        blad_l = light_left.reflected_light_intensity - srodek_l
        blad_r = light_right.reflected_light_intensity - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)
       
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
                   left_engine.stop(stop_action="coast")
                   right_engine.stop(stop_action="coast")
                   break
        if (red_right_travel<red_right+diff and red_right_travel>(red_right-diff)):
           if( green_right_travel< green_right-diff and green_right_travel> green_right-diff):
               if(blue_right_travel< blue_right+diff and blue_right_travel> blue_right-diff):
                   left_engine.stop(stop_action="coast")
                   right_engine.stop(stop_action="coast")
                   break



#sztywny obrot przy czerwonej
def red_trun(angle_forward,angle_turn):
    if (red_left_travel<red_left+diff and red_left_travel>(red_left-diff)):
       if( green_left_travel< green_left-diff and green_left_travel> green_left-diff):
           if(blue_left_travel< blue_left+diff and blue_left_travel> blue_left-diff):
               #pierwszy fragment-podjazd do przodu
               right_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")

               #obrot przez pierwszy fragment czarnej
               right_engine.run_to_rel_pos(position_sp=-angle_turn, speed_sp=300, stop_action="coast")
               left_engine.run_to_rel_pos(position_sp=angle_turn, speed_sp=300, stop_action="coast")
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

    if (red_right_travel<red_right+diff and red_right_travel>(red_right-diff)):
           if( green_right_travel< green_right-diff and green_right_travel> green_right-diff):
               if(blue_right_travel< blue_right+diff and blue_right_travel> blue_right-diff):
                   #pierwszy fragment-podjazd do przodu
                   right_engine.run_to_rel_pos(position_sp=angle_forward, speed_sp=300, stop_action="coast")
                   left_engine.run_to_rel_pos(position_sp=angle_forward, speed_sp=300, stop_action="coast")

                   #obrot przez pierwszy fragment czarnej
                   right_engine.run_to_rel_pos(position_sp=angle_turn, speed_sp=300, stop_action="coast")
                   left_engine.run_to_rel_pos(position_sp=-angle_turn, speed_sp=300, stop_action="coast")
                   #obrac sie az naptka czarna
                   while True:
                        right_engine.run_forever(speed_sp = 100, stop_action = "coast")
                        left_engine.run_forever(speed_sp=-100,stop_action="coast")
                        sleep(0.1)
                        #obraca sie az napotka czarna linie
                        if light_right.reflected_light_intesity>100:
                            left_engine.stop(stop_action="coast")
                            right_engine.stop(stop_action="coast")
                            break

#jazda do klocka
def to_brick(angle_big,angle_medium):
    global touch_sensor
    global black_left
    global blad_right
    global white_left
    global white_right
    global light_right
    global light_left
    global Kp
    global Kd
    global srodek_l
    global srodek_r
    global predkosc_bazowa

    #nie wiem czy silnik tez nie powinny byc

    while not touch_sensor.is_pressed:
        blad_l = light_left.reflected_light_intensity - srodek_l
        blad_r = light_right.reflected_light_intensity - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)
       
        left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
        right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")
        
        poprzedni_blad = blad
        sleep(0.1)
        
        if infrared.proximity >40 and infrared.proximity<60:
            left_engine.stop(stop_action="coast")
            right_engine.stop(stop_action="coast")    
            break
 
    #podnsiesienie klocka, nie wiem w ktora strone jaki kierunek ma silnik medium
    medium.run_to_rel_pos(position_sp=angle_medium, speed_sp=300, stop_action="coast")
    right_engine.run_to_rel_pos(position_sp=-angle_big, speed_sp=300, stop_action="coast")
    left_engine.run_to_rel_pos(position_sp=-angle_big, speed_sp=300, stop_action="coast")
    medium.run_to_rel_pos(position_sp=-angle_medium, speed_sp=300, stop_action="coast")



#powrot na czarna
def come_back_to_black(angle_back,angle_turn):
    #right_engine.run_timed(time_sp=time_back,speed_sp = 200, stop_action = "coast")
    # left_engine.run_timed(time_sp=time_back, speed_sp = 200, stop_action = "coast")
    right_engine.run_to_rel_pos(position_sp=angle_back, speed_sp=300, stop_action="coast")
    left_engine.run_to_rel_pos(position_sp=angle_back, speed_sp=300, stop_action="coast")
    #fragment poczatkowego obracnia sie wokol lini czarnej
    right_engine.run_to_rel_pos(position_sp=angle_turn, speed_sp=300, stop_action="coast")
    left_engine.run_to_rel_pos(position_sp=-angle_turn, speed_sp=300, stop_action="coast")

    #obraca sie wokol wlasnej osi az napotka czarna linie
    while True:
         right_engine.run_forever(speed_sp = 100, stop_action = "coast")
         left_engine.run_forever(speed_sp=-100,stop_action="coast")
         sleep(0.1)
         #obraca sie az napotka czarna linie
         if light_right.reflected_light_intesity>100:
             left_engine.stop(stop_action="coast")
             right_engine.stop(stop_action="coast")
             break


#powrot do skrzyzowania z czarna, potem obrot
def to_brick(angle_forward):
    global touch_sensor
    global black_left
    global blad_right
    global white_left
    global white_right
    global light_right
    global light_left
    global Kp
    global Kd
    global srodek_l
    global srodek_r
    global predkosc_bazowa
 
    #nie wiem czy silnik tez nie powinny byc

    while not touch_sensor.is_pressed:
        blad_l = light_left.reflected_light_intensity - srodek_l
        blad_r = light_right.reflected_light_intensity - srodek_r
        blad = blad_l - blad_r
        blad_prop = Kp * float(blad)
        blad_deri = Kd * (blad - poprzedni_blad)
       
        left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
        right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")
        
        poprzedni_blad = blad
        sleep(0.1)
        if light_right.reflected_light_intesity>100 and light_left.reflected_light_intesity>100:
             left_engine.stop(stop_action="coast")
             right_engine.stop(stop_action="coast") 
             #sztywny podjazd
             right_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
             left_engine.run_to_rel_pos(position_sp=-angle_forward, speed_sp=300, stop_action="coast")
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

