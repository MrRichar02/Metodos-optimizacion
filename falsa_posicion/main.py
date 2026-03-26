import pandas as pd

def falsa_posicion(funcion, xu, xl, error):
    if funcion(xu) * funcion(xl) >= 0:
        print("La función no cambia de signo en el intervalo dado.")
        return None, None
    rows = []
    xr = xu - (funcion(xu) * (xl - xu)) / (funcion(xl) - funcion(xu))
    decicion = funcion(xr) * funcion(xl)
    rows.append([xu, xl, xr, funcion(xr), abs(xu-xr) if abs(xu-xr)<abs(xr-xl) else abs(xr-xl)])
    while abs(xu - xr) > error and abs(xr-xl) > error:
        if decicion < 0:
            xu = xr
        elif decicion > 0:
            xl = xr
        else:
            print("xr es la raíz exacta.")
            return xr,pd.DataFrame(rows, columns=["xu", "xl", "xr", "f(xr)", "Error"])

        xr = xu - (funcion(xu) * (xl - xu)) / (funcion(xl) - funcion(xu))
        decicion = funcion(xr) * funcion(xl)
        rows.append([xu, xl, xr, funcion(xr), abs(xu-xr) if abs(xu-xr)<abs(xr-xl) else abs(xr-xl)])
    return xr, pd.DataFrame(rows, columns=["xu", "xl", "xr", "f(xr)", "Error"])

# func_str = input("Escriba la función: ")
# x = sp.symbols("x")
# f = sp.sympify(func_str)
# np_f = sp.lambdify(x, func_str, "numpy")
# xr1, df1 = falsa_posicion(np_f, 4, 0, 0.01)
# xr2, df2 = falsa_posicion(np_f, 41, 15, 0.01)
#
# print(xr1, xr2)
