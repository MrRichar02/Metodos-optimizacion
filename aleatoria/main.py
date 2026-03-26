import numpy as np
import pandas as pd

# x, y = sp.symbols("x y")
# f_str = sp.sympify("y -x -2*x**2 - 2*x*y -y**2")
# np_f = sp.lambdify([x, y], f_str, "numpy")
def aleatorio(lim_x, lim_y, iterations, f, mode=1):  # mode=1: máximo, mode=2: mínimo
    xu, xl = lim_x
    yu, yl = lim_y
    rows = []

    if mode == 1:  # Buscar máximo
        best_f = -float('inf')
        best_x, best_y = 0, 0
        for _ in range(iterations):
            r = np.random.random()
            current_x = xl + (xu - xl) * r
            current_y = yl + (yu - yl) * r
            current_f = f(current_x, current_y)
            rows.append([best_x, best_y, best_f, r, current_x, current_y, current_f])
            if current_f > best_f:
                best_f = current_f
                best_x, best_y = current_x, current_y
        columns = ["Best x", "Best y", "Best f(x,y)", "r", "current x", "current y", "current f(x,y)"]
    else:  # Buscar mínimo
        best_f = float('inf')
        best_x, best_y = 0, 0
        for _ in range(iterations):
            r = np.random.random()
            current_x = xl + (xu - xl) * r
            current_y = yl + (yu - yl) * r
            current_f = f(current_x, current_y)
            rows.append([best_x, best_y, best_f, r, current_x, current_y, current_f])
            if current_f < best_f:
                best_f = current_f
                best_x, best_y = current_x, current_y
        columns = ["Best x", "Best y", "Best f(x,y)", "r", "current x", "current y", "current f(x,y)"]
    
    df = pd.DataFrame(rows, columns=columns)
    return df

# df = aleatorio((2,-2), (3, 1), 1000, np_f)
# print(df)
