import numpy as np  #memasukkan library numpy
import sympy as smp   #memasukkan library sympy
from scipy.integrate import odeint 
import matplotlib.pyplot as plt  #memasukkan library matplotlib untuk memplot data
from matplotlib import animation     #mengimpor hasil plot dalam bentuk gif
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import PillowWriter

#Rumus dua pendulum meliputi :
# x1 = cos(wt) + L1*sin (teta1)
# x2 = cos(wt) + L2*sin(teta1)+L2*sin(teta2)
# y1 = -L1*cos(teta1)
# y2 = - L1*cos(teta1) - L2*cos(teta2) 

#Menentukan variabel yang diperlukan untuk sympy
t, m, g, L1, L2, w, C, alph, beta = smp.symbols(r't m g L_1, L_2 \omega C \alpha \beta')

#Mendefinisikan teta1(t)dalam sympy dan teta2(t) dan inisiasikannya sebagai fungsi waktu.
the1, the2, =  smp.symbols(r'\theta_1, \theta_2 ', cls=smp.Function)

the1 = the1(t)         #inisiasi teta 1 sebagai fungsi waktu

#Menurunkan teta 1 untuk turunan pertama dan kedua 
the1_d = smp.diff(the1, t)   #diferensiasi teta1 untuk turunan pertama 
the1_dd = smp.diff(the1_d, t)  #turunan kedua
#Mendefinisikan juga untuk teta 2 
the2 = the2(t)  #teta 2 sebagai fungsi waktu 
the2_d = smp.diff(the2, t) #diferensiasi teta2 untuk turunan pertama
the2_dd = smp.diff(smp.diff(the2, t), t) # untuk turunan kedua

#Mendeklarasi untuk nilai x1(teta1),y1(teta1) dan x2(teta1,teta2),y2(teta1,teta2)
x1, y1, x2, y2 = smp.symbols('x_1, y_1, x_2, y_2', cls=smp.Function) # inisiasi sebagai fungsi 
x1= x1(t, the1) 
y1= y1(t, the1)
x2= x2(t, the1, the2)
y2= y2(t, the1, the2)

# Setelah dideklarasi dimasukkan ke dalam bentuk fungsional spesifik dari x1, y1,x2,y2
x1 = smp.cos(w*t)+L1*smp.sin(the1)
y1 = -L1*smp.cos(the1)
x2 = smp.cos(w*t)+L1*smp.sin(the1) + L2*smp.sin(the2)
y2 = -L1*smp.cos(the1) -L2*smp.cos(the2)

#Mendefinisikan Fungsi Numerik untuk Vx1, Vy1, Vx2, Vy2
smp.diff(x1, t)

# Masukkan kedalam rumus = L1*cos(teta1(t))*d/dt*teta(t)-w*sin(wt)untuk semua fungsi numerik
vx1_f = smp.lambdify((t,w,L1,L2,the1,the2,the1_d,the2_d), smp.diff(x1, t))
vx2_f = smp.lambdify((t,w,L1,L2,the1,the2,the1_d,the2_d), smp.diff(x2, t))
vy1_f = smp.lambdify((t,w,L1,L2,the1,the2,the1_d,the2_d), smp.diff(y1, t))
vy2_f = smp.lambdify((t,w,L1,L2,the1,the2,the1_d,the2_d), smp.diff(y2, t))

#Mendefinisikan energi kinetik = T, energi potensial = V, dan rumus Lagrangian L = T-V 
T = 1/2 * (smp.diff(x1, t)**2 + smp.diff(y1, t)**2) + \
    1/2 * m  *(smp.diff(x2, t)**2 + + smp.diff(y2, t)**2)
V = g*y1 + m*g*y2
L = T-V

