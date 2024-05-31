import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

# Stałe
g = 9.81           # przyspieszenie ziemskie w m/s^2
L = 0.5        # długość wahadła w metrach
w0 = np.sqrt(g/L)  #częstosc kołowa wawhadła
T = 10        #czas obrotu ziemi w s (powinno byc 86400 ale wtedy wybombi program bo za duze liczby do rowanania rozniczkowego, do 1000 se radzi)
l = np.radians(90)  #szerokosc goograficzna
omega = 2 * np.pi / T

def system(g, t):
    x, dxdt, y, dydt = g      # x i y to współrzędne sferyczne
    d2xdt2 = 2 * omega * np.sin(l) * np.sin(x) * np.cos(x) * dydt - 2 * omega * np.sin(y) * np.sin(x) * np.sin(x) * np.cos(l) * dydt - w0 ** 2 * np.sin(x) + np.sin(x) * np.cos(x) * dydt * dydt
    epsilon = 1e-6
    d2ydt2 = (-2 * omega * np.sin(l) * np.sin(x) * dxdt + 2 * omega * np.sin(y) * np.sin(x) * np.cos(l) * dxdt - 2 * np.cos(x) * dxdt * dydt) / (np.sin(x) + epsilon)
    return [dxdt, d2xdt2, dydt, d2ydt2]

def solve_system(x0, y0, dxtd0,dydt0, t):

    conditions = [x0, y0, dxtd0,dydt0]

    solution = odeint(system, conditions, t)

    x_sol = solution[:, 0]
    dxdt_sol = solution[:, 1]
    y_sol = solution[:, 2]
    dydt_sol = solution[:, 3]

    return t, x_sol, y_sol, dxdt_sol, dydt_sol


# Przykładowe wartości początkowe
x0 = np.radians(50)
y0 = np.radians(0)
dxdt0 = np.radians(0)
dydt0 = np.radians(0)

# Przedział czasu
t = np.linspace(0, 100, 1000) # start/stop - oczywiste num - jak gesto bedzie "bedzie animacja brala punkty"

# Rozwiązanie układu równań różniczkowych
t, x_sol, y_sol, dxdt_sol, dydt_sol = solve_system(x0, y0, dxdt0, dydt0, t)

xw = L * np.sin(x_sol) * np.cos(y_sol)
yw = L * np.sin(x_sol) * np.sin(y_sol)
zw = -L * np.cos(x_sol)

# Tworzenie wykresu 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-L, L])
ax.set_ylim([-L, L])
ax.set_zlim([-L, L])
line, = ax.plot([], [], [], 'o-', lw=2)
trace, = ax.plot([], [], [], lw=1)

def init():
    line.set_data([], [])
    line.set_3d_properties([])
    return line, trace

def update(frame):
    line.set_data([0, xw[frame]], [0, yw[frame]])
    line.set_3d_properties([0, zw[frame]])
    trace.set_data(xw[:frame], yw[:frame])
    trace.set_3d_properties(zw[:frame])
    return line, trace

ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True)

plt.show()



