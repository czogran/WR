
#kod do dodania jak zadziala zatrzymywanie sie na czerwonym Rafała wersja

if (red_left_travel<red_left+diff and red_left_travel>(red_left-diff)):
       if( green_left_travel< green_left-diff and green_left_travel> green_left-diff):
           if(blue_left_travel< blue_left+diff and blue_left_travel> blue_left-diff):
              #pierwszy fragment-podjazd do przodu
              right_engine.run_timed(time_sp=1000, speed_sp=-200)
              left_engine.run_timed(time_sp=1000, speed_sp=-200)

              #obrot przez pierwszy fragment czarnej
              right_engine.run_timed(time_sp=2000,speed_sp = -100, stop_action = "coast")
              left_engine.run_timed(timed_sp=2000,speed_sp=100,stop_action="coast")
              #obrac sie az naptka czarna
              while True:
                right_engine.run_forever(speed_sp = -100, stop_action = "coast")
                left_engine.run_forever(speed_sp=100,stop_action="coast")
                sleep(0.1)
                #obraca sie az napotka czarna linie
                if light_right.reflected_light_intesity>100:
                    break
    
              

if (red_right_travel<red_right+diff and red_right_travel>(red_right-diff)):
       if( green_right_travel< green_right-diff and green_right_travel> green_right-diff):
           if(blue_right_travel< blue_right+diff and blue_right_travel> blue_right-diff):
              #pierwszy fragment-podjazd do przodu
              right_engine.run_timed(time_sp=1000, speed_sp=-200)
              left_engine.run_timed(time_sp=1000, speed_sp=-200)

              #obrot przez pierwszy fragment czarnej
              right_engine.run_timed(time_sp=2000,speed_sp = 100, stop_action = "coast")
              left_engine.run_timed(timed_sp=2000,speed_sp=-100,stop_action="coast")
              #obrac sie az naptka czarna
              while True:
                right_engine.run_forever(speed_sp = 100, stop_action = "coast")
                left_engine.run_forever(speed_sp=-100,stop_action="coast")
                sleep(0.1)
                #obraca sie az napotka czarna linie
                if light_right.reflected_light_intesity>100:
                    break




#kod do dodania jak zadziala zatrzymywanie sie na czerwonym moja wersja

if (red_left_travel<red_left+diff and red_left_travel>(red_left-diff)):
       if( green_left_travel< green_left-diff and green_left_travel> green_left-diff):
           if(blue_left_travel< blue_left+diff and blue_left_travel> blue_left-diff):
              #pierwszy fragment-sztywny obrot przez pierwsza czerwona linie
              right_engine.run_timed(time_sp=2000, speed_sp=-200)
              while True:
                right_engine.run_forever(speed_sp = -100, stop_action = "coast")
                sleep(0.1)
                #obraca sie az napotka czarna linie
                if light_right.reflected_light_intesity>100:
                    break
    
              

if (red_right_travel<red_right+diff and red_right_travel>(red_right-diff)):
       if( green_right_travel< green_right-diff and green_right_travel> green_right-diff):
           if(blue_right_travel< blue_right+diff and blue_right_travel> blue_right-diff):
                #pierwszy fragment-sztywny obrot przez pierwsza czerwona linie
              left_engine.run_timed(time_sp=2000, speed_sp=-200)
              while True:
                left_engine.run_forever(speed_sp = -100, stop_action = "coast")
                sleep(0.1)
                #obraca sie az napotka czarna linie
                if light_left.reflected_light_intesity>100:
                    break
