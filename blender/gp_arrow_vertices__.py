import sympy as sp
import numpy as np


# vector components to point (tuple understood by blender as point)
def v_2_p(matrix):
    x, y, z = matrix[0], matrix[1], matrix[2]
    return float(x), float(y), float(z)

# numpy: the arc is the angle describing the arc, 2*π will be a full circle, 3*π/2 will be three quarters, etc...
def vertex_circle__numpy(radius, vertex_number, arc, z):
    r = radius
    angles = [i * arc/vertex_number for i in range(vertex_number)]
    return [np.array([r, α, z]) for α in angles]

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

def φ_from_xy(x, y):
    if (x >= 0 and y >= 0) or (x >= 0 and y <= 0): # quadrants 1 & 2
        return np.arctan(y/x)
    else:
        return np.pi + np.arctan(y/x)

def ants(angle):
    return sp.pi*(angle/np.pi)

def transform_angles_from_vector__numpy(v):
    x, y, z = v[0], v[1], v[2]
    r = np.sqrt(x**2 + y**2 + z**2)
    print('r: ', r)
    θ = np.arctan(z/(np.sqrt(x**2 + y**2)))
    print('θ: ', ants(θ))
    φ = φ_from_xy(x, y)
    print('φ: ', ants(φ))
    return φ, θ

# the target vector should be in the default, blender, metric cartesian coordinate system
def rotation_transform_from_vector__numpy(v):
    φ, θ = transform_angles_from_vector__numpy(v)
    return rotation_transform__numpy(φ, θ)

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
    pass
