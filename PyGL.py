

import pygame
import math as M
import time as T
import threading
import concurrent.futures

print("running")


PlotColour = (240, 240, 240)
BackgroundColour = (40, 40, 40)

Width = 600
Height = 500

Scale = 1
Displacement = 0

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Plot')
screen.fill(BackgroundColour)

P1 = (500, 500)
P2 = (200, 200)

def Distance(P0, P1):
    P0x, P0y = P0
    P1x, P1y = P1

    Dy = ( P0y - P1y )
    Dx = ( P0x - P1x )
    Dy = Dy ** 2
    Dx = Dx ** 2
    Dist = M.sqrt( Dy + Dx )
    return Dist

def Gradient(P0, P1):
    P0x, P0y = P0
    P1x, P1y = P1
     
    Dy = ( P1y - P0y )
    Dx = ( P1x - P0x )
    return Dy, Dx

def PLerp(Start, Range, Increment, Distance):
    Inc = Increment * (1/Range) * Distance
    Point = Start + Inc
    return Point

def Lerp(P1, P2, C1, C2):
    P1x, P1y = P1
    P2x, P2y = P2
    R1, G1, B1 = C1
    R2, G2, B2 = C2

    D = M.ceil(Distance(P1, P2))
    Dy, Dx = Gradient(P1, P2)
    DR = (R2-R1)
    DG = (G2-G1)
    DB = (B2-B1)

    for i in range(D):
        x = int(PLerp(P1x, D, i, Dx))
        y = int(PLerp(P1y, D, i, Dy))
        r = abs(int(PLerp(R1, D, i, DR)))
        g = abs(int(PLerp(G1, D, i, DG)))
        b = abs(int(PLerp(B1, D, i, DB)))
        if r >= 255:
            r = 255
        if g >= 255:
            g = 255
        if b >= 255:
            b = 255

        screen.set_at( (x, y) , (r, g, b) )

def PlotTri(V1, V2, V3):
    P1, C1 = V1
    P2, C2 = V2
    P3, C3 = V3

    # Access pool

    LerpPool.submit(Lerp( P1, P2, C1, C2))
    LerpPool.submit(Lerp( P2, P3, C2, C3))
    LerpPool.submit(Lerp( P3, P1, C3, C1))

#    Lerp( P1, P2, C1, C2)
#    Lerp( P2, P3, C2, C3)
#    Lerp( P3, P1, C3, C1)




# Create Thread pool

LerpPool = concurrent.futures.ThreadPoolExecutor(max_workers = 3)
TriPool = concurrent.futures.ThreadPoolExecutor(max_workers = 64)

VertexPool=[
    ((0,0),(255, 0, 0)),
    ((500, 100),(127, 127, 0)),
    ((250, 300),(0,256,0)),
    ((550,350),(0,127,127)),
    ((50, 350),(0,0,255)),
    ((500, 450),(127,0,127))
    ]

for i in range(len(VertexPool)):
    print(VertexPool[i])
    P, C = VertexPool[i]
    print(P,C)

L = 0
Time = 0
while True:
    S = T.perf_counter()
    for i in range(len(VertexPool)):
        P, C = VertexPool[i]
        TriPool.submit(PlotTri((VertexPool[i-2]),(VertexPool[i-1]),(VertexPool[i])))

#    PlotTri(
#        ( ((0, 0),(255,0,0)) ),
#        ( ((50, 50),(0,255,0)) ),
#        ( ((0, 85),(0,0,255)) )
#        )

    pygame.display.flip()
    print("flipped")

    E = T.perf_counter()
    D = E - S
    Time = Time + D
    L = L + 1
    Mean = Time / L
    print((1000*D), "milliseconds")
    print((1000*Mean), "mean milliseconds")
    T.sleep(1)
