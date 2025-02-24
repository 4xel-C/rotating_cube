import math
import os
import time

# Perspective projection of a 3D rotating cube using rotation matrix 

# Rotation angle (A on x, B on y, and C on z)
A, B, C = 0.0, 0.0, 0.0
cubeWidth = 20
width, height = 250, 44  # screen size in character number
zBuffer = [0] * (width * height)  # will keep track of the Z value of each point to determine which point to display in 2D
buffer = [' '] * (width * height) # will recieve each character to display to the screen
distanceFromCam = 100 
K1 = 40 # scale factor
resolution = 1  # Step for the calculation of the points of the cube. Determine computed points density
horizontalOffset = 0

# determine which character to use for the background (no points)
background = " " 

# Function to calculate the new position of a point rotated using angle A, B, C
def calculateX(i, j, k):
    return j * math.sin(A) * math.sin(B) * math.cos(C) - k * math.cos(A) * math.sin(B) * math.cos(C) + \
           j * math.cos(A) * math.sin(C) + k * math.sin(A) * math.sin(C) + i * math.cos(B) * math.cos(C)

def calculateY(i, j, k):
    return j * math.cos(A) * math.cos(C) + k * math.sin(A) * math.cos(C) - \
           j * math.sin(A) * math.sin(B) * math.sin(C) + k * math.cos(A) * math.sin(B) * math.sin(C) - \
           i * math.cos(B) * math.sin(C)

def calculateZ(i, j, k):
    return k * math.cos(A) * math.cos(B) - j * math.sin(A) * math.cos(B) + i * math.sin(B)

# Calculate the 2d position of a point and update the buffers.
def calculateForSurface(cubeX, cubeY, cubeZ, ch):

    # calculate the position
    x = calculateX(cubeX, cubeY, cubeZ)
    y = calculateY(cubeX, cubeY, cubeZ)
    z = calculateZ(cubeX, cubeY, cubeZ) + distanceFromCam # apply an offset for Z not to have the camera on origin

    if z == 0:
        return

    ooz = 1 / z # perspective division

    # Calculate the position in the character array (pixel position)
    # K1 => focal length
    xp = int(width / 2 + K1 * ooz * x * 2)
    yp = int(height / 2 + K1 * ooz * y)
    
    # calculate the index in the 1D array (partionnated in segment of length width, to represent a line)
    idx = xp + yp * width
    if 0 <= idx < width * height:

        # Check if the point in on the first plane compared to other point on the same position but different depth
        if ooz > zBuffer[idx]:
            zBuffer[idx] = ooz # display only the point on the first plane
            buffer[idx] = ch 

os.system("cls" if os.name == "nt" else "clear")
while True:
    # initialize the buffers
    buffer = [background] * (width * height)
    zBuffer = [0] * (width * height)
    
    # calculate all the surface points of the cube; iterate through his width. Fix one dimension to draw the 6 faces.
    for cubeX in range(-cubeWidth, cubeWidth, int(resolution)):
        for cubeY in range(-cubeWidth, cubeWidth, int(resolution)):
            calculateForSurface(cubeX, cubeY, -cubeWidth, '@')
            calculateForSurface(cubeWidth, cubeY, cubeX, '$')
            calculateForSurface(-cubeWidth, cubeY, -cubeX, '~')
            calculateForSurface(-cubeX, cubeY, cubeWidth, '#')
            calculateForSurface(cubeX, -cubeWidth, -cubeY, ';')
            calculateForSurface(cubeX, cubeWidth, cubeY, '+')

    # replace the cursor to the beginning of the terminal, avoid clearing the whole terminal (more fluid)
    print("\x1b[H", end="")

    # Print the ASCII representation of the cube
    for k in range(width * height):

        # Break the line each time we reach the width of the screen
        if k % width == 0:
            print()
        print(buffer[k], end='')

    # increment the rotation angle (determine speed and fluidity)
    A += 0.05
    B += 0.05
    C += 0.01
    time.sleep(0.016)
