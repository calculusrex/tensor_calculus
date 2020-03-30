import sympy as sp
import numpy as np
import functools as ft
sp.init_printing()

from sympy import Eq, symbols, solve, Matrix, diff, pi, sqrt, cos, sin, atan
from sympy import simplify as symp

x0, y0, z0 = symbols('x0 y0 z0')
x1, y1, z1 = symbols('x1 y1 z1')


# The expressions linking the coordinate systems
# These two coordinate systems are both cartesian, but the second one is scaled by 4 on all axes and it's origin is offseted by (10, 3, -5)

coordinate_system_link = {}

coordinate_system_link['x1'] = x0 * cos(pi/4)
coordinate_system_link['y1'] = y0 * sin(pi/4)
coordinate_system_link['z1'] = z0

coordinate_system_link['x0'] = solve(
    Eq(coordinate_system_link['x1'], x1),
    x0)[0]
coordinate_system_link['y0'] = solve(
    Eq(coordinate_system_link['y1'], y1),
    y0)[0]
coordinate_system_link['z0'] = solve(
    Eq(coordinate_system_link['z1'], z1),
    z0)[0]

csl = coordinate_system_link

def convert_point_forward(p0):
    x0_, y0_, z0_ = p0
    x1_ = csl['x1'].subs(x0, x0_).subs(y0, y0_).subs(z0, z0_)
    y1_ = csl['y1'].subs(x0, x0_).subs(y0, y0_).subs(z0, z0_)
    z1_ = csl['z1'].subs(x0, x0_).subs(y0, y0_).subs(z0, z0_)
    return x1_, y1_, z1_

# The points at which we'll convert representations
A0 = (1, 1, 1)
B0 = (0, 0, 2)
C0 = (symp(1)/2, 10, -10)

A1 = convert_point_forward(A0)
B1 = convert_point_forward(B0)
C1 = convert_point_forward(C0)


# The tensors to represent in the new coordinate system

# vectors:
v0 = Matrix([1, 1, 1])
w0 = Matrix([0, 0, 1])
s0 = Matrix([symp(1)/2, 3, sqrt(2)])

# covectors:
α0 = Matrix([1, 4, symp(1)/2]).transpose()
β0 = Matrix([1, 1, 1]).transpose()

# linear maps:
L0 = s0 * α0

# the metric tensor
g0 = sp.eye(3)

# The jacobian matrices, JF is the forward jacobian and JB is the inverse jacobian

JF = Matrix([
    [diff(csl['x0'], x1), diff(csl['x0'], y1), diff(csl['x0'], z1)],
    [diff(csl['y0'], x1), diff(csl['y0'], y1), diff(csl['y0'], z1)],
    [diff(csl['z0'], x1), diff(csl['z0'], y1), diff(csl['z0'], z1)],
])

JB = Matrix([
    [diff(csl['x1'], x0), diff(csl['x1'], y0), diff(csl['x1'], z0)],
    [diff(csl['y1'], x0), diff(csl['y1'], y0), diff(csl['y1'], z0)],
    [diff(csl['z1'], x0), diff(csl['z1'], y0), diff(csl['z1'], z0)],
])



def jacobians_at_point(JF, JB, p0, p1):
    x0_, y0_, z0_ = p0
    x1_, y1_, z1_ = p1
    JF = JF.applyfunc(lambda elem: elem.subs(x1, x1_).subs(y1, y1_).subs(z1, z1_))
    JB = JB.applyfunc(lambda elem: elem.subs(x0, x0_).subs(y0, y0_).subs(z0, z0_))
    return JF, JB


F, B = jacobians_at_point(JF, JB, A0, A1)

# the vector representations in the new coordinate basis:

# vectors:
v1 = B * v0
w1 = B * w0
s1 = B * s0

# covectors:
α1 = α0 * F
β1 = β0 * F

# linear maps:
L1 = B * L0 * F

# metric tensor:
g1 = F.transpose() * g0 * F
