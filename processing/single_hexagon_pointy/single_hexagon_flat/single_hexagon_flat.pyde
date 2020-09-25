# pointy hexagon baby!

import math

TWO_PI = math.pi * 2
centx = 50.0
centy = 50.0
radius = 40.0
angle = TWO_PI / 6
angles = [0.0, 1.04719755, 2.0943951, 3.14159265, 4.1887902, 5.23598776]

beginShape()
for a in angles:
    vx = centx + cos(a) * radius
    vy = centy + sin(a) * radius
    vertex(vx, vy)
endShape(CLOSE)
