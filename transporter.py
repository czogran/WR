

from ev3dev.ev3 import *
from time import sleep



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
    
    #wspolczynniki
    Kp = 5.0
    Kd = 2.0

    predkosc_bazowa = 100.0
    srodek_l = 0
    srodek_r = 0

    #kolory
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
    podniesiony = 0
    opuszczony = 0
    
    def __init__(self):
        podnies_hak_coast()

    def lcdWrite(self,text):
        self.lcd.draw.text((48,13),text)
        self.lcd.update()
    def kalibracja_kolory(self):
        self.lcd.clear()
        lcdWrite("poloz na niebieskim")
        while not self.touch_sensor.is_pressed:
            self.niebieskiLewyR = self.light_left.red
            self.niebieskiPrawyR = self.light_right.red
            self.niebieskiLewyB = self.light_left.blue
            self.niebieskiPrawyB = self.light_right.blue
            self.niebieskiLewyG = self.light_left.green
            self.niebieskiPrawyG = self.light_right.green
        self.lcd.clear()
        lcdWrite("zbadano niebieski, poloz na czerwonym")
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
        lcdWrite("zbadano czerwony")
        while self.touch_sensor.is_pressed:
            continue

    def kalibracja_czujnikow(self):
        lcd.clear()


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
        lcdWrite((48,13),"black left:"+str(self.black_left)+"\n"+"black right:"+str(self.black_right))
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
        lcdWrite((48,13),"white left:"+str(self.white_left)+"\nwhite right:"+str(self.white_right))
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
            blad_prop = Kp * float(blad)
            blad_deri = Kd * float(blad - poprzedni_blad)

            left_engine.run_forever(speed_sp = -predkosc_bazowa - blad_prop + blad_deri, stop_action = "coast")
            right_engine.run_forever(speed_sp = -predkosc_bazowa + blad_prop - blad_deri, stop_action = "coast")

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
        r = self.light_left.red
        b = self.light_left.blue
        g = self.light_left.green
        if inR(r, self.niebieskiLewyR - self.granica_kolory, self.niebieskiLewyR + self.granica_kolory) and inR(b, self.niebieskiLewyB - self.granica_kolory, self.niebieskiLewyB + self.granica_kolory) and inR(g, self.niebieskiLewyG - self.granica_kolory, self.niebieskiLewyG + self.granica_kolory):
            return True
        else:
            return False
    def niebieski_r(self):
        r = self.light_right.red
        b = self.light_right.blue
        g = self.light_right.green
        if inR(r, self.niebieskiPrawyR - self.granica_kolory, self.niebieskiPrawyR + self.granica_kolory) and inR(b, self.niebieskiPrawyB - self.granica_kolory, self.niebieskiPrawyB + self.granica_kolory) and inR(g, self.niebieskiPrawyG - self.granica_kolory, self.niebieskiPrawyG + self.granica_kolory):
            return True
        else:
            return False
    def czerwony_l(self):
        r = self.light_left.red
        b = self.light_left.blue
        g = self.light_left.green
        if inR(r, self.czerwonyLewyR - self.granica_kolory, self.czerwonyLewyR + self.granica_kolory) and inR(b, self.czerwonyLewyB - self.granica_kolory, self.czerwonyLewyB + self.granica_kolory) and inR(g, self.czerwonyLewyG - self.granica_kolory, self.czerwonyLewyG + self.granica_kolory):
            return True
        else:
            return False
    def czerwony_r(self):
        r = self.light_right.red
        b = self.light_right.blue
        g = self.light_right.green
        if inR(r, self.czerwonyPrawyR - self.granica_kolory, self.czerwonyPrawyR + self.granica_kolory) and inR(b, self.czerwonyPrawyB - self.granica_kolory, self.czerwonyPrawyB + self.granica_kolory) and inR(g, self.czerwonyPrawyG - self.granica_kolory, self.czerwonyPrawyG + self.granica_kolory):
            return True
        else:
            return False

    def czarny_l(self):
        r = self.light_left.red
        b = self.light_left.blue
        g = self.light_left.green
        if inR(r, self.czarnyLewyR - self.granica_kolory, self.czarnyLewyR + self.granica_kolory) and inR(b, self.czarnyLewyB - self.granica_kolory, self.czarnyLewyB + self.granica_kolory) and inR(g, self.czarnyLewyG - self.granica_kolory, self.czarnyLewyG + self.granica_kolory):
            return True
        else:
            return False
    def czarny_r(self):
        r = self.light_left.red
        b = self.light_left.blue
        g = self.light_left.green
        if inR(r, self.czarnyPrawyR - self.granica_kolory, self.czarnyPrawyR + self.granica_kolory) and inR(b, self.czarnyPrawyB - self.granica_kolory, self.czarnyPrawyB + self.granica_kolory) and inR(g, self.czarnyPrawyG - self.granica_kolory, self.czarnyPrawyG + self.granica_kolory):
            return True
        else:
            return False
    def czarny_lr_or(self):
        return czarny_l() or czerwony_r()
    def czarny_lr_and(self):
        return czarny_l() and czarny_r()
    def czerwony_lr(self):
        return czerwony_l() or czerwony_r()
    def niebieski_lr(self):
        return niebieski_l() or niebieski_r()
    def czerwony_lr_and(self):
        return czerwony_r() and czerwony_l()
    def inR(self, a, b, c):
        if a > b and a < c:
            return True
        else:
            return False
    def jedz_do_niebieskiej(self):
        jazda_do(niebieski_lr())
    def jedz_do_czerwonej(self):
        jazda_do(czerwony_lr())
    def jedz_do_klocka(self):
        jazda_do(odelglosc_ir())
    def jedz_do_czarnej_and(self):
        jazda_do(czarny_lr())
    def jedz_do_czerwonego_pola(self):
        jazda_do(czerwony_lr_and())
    def zakret(self, kierunek, warunek):
        dojazd = 80
        skret = 80
        jedz_do_przodu(dojazd)
        if kierunek == "lewo":
            zakret_w_lewo(skret)
            zakret_w_lewo_do(warunek())
        elif kierunek == "prawo":
            zakret_w_prawo(skret)
            zakret_w_prawo_do(warunek())
        else:
            lcdWrite("ERROR")
        stop()
    def jedz_do_przodu(self, kat):
        self.left_engine.run_to_rel_pos(position_sp = -kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_to_rel_pos(position_sp = -kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
    def zakret_w_lewo(self, kat):
        self.left_engine.run_to_rel_pos(position_sp = kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_to_rel_pos(position_sp = -kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
    def zakret_w_prawo(self, kat):
        self.left_engine.run_to_rel_pos(position_sp = -kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_to_rel_pos(position_sp = kat, speed_sp = self.predkosc_bazowa, stop_action = "coast")
    def zakret_w_lewo_do(self, warunek):
        self.left_engine.run_forever(speed_sp = -self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_forever(speed_sp = self.predkosc_bazowa, stop_action = "coast")
        while not warunek():
            continue
        stop()
    def zakret_w_prawo_do(self, warunek):
        self.left_engine.run_forever(speed_sp = self.predkosc_bazowa, stop_action = "coast")
        self.right_engine.run_forever(speed_sp = -self.predkosc_bazowa, stop_action = "coast")
        while not warunek():
            continue
        stop()
    def stop(self):
        self.left_engine.stop(stop_action = "coast")
        self.right_engine.stop(stop_action = "coast")
    def zakret_w_lewo_niebieska(self):
        zakret("lewo", niebieski_r())
    def zakret_w_prawo_niebieska(self):
        zakret("prawo", niebieski_l())
    def zakret_w_lewo_czerwona(self):
        zakret("lewo", czerwony_r())
    def zakret_w_prawo_czerwona(self):
        zakret("prawo", czerwony_l())
    def zakret_w_prawo_czarna(self):
        zakret("prawo", czarny_l())
    def zakret_w_lewo_czarna(self):
        zakret("lewo", czarny_r())
    def podnies_klocek(self):
        dystans = 100
        opusc_hak()
        jedz_do_przodu(dystans)
        podnies_hak_hold()
        jedz_do_przodu(-dystans)
    def podnies_hak_hold(self):
        self.medium.run_to_real_pos(position_sp = self.podniesiony, speed_sp = self.predkosc_hak, stop_action = "hold")
    def opusc_hak(self):
        self.medium.run_to_real_pos(position_sp = self.opuszczony, speed_sp = self.predkosc_hak, stop_action = "coast")
    def podnies_hak_coast(self):
        self.medium.run_to_real_pos(position_sp = self.podniesiony, speed_sp = self.predkosc_hak, stop_action = "coast")
    def obrot_lewo_czarna(self):
        zakret_w_lewo_do(czarny_r())
    def obrot_w_prawo_czarna(self):
        zakret_w_prawo_do(czarny_l())
    def start(self):
        lcdWrite("poloz na trasie i wcisnij przycisk aby wystartowac robota")
        while not self.touch_sensor.is_pressed:
            continue
        lcdWrite("START")
    def run(self):
        cofanie = -50
        kalibracja_kolory()
        kalibracja_czujnikow()
        start()
        jedz_do_niebieskiej()
        if niebieski_l():
            zakret_w_lewo_niebieska()
            jedz_do_klocka()
            podnies_hak_hold()
            obrot_w_lewo_czarna()
            jazda_do_czarna_and()
            zakret_w_lewo_czarna()
        else:
            zakret_w_prawo_niebieska()
            jedz_do_klocka()
            podnies_hak_hold()
            obrot_w_lewo_czarna()
            jazda_do_czarna_and()
            zakret_w_prawo_czarna()
        jedz_do_czerwonej()
        if czerwony_l():
            zakret_w_lewo_czerwona()
            jedz_do_czerwonego_pola()
            jedz_do_przodu(cofanie)
            opusc_hak()
            jedz_do_przodu(cofanie)
        else:
            zakret_w_prawo_niebieska()
            jedz_do_czerwonego_pola()
            jedz_do_przodu(cofanie)
            opusc_hak()
            jedz_do_przodu(cofanie)





if __name__ == '__main__':
    robot = Robot()
    robot.run()



