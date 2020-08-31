
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math


# Initialize Vars

# Player Stuffs
px = 300
py = 300
pdx = 5
pdy = 0
pa = 1

# Radian Nonsense
pi = math.pi #pi duh
pi2 = pi/2 
pi3 = 3*pi/2
dr = 0.0174533 # One Degree in radians

# Map Nonsense
MapX = 8
MapY = 8
MapS = 64
Map = [
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 1, 0, 0, 1, 1, 1,
        1, 1, 0, 0, 0, 1, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 1,
        1, 0, 0, 0, 0, 1, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
    ]


def init():
    global pdx
    global pdy
    
    glClearColor(0.3, 0.3, 0.3, 0)
    gluOrtho2D(0, 1024, 512, 0)
    pdx = math.cos(pa) * 5
    pdy = math.sin(pa) * 5

def dist(ax, ay, bx, by, ang):
    return math.sqrt((bx - ax) * (bx - ax) + (by - ay) * (by - ay))
    
    
def drawRays2D(rays):
    global pa, px, py
    disT = 0
    ra = pa - dr * (rays/2)
    if ra < 0:
        ra += 2 * pi
    if ra > 2 * pi:
        ra -= 2 * pi
    xo = 0
    yo = 0
    
    for r in range(0, rays, 1):
        atan = -1/math.tan(ra)
        # Horizontal Lines
        dof = 0 # Depth of field
        disH = 100000
        hx = px
        hy = py
        
        if ra > pi: # If the ray is looking down 180º
            ry = ((int(py)>>6)<<6) - 0.0001
            rx = (py - ry) * atan + px
            yo = -64
            xo = -yo * atan
            
        if ra < pi: # If the ray is looking up < 180º
            ry = ((int(py)>>6)<<6) + 64
            rx = (py - ry) * atan + px
            yo = 64
            xo = -yo * atan
            
        if ra == 0 or ra == math.pi: # If the the ray is straight left or right..
            rx = px
            ry = py
            dof = 8
            
        
        while dof < 8:
            mx = (int(rx))>>6
            my = (int(ry))>>6
            mp = my * MapX + mx
            if mp > 0 and mp < len(Map) and Map[mp] == 1:  # A wall has Been Hit 
                    hx = rx
                    hy = ry
                    disH = dist(px, py, hx, hy, ra) # Calc the rays distance from the player
                    dof = 8 # End this loop
            else: # Next line
                rx += xo
                ry += yo
                dof += 1


        # Vertical Lines
        ntan = -math.tan(ra)
        dof = 0
        disV = 100000
        vx = px
        vy = py
        if ra > pi2 and ra < pi3: # If the ray is looking left
            rx = ((int(px)>>6)<<6) - 0.0001
            ry = (px - rx) * ntan + py
            xo = -64
            yo = -xo * ntan
            
        if ra < pi2 or ra > pi3: # If the ray is looking right
            rx = ((int(px)>>6)<<6) + 64
            ry = (px - rx) * ntan + px
            xo = 64
            yo = -xo * ntan
            
        if ra == 0 or ra == pi: # If the the ray is straight up or down..
            rx = px
            ry = py
            dof = 8
            
        
        while dof < 8:
            mx = (int(rx))>>6
            my = (int(ry))>>6
            mp = my * MapX + mx
            if mp > 0 and mp < len(Map) and Map[mp] == 1:  # A wall has Been Hit 
                    vx = rx
                    vy = ry
                    disV = dist(px, py, vx, vy, ra) # Calc the rays distance from the player
                    dof = 8 # End this loop
            else: # Next line
                rx += xo
                ry += yo
                dof += 1

        # Pick The Shortest ray
        if disV < disH: # Vertical
            rx = vx
            ry = vy
            disT = disV
            glColor3f(0.9, 0, 0)
        if disH < disV: # Horizontal
            rx = hx
            ry = hy
            disT = disH
            glColor3f(0.7, 0, 0)
        # Finally Draw the ray
        glLineWidth(4)
        glBegin(GL_LINES)
        glVertex2i(int(px), int(py))
        glVertex2i(int(rx), int(ry))
        glEnd()

        # 3D Walls

        # Fix Fisheye effect
        ca = pa - ra
        if ca < 0:
            ca += 2 * pi
        if ca > 2 * pi:
            ca -= 2 * pi
        disT = disT * math.cos(ca)
        # Fixed
        
        lineH = MapS * 320/disT # Line Height
        lineO = 160 - lineH/2   # Line Offset
        if lineH > 320:
            lineH = 320
        glLineWidth(8)
        glBegin(GL_LINES)
        glVertex2i(r*8 + 530, int(lineO))
        glVertex2i(r*8 + 530, int(lineH + lineO))
        glEnd()

        # Turn one degree
        ra += dr
        if ra < 0:
            ra += 2 * pi
        if ra > 2 * pi:
            ra -= 2 * pi

    

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawMap2D()
    drawPlayer()
    glutSwapBuffers()


def drawPlayer():
    # Draw a yellow square for the player
    glColor3f(1, 1, 0) 
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2i(int(px), int(py)) 
    glEnd()

    drawRays2D(60)
    
    # Draw the player's direction
    glLineWidth(3)
    glColor3f(1, 1, 0)
    glBegin(GL_LINES)
    glVertex2i(int(px), int(py))
    glVertex2i(int(px + pdx * 5), int(py + pdy * 5))
    glEnd()

    

def buttons(key, x, y):

    global px
    global py
    global pdx
    global pdy
    global pa
    
    # Player Movement --
    # Look Left
    if key == b'a':
        pa -= 0.1
        if pa < 0:
            pa += 2 * pi
        # Rotaion is like finding the pts on a unit circle
        pdx = math.cos(pa) * 5 
        pdy = math.sin(pa) * 5

    # Look Right
    if key == b'd':
        pa += 0.1
        if pa > 2 * pi:
            pa -= 2 * pi

        pdx = math.cos(pa) * 5 
        pdy = math.sin(pa) * 5

    if key == b'w':
        px += pdx
        py += pdy
    if key == b's':
        px -= pdx
        py -= pdy

    # Exit key
    if key == b'\x1b':
        glutDestroyWindow ( window );
##    print(key)
    glutPostRedisplay()


    
def drawMap2D():
    y = 0
    for y in range(0, MapY, 1):
        for x in range(0, MapX, 1):
            xo = x * MapS
            yo = y * MapS
            if Map[y * MapX + x] == 1:
                glColor3f(1,1,1)
            else:
                glColor3f(0,0,0)

            # Create the tile (a square)
            glBegin(GL_QUADS)
            glVertex2i(xo + 1, yo + 1)
            glVertex2i(xo + 1, yo + MapS - 1)
            glVertex2i(xo + MapS - 1, yo + MapS - 1)
            glVertex2i(xo + MapS -1, yo + 1)
            glEnd()

            x += 1
        y += 1



glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(1024, 512)
window = glutCreateWindow("Raymania")
init()
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(buttons)
glutMainLoop()


