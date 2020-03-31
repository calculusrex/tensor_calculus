import bpy
import numpy as np
import sympy as sp

import numpy as np

from numpy import sin, cos, sqrt

import sys
sys.path.insert(0, '/home/feral/engineering/tensor_calculus/blender')
# from gp_arrow_vertices__ import arrow_vertices__float

##################################################################################################################
# The math

# vector components to point (tuple understood by blender as point)
def v_2_p(matrix):
    x, y, z = matrix[0], matrix[1], matrix[2]
    return float(x), float(y), float(z)

# numpy: the arc is the angle describing the arc, 2*π will be a full circle, 3*π/2 will be three quarters, etc...
def vertex_circle(radius, vertex_number, arc, z):
    r = radius
    angles = [i * arc/vertex_number for i in range(vertex_number)]
    return [np.array([r, α, z]) for α in angles]

def vertical_arrow_vertices(length, cone_radius, cone_height):
    root = np.array([0, 0, 0])
    tip = np.array([0, 0, length])
    circle = vertex_circle(cone_radius, 16, 3*np.pi/2,
                           length - cone_height)
    verts = [root, tip] + circle + [tip]
    return verts


def z_rotation_transform(φ):
    return np.array([
        [cos(φ),     -sin(φ),   0],
        [sin(φ),      cos(φ),   0],
        [0,           0,        1]
    ])

def y_rotation_transform(θ):
    return np.array([
        [cos(θ),     0,     -sin(θ)],
        [0,          1,      0     ],
        [sin(θ),     0,      cos(θ)]
    ])

def vertex__cyllindrical_2_cartesian__along_z(v):
    r, θ, z = v[0], v[1], v[2]
    x = r * np.cos(θ)
    y = r * np.sin(θ)
    return np.array([x, y, z])

def vertex__cyllindrical_2_cartesian__along_y(v):
    r, θ, z = v[0], v[1], v[2]
    x = r * np.cos(θ)
    y = r * np.sin(θ)
    return np.array([x, z, y])

def vertex__cyllindrical_2_cartesian__along_x(v):
    r, θ, z = v[0], v[1], v[2]
    x = r * np.cos(θ)
    y = r * np.sin(θ)
    return np.array([z, x, y])


def cartesian_2_spherical_coordiantes(x_, y_, z_):
    r_ = np.sqrt(x_**2 + y_**2 + z_**2)
    φ_ = np.arccos(x_/np.sqrt(x_**2 + y_**2))
    θ_ = np.arcsin(z_/np.sqrt(x_**2 + y_**2 + z_**2))
    return r_, φ_, θ_


def arrow_points(vector, cone_radius, cone_height):
    x, y, z = vector[0] + 1e-10, vector[1] + 1e-10, vector[2] + 1e-10
    r, φ, θ = cartesian_2_spherical_coordiantes(x, y, z)
    arrow = list(map(vertex__cyllindrical_2_cartesian__along_x,
                     vertical_arrow_vertices(r,
                                             cone_radius,
                                             cone_height)))
    rot_transform = y_rotation_transform(θ)
    rot_transform = np.matmul(z_rotation_transform(φ),
                              rot_transform)
    verts = list(map(lambda vert: v_2_p(np.matmul(rot_transform, vert)),
                     arrow))
    return verts


##################################################################################################################
# The blender code

def get_grease_pencil(gpencil_obj_name='GPencil') -> bpy.types.GreasePencil:
    if gpencil_obj_name not in bpy.context.scene.objects:
        bpy.ops.object.gpencil_add(align='WORLD', location=(0, 0, 0), type='EMPTY') # add object
        bpy.context.scene.objects[-1].name = gpencil_obj_name
    gpencil = bpy.context.scene.objects[gpencil_obj_name]
    return gpencil


def get_grease_pencil_layer(gpencil: bpy.types.GreasePencil,
                            gpencil_layer_name='GP_Layer',
                            clear_layer=False) -> bpy.types.GPencilLayer:
    if gpencil.data.layers and gpencil_layer_name in gpencil.data.layers:
        gpencil_layer = gpencil.data.layers[gpencil_layer_name]
    else:
        gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)
    if clear_layer:
        gpencil_layer.clear()
    return gpencil_layer


