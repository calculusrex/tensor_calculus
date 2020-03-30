import sympy as sp
import numpy as np

from sympy import cos, sin, atan, sqrt, Matrix, diff, pi


# cyllindrical system

x, y, z0 = sp.symbols('x y z0')
r, θ, z1 = sp.symbols('r θ z1')

csr = {}

csr['x'] = r*cos(θ)
csr['y'] = r*sin(θ)
csr['z0'] = z1

csr['r'] = sqrt(x**2 + y**2)
csr['θ'] = atan(y/x)
csr['z1'] = z0


# cartesian -> cyllindrical
JF = Matrix([
    [diff(csr['x'], r), diff(csr['x'], θ), diff(csr['x'], z1)],
    [diff(csr['y'], r), diff(csr['y'], θ), diff(csr['y'], z1)],
    [diff(csr['z0'], r), diff(csr['z0'], θ), diff(csr['z0'], z1)],
])
JF = JF.applyfunc(lambda x: sp.simplify(x))


# cyllindrical -> cartesian
JB = Matrix([
    [diff(csr['r'], x), diff(csr['r'], y), diff(csr['r'], z0)],
    [diff(csr['θ'], x), diff(csr['θ'], y), diff(csr['θ'], z0)],
    [diff(csr['z1'], x), diff(csr['z1'], y), diff(csr['z1'], z0)],
])
JB = JB.applyfunc(lambda x: sp.simplify(x))


# vector components to point (tuple understood by blender as point)
def v_2_p(matrix):
    x, y, z = matrix[0], matrix[1], matrix[2]
    return float(x), float(y), float(z)
    

# sympy: the arc is the angle describing the arc, 2*π will be a full circle, 3*π/2 will be three quarters, etc...
def vertex_circle__sympy(radius, vertex_number, arc, z):
    r = radius
    angles = [i * arc/vertex_number for i in range(vertex_number)]
    return [Matrix([r, α, z]) for α in angles]


# numpy: the arc is the angle describing the arc, 2*π will be a full circle, 3*π/2 will be three quarters, etc...
def vertex_circle__numpy(radius, vertex_number, arc, z):
    r = radius
    angles = [i * arc/vertex_number for i in range(vertex_number)]
    return [np.array([r, α, z]) for α in angles]


def vertical_arrow_vertices__sympy(length, cone_radius, cone_height):
    root = Matrix([0, 0, 0])
    tip = Matrix([0, 0, length])
    circle = vertex_circle__sympy(cone_radius, 16, 3*sp.pi/2,
                           length - cone_height)
    verts = [root, tip] + circle + [tip]
    return verts

def vertical_arrow_vertices__numpy(length, cone_radius, cone_height):
    root = np.array([0, 0, 0])
    tip = np.array([0, 0, length])
    circle = vertex_circle__numpy(cone_radius, 16, 3*np.pi/2,
                                  length - cone_height)
    verts = [root, tip] + circle + [tip]
    return verts


# this is a transform that rotates a vertical vector (0, 0, r) to a position given by (r, φ, θ), numeric version
def rotation_transform__numpy(φ, θ):
    return np.array([
        [np.sin(θ)*np.cos(φ), -np.sin(θ)*np.sin(φ), np.cos(θ)],
        [np.sin(φ), np.cos(φ), 0],
        [-np.cos(θ)*np.cos(φ), np.cos(θ)*np.sin(φ), np.sin(θ)]
    ]).transpose()

# this is a transform that rotates a vertical vector (0, 0, r) to a position given by (r, φ, θ), symbolic version
def rotation_transform__sympy(φ, θ):
    return sp.Matrix([
        [sp.sin(θ)*sp.cos(φ), -sp.sin(θ)*sp.sin(φ), sp.cos(θ)],
        [sp.sin(φ), sp.cos(φ), 0],
        [-sp.cos(θ)*sp.cos(φ), sp.cos(θ)*sp.sin(φ), sp.sin(θ)]
    ])

def transform_angles_from_vector__numpy(v):
    x, y, z = v[0], v[1], v[2]
    r = np.sqrt(x**2 + y**2 + z**2)
    θ = np.arctan(z/(np.sqrt(x**2 + y**2)))
    φ = np.arctan(y/x)
    return φ, θ

def transform_angles_from_vector__sympy(v):
    x, y, z = v[0], v[1], v[2]
    r = sp.sqrt(x**2 + y**2 + z**2)
    θ = sp.atan(z/(sp.sqrt(x**2 + y**2)))
    φ = sp.atan(y/x)
    return φ, θ

# the target vector should be in the default, blender, metric cartesian coordinate system
def rotation_transform_from_vector__numpy(v):
    φ, θ = transform_angles_from_vector__numpy(v)
    return rotation_transform__numpy(φ, θ)

# the target vector should be in the default, blender, metric cartesian coordinate system
def rotation_transform_from_vector__sympy(v):
    φ, θ = transform_angles_from_vector__sympy(v)
    return rotation_transform__sympy(φ, θ)

def vertex__cyllindrical_2_cartesian__sympy(v):
    x = csr['x'].subs(r, v[0]).subs(θ, v[1]).subs(z1, v[2])
    y = csr['y'].subs(r, v[0]).subs(θ, v[1]).subs(z1, v[2])
    z = csr['z0'].subs(r, v[0]).subs(θ, v[1]).subs(z1, v[2])
    return Matrix([x, y, z])

def vertex__cyllindrical_2_cartesian__numpy(v):
    r, θ, z = v[0], v[1], v[2]
    x = r * np.cos(θ)
    y = r * np.sin(θ)
    return np.array([x, y, z])


def arrow_vertices__numpy(vector, cone_radius, cone_height):
    x, y, z = vector[0], vector[1], vector[2]
    length = np.sqrt(x**2 + y**2 + z**2)
    verts = list(map(vertex__cyllindrical_2_cartesian__numpy,
                     vertical_arrow_vertices__numpy(length, cone_radius, cone_height)))
    rot_transform = rotation_transform_from_vector__numpy(vector)
    verts = list(map(lambda vert: np.matmul(rot_transform, vert),
                     verts))
    return verts
    


def arrow_vertices__float(vector, cone_radius, cone_height):
    verts = arrow_vertices__numpy(vector, cone_radius, cone_height)
    return list(map(v_2_p, verts))




if __name__ == '__main__':
    sp.init_printing()
