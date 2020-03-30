
from tensor_algebra__ import *

import simpy as sp

s = sp.simplify

system0 = CoordinateSystem()


e__0 = CoordinateBase('e__0',
                      system0)

e__1 = CoordinateBase('e__1',
                      system0,
                      system.base['e__0'],
                      sp.Matrix([
                          [-1, -1],
                          [0, -s(3)/4]
                      ]))
