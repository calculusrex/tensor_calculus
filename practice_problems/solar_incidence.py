import sympy as sp
from sympy import cos, sin, symbols, sqrt, simplify, acos, asin, Matrix, diff, pi



##########################################################################################
# Chapter 2: Earth's orbit around the sun

# the relationships linking the cartesian coordinate system of the sun to the polar coordinate system of the sun.

x, y, z = symbols('x y z')
r, φ, θ = symbols('r φ θ')

# When θ is 0, the system is restricted to the plane of the sun's equator, the plane in which most planets tend to orbit.

sol_prox = {}
sol_prox['x'] = r * cos(θ) * cos(φ)
sol_prox['y'] = r * cos(θ) * sin(φ)
sol_prox['z'] = r * sin(θ)
sol_prox['r'] = sqrt(x**2 + y**2 + z**2)
sol_prox['φ'] = acos(x/(sqrt(x**2 + y**2)))
sol_prox['θ'] = asin(z/(sqrt(x**2 + y**2 + z**2)))

# shorthand for relationship dictionary
rd = sol_prox

F = Matrix([
    [diff(rd['x'], r), diff(rd['x'], φ), diff(rd['x'], θ)],
    [diff(rd['y'], r), diff(rd['y'], φ), diff(rd['y'], θ)],
    [diff(rd['z'], r), diff(rd['z'], φ), diff(rd['z'], θ)]
]).applyfunc(sp.simplify)

B = Matrix([
    [diff(rd['r'], x), diff(rd['r'], y), diff(rd['r'], z)],
    [diff(rd['φ'], x), diff(rd['φ'], y), diff(rd['φ'], z)],
    [diff(rd['θ'], x), diff(rd['θ'], y), diff(rd['θ'], z)]
]).applyfunc(sp.simplify)

# the vector of solar light incidence on the position of the planet. the coordinate base in which it is described here is in the orbit coordinate system (polar coordinate system with the sun at origin) the one i named proxy1
solar_incidence__prox1 = Matrix([
    1,
    0,
    0
])

# vector components are countervariate, so to convert them to the former repsresentation, you apply the forward transform
solar_incidence__sol = F * solar_incidence__prox1


##########################################################################################
# Chapter 2: Earth's axis of rotation

α = sp.Symbol('α')

# I composed this matrix looking at the graph i sketched in my notebook.
F = Matrix([
    [1,  0,      0     ],
    [0,  cos(α), sin(α)],
    [0, -sin(α), cos(α)]
])

B = simplify(F.inv())

solar_incidence__ax = B * solar_incidence__sol

##########################################################################################
# Chapter 3: Earth's surface

β, γ = symbols('β γ')

ax_surf = {}
ax_surf['x'] = r * cos(γ) * cos(β)
ax_surf['y'] = r * cos(γ) * sin(β)
ax_surf['z'] = r * sin(γ)
ax_surf['r'] = sqrt(x**2 + y**2 + z**2)
ax_surf['β'] = acos(x/(sqrt(x**2 + y**2)))
ax_surf['γ'] = asin(z/(sqrt(x**2 + y**2 + z**2)))

rd = ax_surf

F = Matrix([
    [diff(rd['x'], r), diff(rd['x'], β), diff(rd['x'], γ)],
    [diff(rd['y'], r), diff(rd['y'], β), diff(rd['y'], γ)],
    [diff(rd['z'], r), diff(rd['z'], β), diff(rd['z'], γ)]
]).applyfunc(sp.simplify)

B = Matrix([
    [diff(rd['r'], x), diff(rd['r'], y), diff(rd['r'], z)],
    [diff(rd['β'], x), diff(rd['β'], y), diff(rd['β'], z)],
    [diff(rd['γ'], x), diff(rd['γ'], y), diff(rd['γ'], z)]
]).applyfunc(sp.simplify)

solar_incidence__surf = simplify(B * solar_incidence__ax)

if __name__ == '__main__':
    sp.init_printing()
