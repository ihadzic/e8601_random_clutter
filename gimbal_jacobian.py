import sympy as sp

x, y, z, w1, w2, dt, a = sp.symbols('x, y, z, w1, w2, dt, a')

gx = x * sp.cos(w1 * dt) * sp.cos(w2 * dt) \
    - y * sp.cos(w1 * dt) * sp.sin(w2 * dt) \
    - (z * x) / sp.sqrt(a**2 - z**2) * sp.sin(w1 * dt) * sp.cos(w2 * dt) \
    + (z * y) / sp.sqrt(a**2 - z**2) * sp.sin(w1 * dt) * sp.sin(w2 * dt) \

gy = y * sp.cos(w1 * dt) * sp.cos(w2 * dt) \
    - x * sp.cos(w1 * dt) * sp.sin(w2 * dt) \
    - (z * y) / sp.sqrt(a**2 - z**2) * sp.sin(w1 * dt) * sp.cos(w2 * dt) \
    + (z * x) / sp.sqrt(a**2 - z**2) * sp.sin(w1 * dt) * sp.sin(w2 * dt) \

gz = z * sp.cos(w1 * dt) + sp.sqrt(a**2 - z**2) * sp.sin(w1 * dt)

f = sp.Matrix([gx, gy, gz])

Hx = f.jacobian(sp.Matrix([x, y, z]))
Hu = f.jacobian(sp.Matrix([w1, w2]))

Hx_simp = Hx.applyfunc(sp.simplify)
Hu_simp = Hu.applyfunc(sp.simplify)

Hx_func = sp.lambdify((x, y, z, w1, w2, dt, a), Hx_simp)
Hu_func = sp.lambdify((x, y, z, w1, w2, dt, a), Hu_simp)

print(Hx_simp)
print(Hu_simp)

print(Hx_func(1, 1, 1, 4, 5, 0.1, 2))
print(Hu_func(1, 1, 1, 4, 5, 0.1, 2))
