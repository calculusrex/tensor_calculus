import sympy as sp
import numpy as np
import functools as ft
sp.init_printing()

from sympy import Eq, symbols, solve, Matrix, diff, pi, sqrt, cos, sin, atan
from sympy import simplify as symp


x, y, z = symbols('x y z')
r, φ, θ = symbols('r φ θ')

# The expressions linking the coordinate systems
# These two coordinate systems are both cartesian, but the second one is scaled by 4 on all axes and it's origin is offseted by (10, 3, -5)

coordinate_system_link = {}

coordinate_system_link['x'] = r*cos(θ) * cos(φ)
coordinate_system_link['y'] = r*cos(θ) * sin(φ)
coordinate_system_link['z'] = r * sin(θ)

coordinate_system_link['r'] = sqrt(x**2 + y**2 + z**2)
coordinate_system_link['φ'] = atan(y/x)
coordinate_system_link['θ'] = atan(z / (sqrt(x**2 + y**2)))

csl = coordinate_system_link

def convert_point_forward(p0):
    x_, y_, z_ = p0
    r_ = symp(
        csl['r'].subs(x, x_).subs(y, y_).subs(z, z_))
    φ_ = symp(
        csl['φ'].subs(x, x_).subs(y, y_).subs(z, z_))
    θ_ = symp(
        csl['θ'].subs(x, x_).subs(y, y_).subs(z, z_))
    return r_, φ_, θ_


def convert_point_backward(p1):
    r_, φ_, θ_ = p1
    x_ = symp(
        csl['x'].subs(r, r_).subs(φ, φ_).subs(θ, θ_))
    y_ = symp(
        csl['y'].subs(r, r_).subs(φ, φ_).subs(θ, θ_))
    z_ = symp(
        csl['z'].subs(r, r_).subs(φ, φ_).subs(θ, θ_))
    return x_, y_, z_


# The points at which we'll convert representations
A0 = (1, 1, 1)
B0 = (0, 0, 1)
C0 = (1/4, 1/4, sqrt(2)/4)
D0 = (1/8, 2, 1/16)

E1 = (1, pi/6, 3*pi/4)
F1 = (1, 5*pi/4, 3*pi/4)

A1 = convert_point_forward(A0)
B1 = convert_point_forward(B0)
C1 = convert_point_forward(C0)
D1 = convert_point_forward(D0)

E0 = convert_point_backward(E1)
F0 = convert_point_backward(F1)


# The tensors to represent in the new coordinate system

# vectors:
v0 = Matrix([1, 1, 1])
w0 = Matrix([0, 0, 1])
s1 = Matrix([1, 0, 0])
t1 = Matrix([0, 0, 1])

# covectors:
α0 = Matrix([1, 4, symp(1)/2]).transpose()
β0 = Matrix([1, 1, 1]).transpose()

# linear maps:
L0 = Matrix([
    [9, 2, 3],
    [8, 1, 4],
    [7, 6, 5]
])

# the metric tensor
g0 = sp.eye(3)

# The jacobian matrices, JF is the forward jacobian and JB is the inverse jacobian

JF = Matrix([
    [diff(csl['x'], r), diff(csl['x'], φ), diff(csl['x'], θ)],
    [diff(csl['y'], r), diff(csl['y'], φ), diff(csl['y'], θ)],
    [diff(csl['z'], r), diff(csl['z'], φ), diff(csl['z'], θ)],
])

JB = Matrix([
    [diff(csl['r'], x), diff(csl['r'], y), diff(csl['r'], z)],
    [diff(csl['φ'], x), diff(csl['φ'], y), diff(csl['φ'], z)],
    [diff(csl['θ'], x), diff(csl['θ'], y), diff(csl['θ'], z)],
])



def jacobians_at_point(JF, JB, p0, p1):
    x_, y_, z_ = p0
    r_, φ_, θ_ = p1
    JF = JF.applyfunc(lambda elem: elem.subs(r, r_).subs(φ, φ_).subs(θ, θ_))
    JB = JB.applyfunc(lambda elem: elem.subs(x, x_).subs(y, y_).subs(z, z_))
    return JF, JB


F, B = jacobians_at_point(JF, JB, A0, A1)

# the vector representations in the new coordinate basis:

# vectors:
v1 = B * v0
w1 = B * w0
s0 = F * s1
t0 = F * t1

# covectors:
α1 = α0 * F
β1 = β0 * F

# linear maps:
L1 = B * L0 * F

# metric tensor:
g1 = F.transpose() * g0 * F



if __name__ == '__main__':
    print('problem 4, cartesian to spherical')
