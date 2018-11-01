#po dojechaniu z powrotem na skrzyzowanie czarnej z czerwona musi sie znowu ustawic
#najpierw podjezdza do przodu a potem gdy spotka spotka zewnetrznym czujnikiem czarna to zaczyna byc normalnym follower

if light_right.reflected_light_intesity>100 and light_left.reflected_light_intesity>100:
     #sztywny podjazd
     right_engine.run_timed(time_sp=1000, speed_sp=-200)
     left_engine.run_timed(time_sp=1000, speed_sp=-200)
     #obrac sie az naptka czarna
     while True:
        right_engine.run_forever(speed_sp = -100, stop_action = "coast")
        left_engine.run_forever(speed_sp=100,stop_action="coast")
        sleep(0.1)
        #obraca sie az napotka czarna linie
        if light_right.reflected_light_intesity>100:
             break

 # i potem dalej jedzie wzdluz lini az napotka na niebieskie
 #ale tam sytuacja jest symetryczna i wystarczy zmienic, by zrzucal zamiast podnoscil klocek
              