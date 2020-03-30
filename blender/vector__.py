import sympy as sp

from sympy import cos, sin, atan, sqrt, Matrix, diff, pi, symbols, simplify, lambdify



x, y, z = symbols('x y z')
r, φ, θ = symbols('r φ θ')

# spherical coordinate system, origin offsetted by (1, 1, 1)
test_cs = {}
test_cs['rels'] = {}
test_cs['rels']['x'] = r * cos(θ) * cos(φ)
test_cs['rels']['y'] = r * cos(θ) * sin(φ)
test_cs['rels']['z'] = r * sin(θ)
test_cs['rels']['r'] = sqrt(x**2 + y**2 + z**2)
test_cs['rels']['φ'] = atan(y/x)
test_cs['rels']['θ'] = atan(z/sqrt(x**2 + y**2))

subs_post_proc = lambda x: x

def convert_point_forward(p0):
    x_, y_, z_ = p0
    r_ = subs_post_proc(
        test_cs['rels']['r'].subs(x, x_).subs(y, y_).subs(z, z_))
    φ_ = subs_post_proc(
        test_cs['rels']['φ'].subs(x, x_).subs(y, y_).subs(z, z_))
    θ_ = subs_post_proc(
        test_cs['rels']['θ'].subs(x, x_).subs(y, y_).subs(z, z_))
    
    return r_, φ_, θ_

def convert_point_backward(p1):
    r_, φ_, θ_ = p1
    x_ = subs_post_proc(
        test_cs['rels']['x'].subs(r, r_).subs(φ, φ_).subs(θ, θ_))
    y_ = subs_post_proc(
        test_cs['rels']['y'].subs(r, r_).subs(φ, φ_).subs(θ, θ_))
    z_ = subs_post_proc(
        test_cs['rels']['z'].subs(r, r_).subs(φ, φ_).subs(θ, θ_))
    return x_, y_, z_

test_cs['convert_point_forward'] = convert_point_forward
test_cs['convert_point_backward'] = convert_point_backward

test_cs['JF'] = Matrix([
    [diff(test_cs['rels']['x'], r), diff(test_cs['rels']['x'], φ), diff(test_cs['rels']['x'], θ)],
    [diff(test_cs['rels']['y'], r), diff(test_cs['rels']['y'], φ), diff(test_cs['rels']['y'], θ)],
    [diff(test_cs['rels']['z'], r), diff(test_cs['rels']['z'], φ), diff(test_cs['rels']['z'], θ)]
]).applyfunc(simplify)
test_cs['JB'] = Matrix([
    [diff(test_cs['rels']['r'], x), diff(test_cs['rels']['r'], y), diff(test_cs['rels']['r'], z)],
    [diff(test_cs['rels']['φ'], x), diff(test_cs['rels']['φ'], y), diff(test_cs['rels']['φ'], z)],
    [diff(test_cs['rels']['θ'], x), diff(test_cs['rels']['θ'], y), diff(test_cs['rels']['θ'], z)]
]).applyfunc(simplify)




def vector_gp_verts(csys, v):
    pass


if __name__ == '__main__':
    sp.init_printing()


