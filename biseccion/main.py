import pandas as pd

def biseccion(function, xu, xl, error):
    if function(xu) * function(xl) > 0:
        return None, None

        # Inicializar el dataframe
    df = pd.DataFrame(
            columns=["xu", "xl", "xr", "f(xu)", "f(xl)", "f(xr)", "f(xl)f(xr)", "Error"]
    )

    xr = (xl + xu) / 2
    fxu = function(xu)
    fxl = function(xl)
    fxr = function(xr)

    fxl_xu = fxl * fxr
    error_actual = xu - xr

    df.loc[len(df)] = [xu, xl, xr, fxu, fxl, fxr, fxl_xu, error_actual]

    while error_actual > error:
        if fxl_xu < 0:
            xu = xr
        elif fxl_xu > 0:
            xl = xr
        elif fxl_xu == 0:
            return xr, df

        xr = (xl + xu) / 2
        fxu = function(xu)
        fxl = function(xl)
        fxr = function(xr)

        fxl_xu = fxl * fxr
        error_actual = xu - xr

        df.loc[len(df)] = [xu, xl, xr, fxu, fxl, fxr, fxl_xu, error_actual]

    return xr, df

# func_str = input("Escriba la función: ")
# x = sp.symbols("x")
# f = sp.sympify(func_str)
# np_f = sp.lambdify(x, f, "numpy")
# # f = lambda x: 3*x**2 - 120*x + 100
# error = 0.000001
# # xr, df = biseccion(np_f, 45, 35, error)
# xr, df = biseccion(np_f, 1, 0, error)
#
# print(df)
