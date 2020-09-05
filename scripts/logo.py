#!/usr/bin/env python3

import itertools
import numpy as np

import drawSvg as draw

DEG2RAD = 2 * np.pi / 360

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

phi = DEG2RAD * np.array([24, 45, 0])
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
    return tuple(pts[i] for i in inds)

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

rdf = square(r_points, [0, 1, 5, 4])
rf = square(r_points, [4, 5, 9, 8])
ruf = square(r_points, [8, 9, 13, 12])
rd = square(r_points, [1, 2, 6, 5])
rc = square(r_points, [5, 6, 10, 9])
ru = square(r_points, [9, 10, 14, 13])
rdb = square(r_points, [2, 3, 7, 6])
rb = square(r_points, [6, 7, 11, 10])
rub = square(r_points, [10, 11, 15, 14])

squares = [ufl, uf, ufr, ul, uc, ur, ubl, ub, ubr, fdl, fd, fdr, fl, fc, fr, ful, fu, fur, rdf, rf, ruf, rd, rc, ru, rdb, rb, rub]

silver = '#c0c0cf'
black = '#000000'
white = '#ffffff'

square_colors = {sq : black for sq in squares}
square_colors.update({sq : silver for sq in [fdl, fd, fc, fu, fur, rdf, rd, rc, ru, rub]})

def line_is_visible(pt1, pt2):
    good = False
    good |= u_face(pt1) and u_face(pt2)
    good |= f_face(pt1) and f_face(pt2)
    good |= r_face(pt1) and r_face(pt2)
    good |= (u_face(pt1) and f_face(pt2)) or (f_face(pt1) and u_face(pt2))
    good |= (u_face(pt1) and r_face(pt2)) or (r_face(pt1) and u_face(pt2))
    return good

def extend_line(pt1, pt2, c = 1.0):
    pt1 = np.array(pt1)
    pt2 = np.array(pt2)
    v = pt2 - pt1
    return (pt1 + ((c + 1) / 2) * v, pt1 - (c - 1) * v / 2)

c = 1.0

lines = [extend_line(*pair, c = c) for pair in itertools.combinations(cube_grid, 2) if (sum((i1 == i2) for (i1, i2) in zip(*pair)) == 2) and line_is_visible(*pair)]

def is_top_point(pt):
    return (pt[1] == 3) and (pt[2] != -3) and (pt[0] != 3)

line_width = 0.22
top_line_width_scale = 0.75

# def is_outer_



if __name__ == '__main__':


    # arr = [-3, -1, 1, 3]
    # grid = list(itertools.product(arr, arr, arr))
    # edges = []
    # for pair in itertools.combinations(grid, 2):
    #     if sum((i1 == i2) for (i1, i2) in zip(*pair)) == 2:
    #         edges.append(pair)

    d = draw.Drawing(10, 10, origin = 'center')

    yshift = np.array([0, 0.3])

    d.append(draw.Rectangle(-100, -100, 200, 200, stroke_width = 0, fill = '#ff0000'))

    for (sq, color) in square_colors.items():
        points = [project(pt) + yshift for pt in sq]
        d.append(draw.Lines(*(x for pt in points for x in pt), close = True, fill = color, stroke_width = 0))

    for line in lines:
        stroke_width = line_width
        if is_top_point(line[0]) or is_top_point(line[1]):
            stroke_width *= top_line_width_scale
        points = [project(pt) + yshift for pt in line]
        d.append(draw.Line(*(x for pt in points for x in pt), stroke = white, stroke_width = stroke_width))


    d.setPixelScale(100)
    d.saveSvg('logo.svg')
    d.savePng('logo.png')