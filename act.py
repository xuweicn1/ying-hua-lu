import RPi.GPIO as GPIO
import time
import drivers

class SN74595:
    def __init__(self, ser, rclk, srclk, oe=None, srclr=None):
        for pin in [ser, oe, rclk, srclk, srclr]:
            if pin is not None:
                GPIO.setup(pin, GPIO.OUT, initial = 0)
        self.ser = ser
        self.oe = oe
        self.rclk = rclk
        self.srclk = srclk
        self.srclr = srclr
        if srclr != None:
            GPIO.output(srclr, 1)
                
    def clear(self):
        GPIO.output(self.srclr, 0)
        GPIO.output(self.srclr, 1)

    def update(self):
        GPIO.output(self.rclk, 1)
        GPIO.output(self.rclk, 0)

    def streamin(self, statuslst):
        for s in statuslst:
            GPIO.output(self.ser, s)
            GPIO.output(self.srclk, 1)
            GPIO.output(self.srclk, 0)

    def negoe(self, status):
        GPIO.output(self.oe, status)

class HX711:
    def __init__(self, psck, pdt):
        GPIO.setup(pdt, GPIO.IN)
        GPIO.setup(psck, GPIO.OUT, initial=0)
        self.pdt = pdt
        self.psck = psck
        
    def getdv(self):
        d = 0
        while GPIO.input(self.pdt)==1:
            pass
        for i in range(24):
            GPIO.output(self.psck, 1)
            GPIO.output(self.psck, 0)
            d = (d << 1) | GPIO.input(self.pdt)
        GPIO.output(self.psck, 1)
        GPIO.output(self.psck, 0)

        if (d & (1 << (24 - 1))) != 0:
            d = d - (1 << 24)
        return d

class SerialMeter:
    def __init__(self, psck, pdt):
        GPIO.setup(pdt, GPIO.IN)
        GPIO.setup(psck, GPIO.OUT, initial=0)
        self.pdt = pdt
        self.psck = psck
        
    def getdv(self, nbits=24):
        dr = [0] * len(self.pdt)

        for dt in self.pdt:
            while GPIO.input(dt)==1:
                pass
            
        for i in range(nbits):
            GPIO.output(self.psck, 1)
            GPIO.output(self.psck, 0)
            for (j, dt) in enumerate(self.pdt):
                dr[j] = (dr[j] << 1) | GPIO.input(dt)
                
        GPIO.output(self.psck, 1)
        GPIO.output(self.psck, 0)

        for j in range(len(dr)):
            if (dr[j] & (1 << (nbits - 1))) != 0:
                dr[j] = dr[j] - (1 << nbits)
            
        return dr

if __name__=='__main__':
    GPIO.setmode(GPIO.BCM)
                
#    w = SerialMeter(2, [3, 4])
    w = SerialMeter(2, [3, 4])
    print("50") 
    for i in range(20):
        
        dv = w.getdv()
        print(dv)
        time.sleep(0.2)
        i = i+1
    

    # ws0 = HX711(2, 3)
    # print("711-ws0", ws0)


    # ws1 = HX711(2, 4)
    # print("711-ws1", ws1)

    GPIO.setup([21, 20, 16],GPIO.OUT)
    s=SN74595(21, 20, 16)
    # s.streamin([0])
    # s.update()
    print("0")
    s.streamin([0]*16)
    time.sleep(2)
    s.update()

    # print("1")
    # s.streamin([1])
    # s.update()
    # time.sleep(1)

    # print("2")
    # s.streamin([1])
    # s.update()
    # time.sleep(1)

    # print("3")
    # s.streamin([1])
    # s.update()
    # time.sleep(1)

    # print("4")
    # s.streamin([1])
    # s.update()
    # time.sleep(1)

    # print("5")
    # s.streamin([1])
    # s.update()
    # time.sleep(1)



    # print("1")
    # s.streamin([1]*16)
    # time.sleep(2)
    # s.update()
    # print("0")
    # s.streamin([0]*16)
    # time.sleep(2)
    # s.update()
