#!/usr/bin/env python3

import itertools
import numpy as np

import drawSvg as draw

DEG2RAD = 2 * np.pi / 360

alpha = np.arcsin(np.sqrt(3)/3)
beta = np.pi / 4

camera_pos = np.array([0, 0, -40])
surface_pos = np.array([0, 0, 40])
theta = np.array([0, 0, 0])

def Rx(t):
    return np.array([[1, 0, 0], [0, np.cos(t), np.sin(t)], [0, -np.sin(t), np.cos(t)]])

def Ry(t):
    return np.array([[np.cos(t), 0, np.sin(t)], [0, 1, 0], [-np.sin(t), 0, np.cos(t)]])

def Rz(t):
    return np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])


A = np.array([[1, 0, 0], [0, np.cos(theta[0]), np.sin(theta[0])], [0, -np.sin(theta[0]), np.cos(theta[0])]])
B = np.array([[np.cos(theta[1]), 0, -np.sin(theta[1])], [0, 1, 0], [np.sin(theta[1]), 0, np.cos(theta[1])]])
C = np.array([[np.cos(theta[2]), np.sin(theta[2]), 0], [-np.sin(theta[2]), np.cos(theta[2]), 0], [0, 0, 1]])
D = np.array([[1, 0, surface_pos[0] / surface_pos[2]], [0, 1, surface_pos[1] / surface_pos[2]], [0, 0, 1 / surface_pos[2]]])

phi = DEG2RAD * np.array([22, 45, 0])
rx = Rx(phi[0])
ry = Ry(phi[1])
rz = Rz(phi[2])

def project(pt):
    pt2 = rx @ (ry @ pt)
    f = D @ (A @ (B @ (C @ (np.array(pt2) - camera_pos))))
    bx = f[0] / f[2]
    by = f[1] / f[2]
    return (bx, by)

r_face = lambda pt : pt[0] == 3
l_face = lambda pt : pt[0] == -3
u_face = lambda pt : pt[1] == 3
d_face = lambda pt : pt[1] == -3
b_face = lambda pt : pt[2] == 3
f_face = lambda pt : pt[2] == -3

arr = [-3, -1, 1, 3]
cube_grid = list(itertools.product(arr, arr, arr))

u_points = list(filter(u_face, cube_grid))
f_points = list(filter(f_face, cube_grid))
r_points = list(filter(r_face, cube_grid))

def square(pts, inds):
    return [pts[i] for i in inds]

ufl = square(u_points, [0, 1, 5, 4])
uf = square(u_points, [4, 5, 9, 8])
ufr = square(u_points, [8, 9, 13, 12])
ul = square(u_points, [1, 2, 6, 5])
uc = square(u_points, [5, 6, 10, 9])
ur = square(u_points, [9, 10, 14, 13])
ubl = square(u_points, [2, 3, 7, 6])
ub = square(u_points, [6, 7, 11, 10])
ubr = square(u_points, [10, 11, 15, 14])

fdl = square(f_points, [0, 1, 5, 4])
fd = square(f_points, [4, 5, 9, 8])
fdr = square(f_points, [8, 9, 13, 12])
fl = square(f_points, [1, 2, 6, 5])
fc = square(f_points, [5, 6, 10, 9])
fr = square(f_points, [9, 10, 14, 13])
ful = square(f_points, [2, 3, 7, 6])
fu = square(f_points, [6, 7, 11, 10])
fur = square(f_points, [10, 11, 15, 14])

rdf = square(f_points, [0, 1, 5, 4])
rf = square(f_points, [4, 5, 9, 8])
ruf = square(f_points, [8, 9, 13, 12])
rd = square(f_points, [1, 2, 6, 5])
rc = square(f_points, [5, 6, 10, 9])
ru = square(f_points, [9, 10, 14, 13])
rdb = square(f_points, [2, 3, 7, 6])
rb = square(f_points, [6, 7, 11, 10])
rub = square(f_points, [10, 11, 15, 14])



if __name__ == '__main__':

    arr = [-3, -1, 1, 3]
    grid = list(itertools.product(arr, arr, arr))
    edges = []
    for pair in itertools.combinations(grid, 2):
        if sum((i1 == i2) for (i1, i2) in zip(*pair)) == 2:
            edges.append(pair)

    d = draw.Drawing(15, 15, origin = 'center')
    for (pt1, pt2) in edges:
        good = False
        good |= u_face(pt1) and u_face(pt2)
        good |= f_face(pt1) and f_face(pt2)
        good |= r_face(pt1) and r_face(pt2)
        good |= (u_face(pt1) and f_face(pt2)) or (f_face(pt1) and u_face(pt2))
        good |= (u_face(pt1) and r_face(pt2)) or (r_face(pt1) and u_face(pt2))
        if good:
            p1 = project(pt1)
            p2 = project(pt2)
            # p1 = tuple(np.dot(proj_iso, np.array(pt1)))[:2]
            # p2 = tuple(np.dot(proj_iso, np.array(pt2)))[:2]
            d.append(draw.Line(*(p1 + p2), stroke = 'black', stroke_width = 0.1))

    d.setPixelScale(100)
    d.saveSvg('logo.svg')
    d.savePng('logo.png')