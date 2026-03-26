import pandas as pd

def falsa_posicion(funcion, xu, xl, error, max_iter=100):
    if funcion(xu) * funcion(xl) >= 0:
        print("La función no cambia de signo en el intervalo dado.")
        return None, None
    
    rows = []
    iter_count = 0
    
    # Calcular primera aproximación
    xr_anterior = xu - (funcion(xu) * (xl - xu)) / (funcion(xl) - funcion(xu))
    error_actual = abs(xr_anterior)
    
    while error_actual > error and iter_count < max_iter:
        xr = xu - (funcion(xu) * (xl - xu)) / (funcion(xl) - funcion(xu))
        
        # Calcular error usando valor absoluto
        error_actual = abs(xr - xr_anterior) if iter_count > 0 else abs(xr)
        
        rows.append([xu, xl, xr, funcion(xr), error_actual])
        
        # Verificar si es raíz exacta
        if funcion(xr) == 0:
            print("xr es la raíz exacta.")
            return xr, pd.DataFrame(rows, columns=["xu", "xl", "xr", "f(xr)", "Error"])
        
        # Actualizar intervalo
        if funcion(xr) * funcion(xl) < 0:
            xu = xr
        else:
            xl = xr
        
        xr_anterior = xr
        iter_count += 1
    
    if iter_count >= max_iter:
        print(f"Se alcanzó el máximo de iteraciones ({max_iter})")
    
    return xr_anterior, pd.DataFrame(rows, columns=["xu", "xl", "xr", "f(xr)", "Error"])

# func_str = input("Escriba la función: ")
# x = sp.symbols("x")
# f = sp.sympify(func_str)
# np_f = sp.lambdify(x, func_str, "numpy")
# xr1, df1 = falsa_posicion(np_f, 4, 0, 0.01)
# xr2, df2 = falsa_posicion(np_f, 41, 15, 0.01)
#
# print(xr1, xr2)
