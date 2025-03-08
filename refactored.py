import math
import os

# ---------------------------- Configuration properties

# dimension of the screen
width = 150
height = 40

# rotation angle speed
A = 0                  # (rotation around X)
B = 0                  # (rotation around Y)  
C = 0                  # (rotation around Z)

# cube width
cube_width = 15             # 20 characters

distance_from_camera = 100  # distance from the origin
K1 = 40                     # scale factor (field of view)
aspect_ratio = 2            # Ratio to compensate the letter beeing higher than wider
resolution = 1              # number of 3D point calculated before the projection

# ------------------------------------------------------


# Function to calculate the new position of a point rotated using angle A, B, C
def calculateX(i, j, k):
    return (
        j * math.sin(A) * math.sin(B) * math.cos(C)
        - k * math.cos(A) * math.sin(B) * math.cos(C)
        + j * math.cos(A) * math.sin(C)
        + k * math.sin(A) * math.sin(C)
        + i * math.cos(B) * math.cos(C)
    )


def calculateY(i, j, k):
    return (
        j * math.cos(A) * math.cos(C)
        + k * math.sin(A) * math.cos(C)
        - j * math.sin(A) * math.sin(B) * math.sin(C)
        + k * math.cos(A) * math.sin(B) * math.sin(C)
        - i * math.cos(B) * math.sin(C)
    )


def calculateZ(i, j, k):
    return (
        k * math.cos(A) * math.cos(B) - j * math.sin(A) * math.cos(B) + i * math.sin(B)
    )


def calculate_2D_coordinates(x, y, z):
    """
    Calculate the 2D projection coordinates of a 3d point.
    Take the int value to have a round coordinate to map on an array.
    Return the coordinate x, y
    """

    # if z already on the plan, return x and y as there is no projection needed
    if z == 0:
        return x, y
    
    # get distance from camera
    z = z + distance_from_camera

    ooz = 1 / z  # perspective division

    plan_x = int(round((aspect_ratio * K1 * ooz * x + width / 2), 0))
    plan_y = int(round((K1 * ooz * y + height/2), 0))

    return plan_x, plan_y

def calculate_rotated_coordinates(x, y, z):
    """
    Calculate the new 3D coordinates of a point after applying rotation angle on X, Y, Z
    """
    new_x = calculateX(x, y, z)
    new_y = calculateY(x, y, z)
    new_z = calculateZ(x, y, z)

    return (new_x, new_y, new_z)


if __name__ == "__main__":

    os.system("cls" if os.name == "nt" else "clear")
    while True:

        # get the 3D coordinates of all the points faces of the cube stored as well as their symbol (x, y, z, symbol). Queue data structure to update it on  each iteration
        coordinates = []

        for i in range(-cube_width, + cube_width, resolution):
            for j in range(-cube_width, + cube_width, resolution):
                coordinates.append((i, j, cube_width, "#"))      # front face
                coordinates.append((i, j, -cube_width, "%"))     # back face
                coordinates.append((cube_width, i, j, "$"))     # left face
                coordinates.append((cube_width, i, j, "£"))      # right face
                coordinates.append((i, cube_width, j, "%"))      # top face
                coordinates.append((i, -cube_width, j, "@"))  # bottom face

        # 1D array containing the character to print as well as their orginal depth
        screen = [(' ', -math.inf)] * width * height

        for i in range(len(coordinates)):
            x, y, z, symbol = coordinates[i]

            newx, newy, newz = calculate_rotated_coordinates(x, y, z)

            plan_x, plan_y= calculate_2D_coordinates(newx, newy, newz)

            index = int(plan_x + (width*plan_y))

            if not 0 < index < width * height:
                continue

            # update the screen symbol if the point is closest to the camera than the previous one
            if screen[index][1] < z:
                screen[index] = (symbol, z)
        
        # replace the cursor to the beginning of the terminal, avoid clearing the whole terminal (more fluid)
        print("\x1b[H", end="")

        # print the screen
        for i in range(width * height):
            print(screen[i][0], end="")
            
            if i % width == 0:
                print()
        
        # update the rotation angles
        A += 0.03
        B += 0.03
        C += 0.005

