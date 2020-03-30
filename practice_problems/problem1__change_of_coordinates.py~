import sympy as sp
import numpy as np
import functools as ft

from sympy import sin, cos, pi, Eq, sqrt, atan, Matrix, diff

sp.init_printing()

symp = sp.simplify    

# Coordinate system variables
x, y = sp.symbols('x, y')
r, θ = sp.symbols('r θ')

# Vectors
vc = Matrix(
    [1, 1])
wp = Matrix(
    [1, pi/2])
uc = Matrix(
    [-1, 0])
ap = Matrix(
    [-2, pi/3])

# Covectors
αc = Matrix(
    [symp(1)/2, symp(1)/2]).transpose()

βc = Matrix(
    [-1, 2]).transpose()

# Linear Map
Lc = Matrix(
    [[-1, 0],
     [0, 1]])

# Metric Tensor
gc = Matrix(
    [[1, 0],
     [0, 1]])

# coordinate relationships:

coord_rel = {}

coord_rel['x'] = r * cos(θ)

coord_rel['y'] = r * sin(θ)

coord_rel['r'] = sqrt(x**2 + y**2)

coord_rel['θ'] = atan(y/x)

# def cartesian_to_polar__point(x0, y0):
#     r1 = coord_rel['r'].subs(x, x0).subs(y, y0)
#     θ1 = coord_rel['θ'].subs(x, x0).subs(y, y0)
#     return r1, θ1

# points in which to compute the coordinate basis and the change of coordinates for the tensors:
Ac, Bc, Cc = (1, 0), (0, 1), (-1, -1)
Ap = (1, 0)
Bp = (1, pi/2)
Cp = (sqrt(2), 5*pi/4)

J = Matrix(
    [
        [diff(coord_rel['x'], r), diff(coord_rel['x'], θ)],
        [diff(coord_rel['y'], r), diff(coord_rel['y'], θ)],
    ]
)

Jinv = Matrix(
    [
        [diff(coord_rel['r'], x), diff(coord_rel['r'], y)],
        [diff(coord_rel['θ'], x), diff(coord_rel['θ'], y)],
    ]
)

# Jinv = Jinv.applyfunc(lambda x: symp(x))

def transforms_from_jacobians_at_point(j, jinv, point_c, point_p):
    x0, y0 = point_c
    r0, θ0 = point_p

    F = J.applyfunc(
        lambda comp: comp.subs(r, r0).subs(θ, θ0))
    B = Jinv.applyfunc(
        lambda comp: comp.subs(x, x0).subs(y, y0))

    return F, B

F, B = transforms_from_jacobians_at_point(J, Jinv, Cc, Cp)

vp = B * vc
wc = F * wp
up = B * uc
ac = F * ap

Lp = B * Lc * F

αp = αc * F
βp = βc * F


factors = [(F, ('k', 'i')), (F, ('l', 'j')), (gc, ('k', 'l'))]

def replace_index_with(factors, index, i):
    replaced = []
    for matrix, (k, l) in factors:
        m, n = k, l
        if k == index:
            m = i
        if l == index:
            n = i
        replaced.append((matrix, (m, n)))
    return replaced

def expand_on_index(factors, index, n):
    expanded = []
    for i in range(n):
        expanded.append(replace_index_with(factors, index, i))
    return expanded

def indexed_element(factor):
    matrix, (i, j) = factor
    matrix = np.array(matrix)
    return matrix[i][j]

def indices_from_factors(factors):
    indices = set()
    for matrix, (i, j) in factors:
        if isinstance(i, str):
            indices.add(i)
        if isinstance(j, str):
            indices.add(j)
    return indices

def counted_indices_from_factors(factors):
    indices = indices_from_factors
    counts = {}
    for i in indices:
        counts[i] = 0
    for matrix, (i, j) in factors:
        if i in counts.keys():
            counts[i] += 1
        if j in counts.keys():
            counts[j] += 1
    return counts


def no_symbollic_index(factors):
    return len(
        indices_from_factors(factors)) == 0

def sum_over__rec(factors):
    if no_symbollic_index(factors):
        return sum(map(indexed_element, factors))
    else:
        indices = indices_from_factors(factors)
        return sum(
            map(sum_over__rec,
                expand_on_index(factors,
                                indices.pop(),
                                2)))

def sum_over(factors, out_matrix_indices):
    i0, j0 = out_matrix_indices
    mat = sp.eye(2)
    for i in range(2):
        for j in range(2):
            mat[i, j] = sum_over__rec(
                replace_index_with(
                    replace_index_with(factors, j0, j),
                    i0,
                    i))
    return mat
    
    

# def index_combinations(dim):
#     return ft.reduce(lambda a, b: a + b,
#                      [[(i, j) for j in range(dim)] for i in range(dim)])


# gp = eye(2)
# for i, j in index_combinations(2):
#     gp[i, j] = sum(
#         map(lambda ixs:)
#     )