def init_grease_pencil(gpencil_obj_name='GPencil',
                       gpencil_layer_name='GP_layer',
                       clear_layer=True) -> bpy.types.GPencilLayer:
    gpencil = get_grease_pencil(gpencil_obj_name)
    gpencil_layer = get_grease_pencil_layer(gpencil, gpencil_layer_name, clear_layer=clear_layer)
    return gpencil_layer


def draw_line(gp_frame, p0: tuple, p1: tuple):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'
    gp_stroke.points.add(count=2)
    gp_stroke.points[0].co = p0
    gp_stroke.points[1].co = p1
    return gp_stroke


def draw_arrow(gp_frame, vector, material_index, cone_radius, cone_height):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'
    gp_stroke.line_width = 5
    gp_stroke.material_index = material_index
    verts = arrow_vertices(vector, cone_radius, cone_height)
    gp_stroke.points.add(count=len(verts))
    for i in range(len(verts)):
        gp_stroke.points[i].co = verts[i]
    return gp_stroke


def select_object(obj):
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

# def create_gp_material(gp: bpy.types.GreasePencil,
#                        color: tuple,
#                        material_name):
#     select_object(gp)
#     bpy.ops.material.new(
#         material_name, set_active=True)
#     bpy.context.object.active_material_index = -1
#     material = bpy.context.object.active_material
#     material.grease_pencil.color = (color)
#     return material, -1


def create_layer(gpencil, layer_name):
    layer = gpencil.data.layers.new(layer_name, set_active=True)
    return layer

def get_layer(gpencil,
              layer_name,
              clear_layer=False):
    if gpencil.data.layers and layer_name in gpencil.data.layers:
        layer = gpencil.data.layers[layer_name]
    else:
        layer = create_layer(gpencil, layer_name)
    if clear_layer:
        layer.clear()
    return layer


def draw_arrow(name,
               grease_pencil,
               layer: bpy.types.GPencilLayer,
               position: np.array,                             # numeric
               vector: np.array,                               # numeric
               thickness: float,
               material_index: float,
               cone_radius: float,
               cone_height: float):
    frame = layer.frames.new(0)
    stroke = frame.strokes.new()
    stroke.display_mode = '3DSPACE'
    stroke.line_width = thickness
    # material, material_index = create_gp_material(grease_pencil, color, name)
    stroke.material_index = material_index
    points = arrow_points(vector, cone_radius, cone_height)
    stroke.points.add(count=len(points))
    for i in range(len(points)):
        stroke.points[i].co = points[i]
    return layer
    

vector_count = 0
def plot_vector(name: str,
                position: sp.Matrix,         # symbolic
                vector: sp.Matrix,           # symbolic
                thickness: float,            # grease pencil line thickness
                material_index: int):
    print('##################################################################################')
    print(f'Plotting vector: {name}')
    numeric_p = np.array(position).transpose().astype(np.float64)
    print('position: ', numeric_p)
    numeric_v = np.array(vector).transpose()[0].astype(np.float64)
    print('vector: ', numeric_v)
    grease_pencil = get_grease_pencil(f'{name}__{str(vector_count).zfill(3)}')
    layer = get_layer(grease_pencil, name, clear_layer=True)
    draw_arrow(name, grease_pencil, layer, numeric_p, numeric_v, thickness, material_index, 0.02, 0.2)
    

##################################################################################################################
# The tensor calculus problem

sys.path.insert(0, '/home/feral/engineering/tensor_calculus/problems')

import problem4__change_of_coordinates__cartesian_2_spherical as problem
import importlib

importlib.reload(problem)


plot_vector('v0', [0, 0, 0], problem.v0, 3, 0)




##################################################################################################################

if __name__ == '__main__':

    gp_layer = init_grease_pencil()
    gp_frame = gp_layer.frames.new(0)


    # draw_arrow(gp_frame, np.array([1, 0, 0]), 0, 0.03, 0.3)
    # draw_arrow(gp_frame, np.array([0, 1, 0]), 0, 0.03, 0.3)
    # draw_arrow(gp_frame, np.array([0, 0, 1]), 0, 0.03, 0.3)

    # draw_arrow(gp_frame, np.array([2/3, 1/2, 3/2]), 1, 0.03, 0.3)


    # for θ in np.arange(-np.pi/2, np.pi/2, np.pi/32):
    #     for φ in np.arange(0, 2*np.pi, np.pi/32):
    #         draw_arrow(gp_frame, np.array([np.cos(θ)*np.cos(φ), np.cos(θ)*np.sin(φ), np.sin(θ)]), 0.01, 0.1)
