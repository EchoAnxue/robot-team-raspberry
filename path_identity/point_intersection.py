# Python program to find the point of
# intersection of two lines

# Class used to used to store the X and Y
# coordinates of a point respectively
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Method used to display X and Y coordinates
    # of a point
    def displayPoint(self, p):
        print(f"({p.x}, {p.y})")


def lineLineIntersection(A, B, C, D):
    # Line AB represented as a1x + b1y = c1
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1 * (A.x) + b1 * (A.y)

    # Line CD represented as a2x + b2y = c2
    a2 = D.y - C.y
    b2 = C.x - D.x
    c2 = a2 * (C.x) + b2 * (C.y)

    determinant = a1 * b2 - a2 * b1

    if (determinant == 0):
        # The lines are parallel. This is simplified
        # by returning a pair of FLT_MAX
        return Point(10 ** 9, 10 ** 9)
    else:
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        return Point(x, y)


def calculate_midpoint(points):
    if not points:
        return None  # 如果没有点，则返回 None

    total_x = 0
    total_y = 0

    # 计算所有点的 x 和 y 坐标之和
    for point in points:
        total_x += point.x
        total_y += point.y

    # 计算平均值得到中点坐标
    midpoint_x = total_x / len(points)
    midpoint_y = total_y / len(points)

    return Point(midpoint_x, midpoint_y)



# Driver code
A = Point(1, 1)
B = Point(4, 1)
C = Point(8, 1)
D = Point(10, 1)

intersection = lineLineIntersection(A, B, C, D)

if (intersection.x == 10**9 and intersection.y == 10**9):
	print("The given lines AB and CD are parallel.")
else:
	# NOTE: Further check can be applied in case
	# of line segments. Here, we have considered AB
	# and CD as lines
	print("The intersection of the given lines AB " + "and CD is: ")
	intersection.displayPoint(intersection)


# This code is contributed by Saurabh Jaiswal
