import numpy as np
import pandas as pd

# x, y = sp.symbols("x y")
# f_str = sp.sympify("y -x -2*x**2 - 2*x*y -y**2")
# np_f = sp.lambdify([x, y], f_str, "numpy")
def aleatorio(lim_x, lim_y, iterations, f):
    xu, xl = lim_x
    yu, yl = lim_y
    rows = []

    max_f, maxx, maxy = 1e-9, 0, 0
    for _ in range(iterations):
        r = np.random.random()
        current_x = xl+(xu-xl)*r
        current_y = yl+(yu-yl)*r
        current_f = f(current_x, current_y)
        rows.append([maxx, maxy, max_f, r, current_x, current_y, current_f])
        if current_f > max_f: 
            max_f = current_f
            maxx = current_x
            maxy = current_y
    df = pd.DataFrame(rows, columns=["Max x", "Max y", "Max f(x,y)", "r", "current x", "current y", "current f(x,y)"])
    return df

# df = aleatorio((2,-2), (3, 1), 1000, np_f)
# print(df)
