


#plan taki, cofamy sie kawalek, taki by na pewno wjechac na czarna i sie obracamy wokol niej

#powrot na czarna
right_engine.run_timed(time_sp=2000,speed_sp = 200, stop_action = "coast")
left_engine.run_timed(time_sp=2000, speed_sp = 200, stop_action = "coast")

#fragment poczatkowego obracnia sie wokol lini czarnej
right_engine.run_timed(time_sp=2000,speed_sp = 200, stop_action = "coast")
left_engine.run_timed(time_sp=2000, speed_sp = -200, stop_action = "coast")

#obraca sie wokol wlasnej osi az napotka czarna linie
while True:
     right_engine.run_forever(speed_sp = 100, stop_action = "coast")
     left_engine.run_forever(speed_sp=-100,stop_action="coast")
     sleep(0.1)
     #obraca sie az napotka czarna linie
     if light_right.reflected_light_intesity>100:
       break