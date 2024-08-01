import sympy as sp

print('calculating posterior for first landmark addition')
a, d, e = sp.symbols('a, d, e')
J = sp.Matrix([[-1, 1]])
H = J
Sigma = sp.Matrix([[a, 0],[0, d]])
SigmaHT = Sigma * H.transpose()
HSigmaHT = H * SigmaHT
K = SigmaHT * (HSigmaHT + sp.Matrix([[e]]))**-1
k1 = sp.limit(K[0,0], d, sp.oo)
k2 = sp.limit(K[1,0], d, sp.oo)
print('lim K=[[{}],[{}]]'.format(k1, k2))
Sigma_next = (sp.eye(2) - K*H)*Sigma
s11 = sp.limit(Sigma_next[0,0], d, sp.oo)
s12 = sp.limit(Sigma_next[0,1], d, sp.oo)
s21 = sp.limit(Sigma_next[1,0], d, sp.oo)
s22 = sp.limit(Sigma_next[1,1], d, sp.oo)
print('lim Sigma_next=[[{}, {}],[{}, {}]]'.format(s11, s12, s21, s22))
print('')

print('calculating posterior for second landmark addition')
a, b, x, d, e = sp.symbols('a, b, x, d, e')
J = sp.Matrix([[-1, 1]])
F = sp.Matrix([[1, 0, 0],[0, 0, 1]])
H = J * F
Sigma = sp.Matrix([[a, x, 0],[x, b, 0], [0, 0, d]])
SigmaHT = Sigma * H.transpose()
HSigmaHT = H * SigmaHT
K = SigmaHT * (HSigmaHT + sp.Matrix([[e]]))**-1
k1 = sp.limit(K[0,0], d, sp.oo)
k2 = sp.limit(K[1,0], d, sp.oo)
k3 = sp.limit(K[2,0], d, sp.oo)
print('lim K=[[{}],[{}],[{}]]'.format(k1, k2, k3))
Sigma_next = (sp.eye(3) - K*H)*Sigma
s11 = sp.limit(Sigma_next[0,0], d, sp.oo)
s12 = sp.limit(Sigma_next[0,1], d, sp.oo)
s13 = sp.limit(Sigma_next[0,2], d, sp.oo)
s21 = sp.limit(Sigma_next[1,0], d, sp.oo)
s22 = sp.limit(Sigma_next[1,1], d, sp.oo)
s23 = sp.limit(Sigma_next[1,2], d, sp.oo)
s31 = sp.limit(Sigma_next[2,0], d, sp.oo)
s32 = sp.limit(Sigma_next[2,1], d, sp.oo)
s33 = sp.limit(Sigma_next[2,2], d, sp.oo)
print('lim Sigma=[[{}, {}, {}],[{}, {}, {}],[{}, {}, {}]]'.format(
    s11, s12, s13, s21, s22, s23, s31, s32, s33))
print('')

print('calculating posterior for third landmark addition')
a, b, c, w, x, d, e = sp.symbols('a, b, c, w, x, d, e')
J = sp.Matrix([[-1, 1]])
F = sp.Matrix([[1, 0, 0, 0],[0, 0, 0, 1]])
H = J * F
Sigma = sp.Matrix([[a, x, w, 0],[x, b, x, 0], [w, x, c, 0], [0, 0, 0, d]])
SigmaHT = Sigma * H.transpose()
HSigmaHT = H * SigmaHT
K = SigmaHT * (HSigmaHT + sp.Matrix([[e]]))**-1
k1 = sp.limit(K[0,0], d, sp.oo)
k2 = sp.limit(K[1,0], d, sp.oo)
k3 = sp.limit(K[2,0], d, sp.oo)
k4 = sp.limit(K[3,0], d, sp.oo)
print('lim K=[[{}],[{}],[{}],[{}]]'.format(k1, k2, k3, k4))
Sigma_next = (sp.eye(4) - K*H)*Sigma
s11 = sp.limit(Sigma_next[0,0], d, sp.oo)
s12 = sp.limit(Sigma_next[0,1], d, sp.oo)
s13 = sp.limit(Sigma_next[0,2], d, sp.oo)
s14 = sp.limit(Sigma_next[0,3], d, sp.oo)
s21 = sp.limit(Sigma_next[1,0], d, sp.oo)
s22 = sp.limit(Sigma_next[1,1], d, sp.oo)
s23 = sp.limit(Sigma_next[1,2], d, sp.oo)
s24 = sp.limit(Sigma_next[1,3], d, sp.oo)
s31 = sp.limit(Sigma_next[2,0], d, sp.oo)
s32 = sp.limit(Sigma_next[2,1], d, sp.oo)
s33 = sp.limit(Sigma_next[2,2], d, sp.oo)
s34 = sp.limit(Sigma_next[2,3], d, sp.oo)
s41 = sp.limit(Sigma_next[3,0], d, sp.oo)
s42 = sp.limit(Sigma_next[3,1], d, sp.oo)
s43 = sp.limit(Sigma_next[3,2], d, sp.oo)
s44 = sp.limit(Sigma_next[3,3], d, sp.oo)
print('lim Sigma=[[{}, {}, {}, {}],[{}, {}, {}, {}],[{}, {}, {}, {}],[{}, {}, {}, {}]]'.format(
    s11, s12, s13, s14,
    s21, s22, s23, s24,
    s31, s32, s33, s34,
    s41, s42, s43, s44))
