# pointy hexagon baby!

import math

TWO_PI = math.pi * 2
centx = 50.0
centy = 50.0
radius = 40.0
angle = TWO_PI / 6
angles = [0.52359878, 1.57079633, 2.61799388, 3.66519143, 4.71238898, 5.75958653]

beginShape()
for a in angles:
    vx = centx + cos(a) * radius
    vy = centy + sin(a) * radius
    vertex(vx, vy)
endShape(CLOSE)
