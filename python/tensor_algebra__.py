import sympy as sp
import numpy as np
import functools as ft



# Product = Operation(commutative=True, associative=True)

def chars_to_string(chars):
    return ft.reduce(lambda a, b: f'{a}{b}', chars)


def tprint(tensor):
    superscript, center, subscript = tstrings(tensor)
    print(superscript)
    print(center)
    print(subscript)

def tstrings(tensor):
    superscript = ""
    center = ""
    subscript = ""

    # the tensor name
    superscript = superscript + chars_to_string([' ' for _ in range(len(tensor.name))])
    center = center + tensor.name
    subscript = subscript + chars_to_string([' ' for _ in range(len(tensor.name))])

    # the indices
    superscript = superscript + chars_to_string(tensor.contravariant_indices)
    center = center + chars_to_string(
        [' ' for _ in range(max(len(tensor.contravariant_indices),
                                len(tensor.covariant_indices)))])
    subscript = subscript + chars_to_string(tensor.covariant_indices)

    return superscript, center, subscript
    


class GeneralTensor():
    def __init__(self, name, covariant_indices, contravariant_indices):
        self.name = name
        self.covariant_indices = covariant_indices
        self.contravariant_indices = contravariant_indices
        self.type = len(contravariant_indices), len(covariant_indices)

class NDTensor():
    pass



def kronecker_delta(ndim):
    return sp.Matrix(
        [[(1 if i==j else 0) for i in range(ndim)] for j in range(ndim)]
    )


# def forward_transform__from_root(base):
#     transform = kronecker_delta(base.system.ndim)

#     while not base.isroot:
#         transform = transform * base.transform_to_defbase
    
#     return transform


# def backward_transform__to_root(base):
#     transforms = []

#     while not base.isroot:
#         transforms.append(base.transform_from_defbase)
#         base = base.defbase

#     transforms.reverse()
    
#     return ft.reduce(lambda m1, m2: m1 * m2, transforms)



# class CoordinateSystem():
#     def __init__(self):
#         self.coordinate_base_identifiers = set()
#         self.base = {}
        

#     def add(self, base):
#         self.coordinate_base_identifiers.add(base.identifier)
#         if not base.isroot:
#             self.base[base.identifier] = base
            
            
        


# class CoordinateBase():
#     def __init__(self, string_identifier, coordinate_system,
#                  definition_base=None, forward_transform_matrix=None):

#         assert (string_identifier not in coordinate_system.coordinate_base_identifiers), 'Identifeir already in use'
        
#         self.identifier = string_identifier
#         self.system = coordinate_system

#         self.transform_from = {}
#         self.transform_to = {}

#         if definition_base == None:
#             self.isroot = True
#             self.defbase = None

#         else:
#             self.isroot = False
#             self.defbase = definition_base
#             self.transform_from_defbase = forward_transform_matrix
#             self.transform_to_defbase = forward_transform_matrix.inv()
#             self.transform_from[self.defbase.identifier] = forward_transform_matrix
#             self.transform_to[self.defbase.identifier] = forward_transform_matrix.inv()

#         self.system.add(self)


# class Vector():
#     def __init__(self, coordinate_system, coordinate_base, *coords):
#         self.system = coordinate_system
#         self.defbase = coordinate_base
#         self.comps = sp.Matrix(
#             coords)

#     def base():
#         pass
        


if __name__ == '__main__':
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('TENSOR ALGEBRA')
    print()

    sp.init_printing(use_unicode=True)

    
