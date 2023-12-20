# ON = 0
# OFF = 1
# AUTO = 2
#
# lights = ["on", "off", "auto"]
# RED = 0
# GREEN = 1
# BLUE = 2
# BLACK = 3
# YELLOW = 4
#
# speeds = [0.25,0.5,0.75,1]
#
# IR=0
# CAMERA = 1
# FREE=2
# REMOTE =3
# modes = ["IR line follow", "Camera line follow", "free travel"," Remote control"]
#
# colors = ["red", "green", "blue", "black", "yellow"]
# SMALL = 0
# MIDDLE = 1
# BIG =2
# camera_size=["640*480","1280*720","1920*1080"]
#
#
#
# ultra_distance=[10,20,30,40,50,100]
#
# STOP = 0
# BACKUP = 1
# TURN = 2
# collision_behaviour =["stop","backup","turn around"]
#
# DISABLED = 0
# MINIMAL = 1
# EXTENSIVE = 2
# loggings = ["disabled","minimal","extensive"]

# 用于给其他函数传递参数值，这里的数值都是每个选项数组index
# 到时候 IRLineFollow(Options1 op):
class Options1:

    def __init__(self, light,color,speed,mode,size,distance,behaviour, logging ):
        # Lights on / off / auto
        # Line color red / green / blue / black / yellow /
        # Max speed 25% / 50% / 75% / 100%
        # Working mode: IR line follow, Camera line follow, free travel, Remote control
        # Camera image size 640*480, 1280*720, 1920 * 1080
        # Ultrasound detection distance: 10cm, 20cm, 30cm, 40cm, 50cm, 1m
        # Collision behaviour: stop / backup / turn around
        # logging: disabled, minimal, extensive

        self.light = light
        self.color = color
        self.speed = speed
        self.mode = mode
        self.size = size
        self.distance = distance
        self.behaviour = behaviour
        self.logging = logging


