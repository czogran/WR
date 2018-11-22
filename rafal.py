from ev3dev.ev3 import * 
from time import *

class Robot:
    light_left = ColorSensor('in1')
    light_right = ColorSensor('in2')
    touch_sensor = TouchSensor()
    infrared = InfraredSensor()
    lcd = Screen()
    
    right_engine = LargeMotor('outB')
    left_engine = LargeMotor('outA')
    medium = MediumMotor()
    
    white_left = 0
    white_right = 0
    black_left = 0
    black_right = 0
    
    # wspolczynniki
    Kp = 2.0
    Kd = 0.5
    predkosc_bazowa = 50.0
    srodek_l = 0
    srodek_r = 0
    # kolory
    niebieskiLewyR = 30
    niebieskiLewyB = 210
    niebieskiLewyG = 68
    niebieskiPrawyR = 30
    niebieskiPrawyB = 230
    niebieskiPrawyG = 79
    czerwonyLewyR = 220
    czerwonyLewyB = 48
    czerwonyLewyG = 17
    czerwonyPrawyR = 275
    czerwonyPrawyB = 52
    czerwonyPrawyG = 19
    czarnyLewyR = 0
    czarnyLewyB = 0
    czarnyLewyG = 0
    czarnyPrawyR = 0
    czarnyPrawyB = 0
    czarnyPrawyG = 0
    bialyLewyR = 300
    bialyLewyB = 300
    bialyLewyG = 300
    bialyPrawyR = 300
    bialyPrawyB = 300
    bialyPrawyG = 300
    granica_kolory = 30
    #hak
    podniesiony_z_wejsciowej = 100
    podniesiony = 60
    opuszczony = -60
    predkosc_hak = 100
    
    #czas
    czas0 = 0
    def __init__(self):
        self.medium.reset()
        self.podnies_hak_poczatek()
    def lcdWrite(self, text):
        self.lcd.draw.text((48, 13), text)
        self.lcd.update()
    def kalibracja_kolory(self):
        self.lcd.clear()
        self.lcdWrite("poloz na niebieskim")
        while not self.touch_sensor.is_pressed:
            self.niebieskiLewyR = self.light_left.red
            self.niebieskiPrawyR = self.light_right.red
            self.niebieskiLewyB = self.light_left.blue
            self.niebieskiPrawyB = self.light_right.blue
            self.niebieskiLewyG = self.light_left.green
            self.niebieskiPrawyG = self.light_right.green
        self.lcd.clear()
        self.lcdWrite("zbadano niebieski, poloz na czerwonym")
        while self.touch_sensor.is_pressed:
            continue
        while not self.touch_sensor.is_pressed:
            self.czerwonyLewyR = self.light_left.red
            self.czerwonyPrawyR = self.light_right.red
            self.czerwonyLewyB = self.light_left.blue
            self.czerwonyPrawyB = self.light_right.blue
            self.czerwonyLewyG = self.light_left.green
            self.czerwonyPrawyG = self.light_right.green
        self.lcd.clear()
        self.lcdWrite("zbadano czerwony")
        while self.touch_sensor.is_pressed:
            continue
    def kalibracja_czujnikow(self):
        self.lcd.clear()
        while not self.touch_sensor.is_pressed:
            self.black_left = self.light_left.reflected_light_intensity
            self.black_right = self.light_right.reflected_light_intensity
            self.czarnyLewyR = self.light_left.red
            self.czarnyPrawyR = self.light_right.red
            self.czarnyLewyB = self.light_left.blue
            self.czarnyPrawyB = self.light_right.blue
            self.czarnyLewyG = self.light_left.green
            self.czarnyPrawyG = self.light_right.green
        print("black left:"+str(self.black_left)+"\n"+"black right:"+str(self.black_right))
        self.lcdWrite("black left:"+str(self.black_left)+"\nblack right:"+str(self.black_right))
        while self.touch_sensor.is_pressed:
            continue
        while not self.touch_sensor.is_pressed:
            self.lcd.clear()
            self.white_left = self.light_left.reflected_light_intensity
            self.white_right = self.light_right.reflected_light_intensity
            self.bialyLewyR = self.light_left.red
            self.bialyPrawyR = self.light_right.red
            self.bialyLewyB = self.light_left.blue
            self.bialyPrawyB = self.light_right.blue
            self.bialyLewyG = self.light_left.green
            self.bialyPrawyG = self.light_right.green
        print("white left:"+str(self.white_left)+"\nwhite right:"+str(self.white_right))
        self.lcdWrite("white left:"+str(self.white_left)+"\nwhite right:"+str(self.white_right))
        while self.touch_sensor.is_pressed:
            continue
        self.lcd.clear()
        self.srodek_l = (self.white_left + self.black_left) // 2
        self.srodek_r = (self.white_right + self.black_right) // 2
    def jazda_do(self, warunek):
        blad = 0
        poprzedni_blad = 0
        blad_l = 0
        blad_r = 0
        blad_prop = 0.0
        blad_deri = 0.0
        while not warunek():
            blad_l = self.light_left.reflected_light_intensity - self.srodek_l
            blad_r = self.light_right.reflected_light_intensity - self.srodek_r
            blad = blad_r - blad_l
            blad_prop = self.Kp * float(blad)
            blad_deri = self.Kd * float(blad - poprzedni_blad)
            self.left_engine.run_forever(speed_sp = -self.predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
            self.right_engine.run_forever(speed_sp = -self.predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")
            poprzedni_blad = blad
            sleep(0.1)
    def odleglosc_ir(self):
        min_odleglosc = 40
        max_odleglosc = 60
        if self.infrared.proximity > min_odleglosc and self.infrared.proximity < max_odleglosc:
            return True
        else:
            return False
    def niebieski_l(self):
#        r = self.light_left.red
#        b = self.light_left.blue
#        g = self.light_left.green
#        if self.inR(r, self.niebieskiLewyR - self.granica_kolory, self.niebieskiLewyR + self.granica_kolory) and self.inR(b, self.niebieskiLewyB - self.granica_kolory, self.niebieskiLewyB + self.granica_kolory) and self.inR(g, self.niebieskiLewyG - self.granica_kolory, self.niebieskiLewyG + self.granica_kolory):
#            return True
#        else:
#            return False

        r=self.light_left.red
        if self.inR(r,self.niebieskiLewyR-self.granica_kolory,self.niebieskiLewyR+self.granica_kolory):
            b=self.light_left.blue
            if self.inR(b,self.niebieskiLewyB-self.granica_kolory,self.niebieskiLewyB+self.granica_kolory):
                g=self.light_left.green
                if self.inR(g,self.niebieskiLewyG-self.granica_kolory,self.niebieskiLewyG+self.granica_kolory):
                    return True
        return False
    def niebieski_r(self):
        r=self.light_right.red
        if self.inR(r,self.niebieskiPrawyR-self.granica_kolory,self.niebieskiPrawyR+self.granica_kolory):
            b=self.light_right.blue
            if self.inR(b,self.niebieskiPrawyB-self.granica_kolory,self.niebieskiPrawyB+self.granica_kolory):
                g=self.light_right.green
                if self.inR(g,self.niebieskiPrawyG-self.granica_kolory,self.niebieskiPrawyG+self.granica_kolory):
                    return True
        return False
        
        # r = self.light_right.red
       # b = self.light_right.blue
       # g = self.light_right.green
       # if self.inR(r, self.niebieskiPrawyR - self.granica_kolory, 
#self.niebieskiPrawyR + self.granica_kolory) and self.inR(b, 
#self.niebieskiPrawyB - self.granica_kolory, self.niebieskiPrawyB + 
#self.granica_kolory) and self.inR(g, self.niebieskiPrawyG - 
#self.granica_kolory, self.niebieskiPrawyG + self.granica_kolory):
            #return True
       # else:
        #    return False
    def czerwony_l(self):
        r=self.light_left.red
        if self.inR(r,self.czerwonyLewyR-self.granica_kolory,self.czerwonyLewyR+self.granica_kolory):
            b=self.light_left.blue
            if self.inR(b,self.czerwonyLewyB-self.granica_kolory,self.czerwonyLewyB+self.granica_kolory):
                g=self.light_left.green
                if self.inR(g,self.czerwonyLewyG-self.granica_kolory,self.czerwonyLewyG+self.granica_kolory):
                    return True
        return False
 
    def czerwony_r(self):
        r=self.light_right.red
        if self.inR(r,self.czerwonyPrawyR-self.granica_kolory,self.czerwonyPrawyR+self.granica_kolory):
            b=self.light_right.blue
            if self.inR(b,self.czerwonyPrawyB-self.granica_kolory,self.czerwonyPrawyB+self.granica_kolory):
                g=self.light_right.green
                if self.inR(g,self.czerwonyPrawyG-self.granica_kolory,self.czerwonyPrawyG+self.granica_kolory):
                    return True
        return False
 

    def czarny_l(self):
        #r = self.light_left.red
        #b = self.light_left.blue
        #g = self.light_left.green
        #if self.inR(r, self.czarnyLewyR - self.granica_kolory, 
#self.czarnyLewyR + self.granica_kolory) and self.inR(b, self.czarnyLewyB 
#- self.granica_kolory, self.czarnyLewyB + self.granica_kolory) and self.inR(g, self.czarnyLewyG - self.granica_kolory, self.czarnyLewyG + self.granica_kolory):
 #           return True
 #       else:
  #          return False
        if self.light_left.reflected_light_intensity<40:
            return True
        else:
            return False

    def czarny_r(self):
    #    r = self.light_left.red
   #     b = self.light_left.blue
  #      g = self.light_left.green
 #       if self.inR(r, self.czarnyPrawyR - self.granica_kolory, 
#self.czarnyPrawyR + self.granica_kolory) and self.inR(b, 
#self.czarnyPrawyB - self.granica_kolory, self.czarnyPrawyB + 
#self.granica_kolory) and self.inR(g, self.czarnyPrawyG - 
#self.granica_kolory, self.czarnyPrawyG + self.granica_kolory):
     #       return True
      #  else:
       #     return False
        if self.light_right.reflected_light_intensity<40:
            return True
        else:
            return False


    def czarny_lr_or(self):
        return self.czarny_l() or self.czerwony_r()
    def czarny_lr_and(self):
        return self.czarny_l() and self.czarny_r()
    def czerwony_lr(self):
        return self.czerwony_l() or self.czerwony_r()
    def niebieski_lr(self):
        return self.niebieski_l() or self.niebieski_r()
    def czerwony_lr_and(self):
        return self.czerwony_r() and self.czerwony_l()
    def inR(self, a, b, c):
        if a > b and a < c:
            return True
        else:
            return False
    def jedz_do_niebieskiej(self):
        self.jazda_do(self.niebieski_lr)
    def jedz_do_czerwonej(self):
        self.jazda_do(self.czerwony_lr)
    def jedz_do_klocka(self):
        self.jazda_do(self.odleglosc_ir)
    def jedz_do_czarnej_and(self):
        self.jazda_do(self.czarny_lr_and)
        self.stop()
    def jedz_do_czerwonego_pola(self):
        self.jazda_do(self.czerwony_lr_and)
    def zakret(self, kierunek, warunek):
        dojazd = 55
        skret = 80
        self.jedz_do_przodu(dojazd)
        if kierunek == "lewo":
            self.zakret_w_lewo(skret)
            self.zakret_w_lewo_do(warunek)
        elif kierunek == "prawo":
            self.zakret_w_prawo(skret)
            self.zakret_w_prawo_do(warunek)
        else:
            self.lcdWrite("ERROR")
        self.stop()
    def jedz_do_przodu(self, kat):
        self.left_engine.run_to_rel_pos(position_sp = -kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_to_rel_pos(position_sp = -kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        sleep(3)
    def zakret_w_lewo(self, kat):
        self.left_engine.run_to_rel_pos(position_sp =- kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_to_rel_pos(position_sp = kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        sleep(4)
    def zakret_w_prawo(self, kat):
        self.left_engine.run_to_rel_pos(position_sp = kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_to_rel_pos(position_sp = -kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        sleep(4)
    def zakret_w_lewo_do(self, warunek):
        self.left_engine.run_forever(speed_sp = -self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_forever(speed_sp = self.predkosc_bazowa, stop_action = "coast")
        while not warunek():
            continue
        self.stop()
    def zakret_w_prawo_do(self, warunek):
        self.left_engine.run_forever(speed_sp = self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_forever(speed_sp = -self.predkosc_bazowa, stop_action = "coast")
        while not  warunek():
            continue
        self.stop()
    def stop(self):
        self.left_engine.stop(stop_action = "coast")
        self.right_engine.stop(stop_action = "coast")
    def zakret_w_lewo_niebieska(self):
        self.zakret("lewo", self.niebieski_r)
    def zakret_w_prawo_niebieska(self):
        self.zakret("prawo", self.niebieski_l)
    def zakret_w_lewo_czerwona(self):
        self.zakret("lewo", self.czerwony_r)
    def zakret_w_prawo_czerwona(self):
        self.zakret("prawo", self.czerwony_l)
    def zakret_w_prawo_czarna(self):
        self.zakret("prawo", self.czarny_l)
    def zakret_w_lewo_czarna(self):
        self.zakret("lewo", self.czarny_r)
    def podnies_klocek(self):
        dystans = 200

        self.stop()
        self.opusc_hak()
        self.jedz_do_przodu(dystans)
        self.podnies_hak_hold()
        self.jedz_do_przodu(-dystans)
    def podnies_hak_hold(self):
        self.medium.run_to_rel_pos(position_sp = self.podniesiony, speed_sp = self.predkosc_hak, stop_action = "hold")
        sleep(4)
    def opusc_hak(self):
        self.medium.run_to_rel_pos(position_sp = self.opuszczony, speed_sp = self.predkosc_hak, stop_action = "coast")
        sleep(4)
    def podnies_hak_coast(self):
        self.medium.run_to_rel_pos(position_sp = self.podniesiony, speed_sp = self.predkosc_hak, stop_action = "coast")
        sleep(4)
    def podnies_hak_poczatek(self):
        self.medium.run_to_rel_pos(position_sp = self.podniesiony_z_wejsciowej, speed_sp = self.predkosc_hak, stop_action = "coast")
        sleep(4)
    def obrot_lewo_czarna(self):
        self.zakret_w_lewo(300)
        self.zakret_w_lewo_do(self.czarny_r)
    def obrot_w_prawo_czarna(self):
        self.zakret_w_prawo_do(self.czarny_l)
    def start(self):
        self.lcdWrite("poloz na trasie i wcisnij przycisk aby wystartowac robota")
        while not self.touch_sensor.is_pressed:
            continue
        self.lcdWrite("START")
    def cofanie(self, kat):
        self.jedz_do_przodu(-kat)
    def timer_start(self):
        self.czas0 = time()
    def czy_minelo(self, czas):
        if time() - self.czas0 < czas:
            return False
        else:
            return True
    
    def czy_minely_2s(self):
        return self.czy_minelo(2)
    def do_czerwonej_2s(self):
        self.timer_start()
        self.jazda_do(self.czy_minely_2s)
        self.jazda_do_czerwonej()
    def run(self):
        cofanie = -50
        self.kalibracja_kolory()
        self.kalibracja_czujnikow()
        self.start()
        self.jedz_do_niebieskiej()
        if self.niebieski_l():
            self.zakret_w_lewo_niebieska()
            self.jedz_do_klocka()
            self.podnies_klocek()
            self.cofanie(50)
            self.obrot_lewo_czarna()
            self.jedz_do_czarnej_and()
            self.zakret_w_lewo_czarna()
        else:
            self.zakret_w_prawo_niebieska()
            self.jedz_do_klocka()
            self.podnies_klocek()
            self.cofanie(50)
            self.obrot_lewo_czarna()
            self.jedz_do_czarnej_and()
            self.zakret_w_prawo_czarna()
        self.jedz_do_czerwonej()
        if self.czerwony_l():
            self.zakret_w_lewo_czerwona()
            self.jedz_do_czerwonego_pola()
            self.jedz_do_przodu(cofanie)
            self.opusc_hak()
            self.jedz_do_przodu(cofanie)
        else:
            self.zakret_w_prawo_czerwona()
            self.jedz_do_czerwonego_pola()
            self.jedz_do_przodu(cofanie)
            self.opusc_hak()
            self.jedz_do_przodu(cofanie)
if __name__ == '__main__':
    robot = Robot()
    robot.run()