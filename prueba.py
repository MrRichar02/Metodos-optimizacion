import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir la función
def f(x, y):
    return y - x - 2*x**2 - 2*x*y - y**2

# Crear la malla
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# Crear la figura 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficar la superficie
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, edgecolor='none')

# Resaltar la curva donde Z=0 (en rojo)
contour = ax.contour(X, Y, Z, levels=[0], colors='red', linewidths=2, zorder=10)

# Personalizar
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Superficie f(x,y) = y - x - 2x² - 2xy - y²\nCurva roja: f(x,y)=0')

# Agregar barra de color
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

plt.show()
