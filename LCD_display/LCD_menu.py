"""

This is the main file which will hold the Washing Machine code.

"""


ON = 0
OFF = 1
AUTO = 2

lights = ["on", "off", "auto"]
RED = 0
GREEN = 1
BLUE = 2
BLACK = 3
YELLOW = 4

speeds = [0.25,0.5,0.75,1]

IR=0
CAMERA = 1
FREE=2
REMOTE =3
modes = ["IR line follow", "Camera line follow", "free travel"," Remote control"]

colors = ["red", "green", "blue", "black", "yellow"]
SMALL = 0
MIDDLE = 1
BIG =2
camera_size=["640*480","1280*720","1920*1080"]



ultra_distance=[10,20,30,40,50,100]

STOP = 0
BACKUP = 1
TURN = 2
collision_behaviour =["stop","backup","turn around"]

DISABLED = 0
MINIMAL = 1
EXTENSIVE = 2
loggings = ["disabled","minimal","extensive"]
# import RPi.GPIO as GPIO
import time
# import LCD1602 as LCD
import menu_options as op




BtnPin_change = 16
BtnPin_cycle = 13
BtnPin_select = 16
BtnPin_cancle = 12

Gpin = 5
Rpin = 6

menu_list_1 = ["Lights" ,
"Line color",
"Max speed ",
"Working mode",
"Camera image size ",
"Ultrasound detection distance",
"Collision behaviour",
]


menu_list_2 = [["on "," off", "auto"],
              ["red","green","blue","black","yellow"],
               ["25%","50%","75%","100%"],
               ["IR line follow","Camera line follow","free travel","Remote control"],
               ["640*480","1280*720","1920*1080"],
               ["10","20","30","40","40","100"],
               ["stop","backup","turn around"],
               ["disabled","minimal","extensive"]]


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
    GPIO.setup(Gpin, GPIO.OUT)  # Set Green Led Pin mode to output
    GPIO.setup(Rpin, GPIO.OUT)  # Set Red Led Pin mode to output
    # 接正极
    GPIO.setup(BtnPin_change, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(BtnPin_cycle, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(BtnPin_select, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(BtnPin_cancle, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # Set BtnPin's mode is input, and pull up to high level(3.3V)


if __name__ == '__main__':  # Program start from here
    setup()
    LCD.main()
    # menu_1 --main options

    print(op.ON)
    #     def __init__(self, light,color,speed,mode,size,distance,behaviour, logging ):
    menu1 = op.Options1(ON,BLUE,0,CAMERA,MIDDLE,5,TURN,DISABLED)
    user_list = [menu1.light,menu1.color,menu1.speed,menu1.mode,menu1.size,menu1.distance,menu1.behaviour,menu1.logging]
    menu1.light=op.OFF
    print(user_list)
    def set(i,j):
        if i==0:
            menu1.light = j
        elif i==1:
            menu1.color = j
        elif i==2:
            menu1.speed = j
        elif i==3:
            menu1.mode = j
        elif i==4:
            menu1.size = j
        elif i==5:
            menu1.distance = j
        elif i==6:
            menu1.behaviour = j
        elif i==7:
            menu1.logging = j

    def menu1_0():
        i = 0
        try:
            while True:
                LCD.display_page(menu_list_1[i],user_list[i])
                time.sleep(0.5)
                if GPIO.input(BtnPin_change) == True:
                    time.sleep(0.01)
                    if GPIO.input(BtnPin_change) == True:
                        menu2_0(i)
                elif GPIO.input(BtnPin_cycle) == True:
                    time.sleep(0.01)
                    if GPIO.input(BtnPin_cycle) == True:
                        i = (i+1)%8
                else:
                    time.sleep(0.01)

        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.cleanup()

    def menu2_0(i):
        j = 0
        length = len(menu_list_2[i])
        try:
            while True:
                LCD.display_page("set " + str(i+1),menu_list_2[i][j])
                time.sleep(0.5)
                if GPIO.input(BtnPin_change) == True:
                    time.sleep(0.01)
                    if GPIO.input(BtnPin_change) == True:
                        menu2_0(i)
                elif GPIO.input(BtnPin_cycle) == True:
                    time.sleep(0.01)
                    if GPIO.input(BtnPin_cycle) == True:
                        j = (j+1)%length
                elif GPIO.input(BtnPin_select) == True:
                    time.sleep(0.01)
                    if GPIO.input(BtnPin_select) == True:
                        user_list[i] = menu_list_2[i][j]
                        set(i,j)
                        print(user_list)
                elif GPIO.input(BtnPin_cancle) == True:
                    time.sleep(0.01)
                    if GPIO.input(BtnPin_cancle) == True:
                        menu1_0()
                else:
                    time.sleep(0.01)
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
            GPIO.cleanup()

    menu1_0()

