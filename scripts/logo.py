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
border_gray = '#777777'

square_colors = {sq : black for sq in squares}
square_colors.update({sq : silver for sq in [fdl, fd, fc, fu, fur, rdf, rd, rc, ru, rub]})

square_factor = 0.86

plane_factor = 1.04
delta = 3 * (plane_factor - 1)

u_plane = [(-3 - delta, 3, -3), (-3 - delta, 3, 3 + delta), (3, 3, 3 + delta), (3, 3, -3)]
f_plane = [(-3 - delta, -3 - delta, -3), (-3 - delta, 3, -3), (3, 3, -3), (3, -3 - delta, -3)]
r_plane = [(3, -3 - delta, -3), (3, 3, -3), (3, 3, 3 + delta), (3, -3 - delta, 3 + delta)]

def centroid(points):
    arr = np.array(points)
    return arr.sum(axis = 0) / len(points)

def scale(pt, anchor, factor = 1.0):
    anchor = np.array(anchor)
    v = np.array(pt) - anchor
    return anchor + factor * v

def scale_polygon(points, factor = 1.0):
    center = centroid(points)
    return [scale(pt, center, factor = factor) for pt in points]

yshift = np.array([0, 0.32])

def project_polygon(points):
    return [project(pt) + yshift for pt in points]

def draw_polygon2D(points, **kwargs):
    return draw.Lines(*(x for pt in points for x in pt), close = True, **kwargs)

def draw_polygon(points, **kwargs):
    return draw_polygon2D(project_polygon(points), **kwargs)

border_factor = 1.015
border_points = u_plane[:3] + [r_plane[3], r_plane[0]] + [f_plane[0]]
border_points = scale_polygon(project_polygon(border_points), factor = border_factor)


if __name__ == '__main__':


    d = draw.Drawing(9.4, 9.4, origin = 'center')

    # draw outer border
    d.append(draw_polygon2D(border_points, fill = border_gray))

    # draw white planes
    for sq in [u_plane, f_plane, r_plane]:
        d.append(draw_polygon(sq, fill = white))

    for (sq, color) in square_colors.items():
        # draw outer squares
        d.append(draw_polygon(sq, fill = white, stroke_width = 0))

        # draw inner squares
        inner_points = scale_polygon(sq, factor = square_factor)
        d.append(draw_polygon(inner_points, fill = color, stroke_width = 0))

    d.setPixelScale(100)
    d.saveSvg('logo.svg')
    d.savePng('logo.png')