# Menyelesaikan persamaan Lagrangian dohL/dohteta - d/dt*dohL/dohteta = 0 
# Pada LE1 
LE1 = smp.diff(L, the1) - smp.diff(smp.diff(L, the1_d), t)
LE1 = LE1.simplify()
# Pada LE2
LE2 = smp.diff(L, the2) - smp.diff(smp.diff(L, the2_d), t)
LE2 = LE2.simplify()

#Karena keduanya sama dengan nol dan linier maka dapat dinyatakan
#bahwa doh(t)^2teta1 dan doh(t)^teta 2 dapat menyelesaikan masalah
#(ini memberi kita dua ODE orde kedua yang digabungkan)
sols = smp.solve([LE1, LE2], (the1_dd, the2_dd),
                simplify=False, rational=False)

sols[the1_dd] #d^2 / dt^2 theta_1

# Untuk menemukan frekuensi berjalan yang menghasilkan resonansi, dapat disederhanakan dengan mengasumsikan :
# Asumsi pendekatan sudut kecil untuk teta1 dan teta 2
# Asumsi bahwa teta1 dan teta2 memiliki solusi teta1(t) = C*cos(wt) dan teta2(t) = C*alph*cos(wt) 

# Untuk LE1
a = LE1.subs([(smp.sin(the1-the2), the1-the2),
         (smp.cos(the1-the2), 1),
         (smp.cos(the1), 1),
         (smp.sin(the1), the1),
         (the1, C*smp.cos(w*t)),
         (the2, C*alph*smp.cos(w*t)),
         (m, 1),
         (L2, L1),
         ]).doit().series(C, 0, 2).removeO().simplify()
b = LE2.subs([(smp.sin(the1-the2), the1-the2),
         (smp.cos(the1-the2), 1),
         (smp.cos(the1), 1),
         (smp.cos(the2), 1),
         (smp.sin(the1), the1),
         (smp.sin(the2), the2), 
         (the1, C*smp.cos(w*t)),
         (the2, C*alph*smp.cos(w*t)),
         (m, 1),
         (L2, L1),
         ]).doit().series(C, 0, 2).removeO().simplify()
yeet = smp.solve([a.args[1], b.args[2]], (w, alph))
yeet[2][0]
yeet[0][0]
smp.limit(yeet[1][0].subs(C, beta/L1).simplify(), beta, smp.oo)

# Pertukaran Numerik
# Dengan mendefinisikan persamaan :
# d^2teta/dt^2 = dzeta/dt dimana dteta/dt = zeta
dz1dt_f = smp.lambdify((t, m, g, w, L1, L2, the1, the2, the1_d, the2_d), sols[the1_dd])
dthe1dt_f = smp.lambdify(the1_d, the1_d)

dz2dt_f = smp.lambdify((t, m, g, w, L1, L2, the1, the2, the1_d, the2_d), sols[the2_dd])
dthe2dt_f = smp.lambdify(the2_d, the2_d)

#Mendefinisikan sistem ODE untuk python S = (teta1,zeta1,teta2,zeta2) 
def dSdt(S, t):
    the1, z1, the2, z2 = S
    return [
        dthe1dt_f(z1),
        dz1dt_f(t, m, g, w, L1, L2, the1, the2, z1, z2),
        dthe2dt_f(z2),
        dz2dt_f(t, m, g, w, L1, L2, the1, the2, z1, z2),
    ]

# Masukkan bebeberapa nilai numerik untuk mendapatkan solusi 
t = np.linspace(0, 20, 1000)
g = 9.81
m=1
L1 = 20
L2 = 20
w = np.sqrt(g/L1)
ans = odeint(dSdt, y0=[0, 0, 0, 0], t=t)

# inisiasi plot untuk plot teta1(t)
plt.plot(ans.T[0])

#Fungsi yang menghitung energi kinetik rata - rata ( dengan asumsi ) dari sistem yang diberikan oleh :
# E(w) = Mean(Vx1^2 + Vy1^2 + Vx2^2 + Vy2^2)
# maka nilai V dihitung dengan memecahkan ODE untuk sejumlah titik waktu untuk nilai spesifik w

