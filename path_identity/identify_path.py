# 巡线
# find road
# 在一张图像中找出一行中蓝色像素所在的位置
import math

import cv2
import numpy as np
import point
import point_intersection as pi
import line


# 图像色彩空间变换
def exchange(img):
    # 裁剪坐标为[y0:y1, x0:x1]
    # cropped = img[0:640, 100:480]
    #  to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # remove irrelevant info

    print("baocunchengogng")
    # mask know hsv picture where is blue
    lower_blue = np.array([60, 35, 140])
    upper_blue = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # image & mask
    result = cv2.bitwise_and(img, img, mask=mask)
    # gray scale
    gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # canny
    min_range = 50
    max_range = 150
    edges = cv2.Canny(gray_image, min_range, max_range)

    return edges




def GetAngle(line1, line2)->int:
    """
    计算两条线段之间的夹角
    :param line1: line
    :param line2: line
    :return:
    """
    dx1 = line1[0][0] - line1[0][2]
    dy1 = line1[0][1] - line1[0][3]
    dx2 = line2[0][0] - line2[0][2]
    dy2 = line2[0][1] - line2[0][3]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180 / math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180 / math.pi)
    # print(angle2)
    if angle1 * angle2 >= 0:
        insideAngle = abs(angle1 - angle2)
    else:
        insideAngle = abs(angle1) + abs(angle2)
        if insideAngle > 180:
            insideAngle = 360 - insideAngle
    insideAngle = insideAngle % 180
    return insideAngle

