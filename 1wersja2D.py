#kod korzystający ze wzorów z wikipedii, okazalo się, że równania są zbyt złożone dla pythona, aby zrealizować w 3d, więc z tymi wzorami zrobilismy 2d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

L = 0.3  # Długość wahadła (m)
g = 9.81  # Przyspieszenie grawitacyjne (m/s^2)
T = 10  # Czas trwania (s)
Ω = 2 * np.pi / T  # Pulsacja obrotu Ziemi
l = np.radians(90)  # Szerokość geograficzna wahadła
ω0 = np.sqrt(g / L)
theta0 = np.pi / 4  # początkowy kąt (w radianach)




# Definicja układu równań różniczkowych
def system(y, t):
    x, dxdt, y, dydt = y
    d2ydt2 = -2 * y * ω0 * ω0 - 2 * Ω * dxdt * np.sin(l)
    d2xdt2 = -2 * x * ω0 * ω0 + 2 * Ω * dydt * np.sin(l)
    return [dxdt, d2xdt2, dydt, d2ydt2]


# Funkcja do rozwiązania równań różniczkowych
def solve_system(x0, y0, dxdt0, dydt0, t):
    # Warunki początkowe
    initial_conditions = [x0, dxdt0, y0, dydt0]

    # Rozwiązanie układu równań różniczkowych
    solution = odeint(system, initial_conditions, t)

    # Rozdzielenie wyników na poszczególne zmienne
    x_sol = solution[:, 0]
    dxdt_sol = solution[:, 1]
    y_sol = solution[:, 2]
    dydt_sol = solution[:, 3]

    return t, x_sol, y_sol, dxdt_sol, dydt_sol


# Przykładowe wartości początkowe
x0 = 0.0
y0 = 0.0
dxdt0 = 10.0
dydt0 = 0.0

# Przedział czasu
t = np.linspace(0, 10, 1000)

# Rozwiązanie układu równań różniczkowych
t, x_sol, y_sol, dxdt_sol, dydt_sol = solve_system(x0, y0, dxdt0, dydt0, t)





# Funkcja do aktualizacji animacji
def update(frame):
    ax.clear()
    ax.plot(x_sol[:frame], y_sol[:frame], color='g', linestyle='--')  # Ścieżka wahadła
    ax.plot([0, x_sol[frame]], [0, y_sol[frame]], color='b')  # Linia wahadła
    ax.scatter(x_sol[frame], y_sol[frame], color='r')  # Masa wahadła
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Animacja Wahadła w 2D')


# Tworzenie animacji
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ani = FuncAnimation(fig, update, frames=len(t), interval=10)  # Mniejszy interval dla szybszej animacji

plt.show()