def get_energy(w):
    t = np.linspace(0, 100, 2000)
    ans = odeint(dSdt, y0=[0.1, 0.1, 0, 0], t=t)
    vx1 = vx1_f(t,w,L1,L2,ans.T[0],ans.T[2],ans.T[1],ans.T[3])
    vx2 = vx2_f(t,w,L1,L2,ans.T[0],ans.T[2],ans.T[1],ans.T[3])
    vy1 = vy1_f(t,w,L1,L2,ans.T[0],ans.T[2],ans.T[1],ans.T[3])
    vy2 = vy2_f(t,w,L1,L2,ans.T[0],ans.T[2],ans.T[1],ans.T[3])
    E = 1/2 * np.mean(vx1**2+vx2**2+vy1**2+vy2**2)
    return E

# inisiasi nilai w(s) dan E(s) 
ws = np.linspace(0.4, 1.3, 100)
Es = np.vectorize(get_energy)(ws)

#Memplot sistem energi kinetic untuk nilai diferensial dari w 

plt.plot(ws, Es)
plt.axvline(1.84775*np.sqrt(g/L1), c='k', ls='--')
plt.axvline(0.76536*np.sqrt(g/L1), c='k', ls='--')
# Tautochrone
#plt.axvline(np.sqrt(np.pi*g**(-1/2)), c='k', ls='--')
plt.grid()

#Selesaikan ODE untuk nilai tertentu sehingga muncul solusi. Tentukan juga fungsi teta1(t) dan teta2(t)
# Mengembalikan nilai x dan y yang sesuai dari asal. bob pertama dan bob kedua
t = np.linspace(0, 200, 20000)
g = 9.81
m=1
L1 = 20
L2 = 20
w = ws[ws>1][np.argmax(Es[ws>1])]
ans = odeint(dSdt, y0=[0.1, 0.1, 0, 0], t=t)

def get_x0y0x1y1x2y2(t, the1, the2, L1, L2):
    return (np.cos(w*t),
            0*t,
            np.cos(w*t) + L1*np.sin(the1),
            -L1*np.cos(the1),
            np.cos(w*t) + L1*np.sin(the1) + L2*np.sin(the2),
            -L1*np.cos(the1) - L2*np.cos(the2),
    )

x0, y0, x1, y1, x2, y2 = get_x0y0x1y1x2y2(t, ans.T[0], ans.T[2], L1, L2)

# Membuat Animasi 
def animate(i):
    ln1.set_data([x0[::10][i], x1[::10][i], x2[::10][i]], [y0[::10][i], y1[::10][i], y2[::10][i]])
    trail1 = 50            # length of motion trail of weight 1 
    trail2 = 50            # length of motion trail of weight 2
    ln2.set_data(x1[::10][i:max(1,i-trail1):-1], y1[::10][i:max(1,i-trail1):-1])   # marker + line of first weight
    ln3.set_data(x2[::10][i:max(1,i-trail2):-1], y2[::10][i:max(1,i-trail2):-1])   # marker + line of the second weight
    
fig, ax = plt.subplots(1,1, figsize=(8,8))
ax.set_facecolor('k')
ax.get_xaxis().set_ticks([])    # enable this to hide x axis ticks
ax.get_yaxis().set_ticks([])    # enable this to hide y axis ticks
ln1, = plt.plot([], [], 'ro--', lw=3, markersize=8)
ln2, = ax.plot([], [], 'ro-',markersize = 8, alpha=0.05, color='cyan')   # line for Earth
ln3, = ax.plot([], [], 'ro-',markersize = 8,alpha=0.05, color='cyan')
ax.set_ylim(-44,44)
ax.set_xlim(-44,44)
ani = animation.FuncAnimation(fig, animate, frames=2000, interval=50)
ani.save('pen.gif',writer='pillow',fps=50)