def list_Direction(image,direction):
    # left，right，vertical
    white = (255, 255, 255)
    if direction[0]==1:
        cv2.putText(image, "go forward", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)

    if direction[1]==1:
        cv2.putText(image, "go forward", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)


    if direction[2]==1:
        cv2.putText(image, "go forward", (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)


def process(image):
    edges = exchange(image)
    # 最小线段的长度 50->60
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=250)
    width = image.shape[1]  # the shape is the height (0) and width (1)
    min_width = width * 0.4  # look at 10% to the left of the center
    cen_width = width // 2  # look at 10% to the left of the center
    max_width = width * 0.6  # look at 10% to the left of the center
    height = image.shape[0]  # the shape is the height (0) and width (1)
    min_height = height * 0.4  # look at 10% to the left of the center
    cen_height = height // 2  # look at 10% to the left of the center
    max_height = height * 0.6  # look at 10% to the left of the center
    # BGR colour defined
    white = (255, 255, 255)
    pink = (138, 43, 226)
    purple = (128, 0, 128)
    green = (0, 139, 0)
    gold = (37, 193, 255)
    if lines is not None:
        # 处理长度
        leng = len(lines)
    else:
        # 处理对象为None的情况
        return
    print(leng, "length")
    line_horizon = []
    line_horizon.append([0, height, width, height])

    vertical_line = []
    horizon_line = []

    inter_line = []
    inter_line.append(0)

    # left，right，vertical
    direction = [0, 0, 0]
    # junction, turn, end of line
    distance = [0, 0, 0]

    # 挑选出较为竖直的线
    # 挑选出偏水平的线

    for i in range(len(lines)):

        line1 = lines[i]
        x1, y1, x2, y2 = line1[0]
        # 创建 Point 实例表示线段端点
        p1 = point.Point(int(x1), int(y1))
        q1 = point.Point(int(x2), int(y2))
        angle = GetAngle(line1, line_horizon)
        print(angle, ": angle")
        y = min(y1, y2)
        k = (y2 - y1) * (x2 - x1)
        if (abs(angle) > 45):
            #不是弧度制，单位是°
            vertical_line.append(line.line(y, angle, p1, q1))
            if k > 0:
                text = str(90 - angle) + ": vertical offset angle"
            else:
                text = str(angle - 90) + ": vertical offset angle"
            cv2.putText(image, text, (200, 400), cv2.FONT_HERSHEY_COMPLEX, 1, purple, 1)

        if (abs(angle) < 45) & (y > min_height) & (y1 < max_height):
            if k > 0:
                angle = -angle
            horizon_line.append(line.line(0, angle, p1, q1))
            print("hengxian")

    try:
        vertical = vertical_line[0]
    except IndexError:
        return

    # justify forward traffic
    if vertical.distance > min_height:
        # 直行尽头

        distance[1] = height - vertical.distance
        distance[2] = height - vertical.distance
    else:
        # has forward
        direction[2] = 1

    # 检查线段是否相交 p1q1,p2q2
    # 画出横线的angle
    try:
        horizon = horizon_line[0]

        inter = pi.lineLineIntersection(vertical.p1, vertical.q1, horizon.p1, horizon.q1)

        # select left point and right point
        if horizon.p1.x < horizon.q1.x:
            minP = horizon.p1
            maxP = horizon.q1
        else:
            minP = horizon.q1
            maxP = horizon.p1
        #     draw

        if inter.x >= maxP.x - 15:
            direction[0] = 1
            distance[1] = height - inter.y
            cv2.line(image, (int(minP.x), int(minP.y)), (int(inter.x), int(inter.y)), green, 2)
            text = str(horizon.angle) + ": left angle"
            cv2.putText(image, text, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, green, 1)
            cv2.circle(image, (int(inter.x), int(inter.y)), 5, pink, 6)
        elif inter.x <= minP.x + 15:
            direction[1] = 1
            distance[1] = height - inter.y
            # right
            cv2.line(image, (int(maxP.x), int(maxP.y)), (int(inter.x), int(inter.y)), gold, 2)
            text = str(-horizon.angle) + ": right angle"
            cv2.putText(image, text, (400, 100), cv2.FONT_HERSHEY_COMPLEX, 1, gold, 1)
            cv2.circle(image, (int(inter.x), int(inter.y)), 5, pink, 6)
        elif (minP.x + 20 < inter.x) & (inter.x < maxP.x - 20):
            direction[0] = 1
            direction[1] = 1
            distance[0] = height - inter.y
            # left
            cv2.line(image, (int(minP.x), int(minP.y)), (int(inter.x), int(inter.y)), green, 2)
            text = str(horizon.angle) + ": left angle"
            cv2.putText(image, text, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, green, 1)
            cv2.circle(image, (int(inter.x), int(inter.y)), 5, pink, 6)
            # right
            cv2.line(image, (int(maxP.x), int(maxP.y)), (int(inter.x), int(inter.y)), gold, 2)
            text = str(-horizon.angle) + ": right angle"
            cv2.putText(image, text, (400, 100), cv2.FONT_HERSHEY_COMPLEX, 1, gold, 1)
            cv2.circle(image, (int(inter.x), int(inter.y)), 5, pink, 6)
        # distance
        if direction[2] == 0:
            # turn
            distance[1] = height - inter.y
            distance[2] = height - inter.y
        else:
            #    junction
            distance[0] = height - inter.y
        # # 判断属于 junction/turn/enf of line 以及该转点的距离
        if sum(direction) == 1:
            if direction[0]==1:
                cv2.putText(image, "left corner,it has only 1 path, left.   turning point: " + str(int(distance[1])), (5, 20),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)
            else:
                cv2.putText(image, "right corner,it has only 1 path, right.   turning point: " + str(int(distance[1])), (5, 20),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)
        elif sum(direction) == 2:
            if direction[2] == 1:
                if direction[0]==1:
                    cv2.putText(image, "a left T-junction, it has 2 paths, left and forwards.  junction:" + str(int(distance[0])), (5, 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)
                else:
                    cv2.putText(image, "a right T-junction, it has 2 paths, right and forwards.  junction:" + str(int(distance[0])), (5, 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)

            else:
                cv2.putText(image, "a terminating T-junction, it has two paths, left and right.", (5, 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)
                cv2.putText(image, "turning point:" + str(int(distance[1])), (5, 40),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)
        else:
            cv2.putText(image, "crossroads, it has 3 paths, left, forwards and right junction:" + str(int(distance[0])), (5, 20),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)
    except IndexError:
        if distance[2] != 0:
            cv2.putText(image, "end of line:    " + str(int(distance[2])), (5, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        white, 1)
        else:
            cv2.putText(image, "go forward", (5, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, white, 1)
        cv2.imshow('capture', image)
        return
    cv2.imshow('capture', image)



cv2.namedWindow("Photo_Detect")  # 定义一个窗口
cap = cv2.VideoCapture(0)  # 捕获摄像头图像  0位默认的摄像头 笔记本的自带摄像头  1为外界摄像头


def video_demo():
    i = 0
    while (True):  # 值为1不断读取图像
        ret, frame = cap.read()  # 视频捕获帧
        cv2.imshow('Photo_Detect', frame)  # 显示窗口 查看实时图像
        if i == 25:
            process(frame)
            i = 0  # 显示处理图窗口
        i = i + 1
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按Q关闭所有窗口  一次没反应的话就多按几下
            break
    # 执行完后释放窗口
    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


video_demo()


