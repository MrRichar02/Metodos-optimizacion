import numpy as np
import pandas as pd
import sympy as sp

def newton(function, initial_value, mode, error):
    x = sp.symbols('x')
    function_first_derivate = sp.diff(function, x)
    function_second_derivate = sp.diff(function, x, 2)

    np_function = sp.lambdify(x, function, "numpy")
    np_function_first_derivate = sp.lambdify(x, function_first_derivate, "numpy")
    np_function_second_derivate = sp.lambdify(x, function_second_derivate, "numpy")

    match mode:
        case 0:
            raiz = initial_value
            rows = []
            while True:
                fd0 = np_function(raiz)
                fd1 = np_function_first_derivate(raiz)
                fd2 = np_function_second_derivate(raiz)
                last_raiz = raiz
                raiz -= np_function(raiz) / np_function_first_derivate(raiz)
                actual_error = abs(last_raiz - raiz)
                rows.append([last_raiz, fd0, fd1, fd2, actual_error])
                if actual_error < error:
                    break
            return raiz, pd.DataFrame(rows, columns=["x", "f(x)", "f'(x)", "f''(x)", "Error"])

        case 1:
            max_x = initial_value
            rows = []
            while True:
                fd0 = np_function(max_x)
                fd1 = np_function_first_derivate(max_x)
                fd2 = np_function_second_derivate(max_x)
                last_max_x = max_x
                max_x -= fd1 / fd2
                actual_error = abs(last_max_x - max_x)
                rows.append([last_max_x, fd0, fd1, fd2, actual_error])
                if actual_error < error:
                    break
            return max_x, pd.DataFrame(rows, columns=["x", "f(x)", "f'(x)", "f''(x)", "Error"])

# x = sp.symbols("x")
# try:
#     function = input("Escriba la función: ")
#     sp.pprint(sp.sympify(function))
# except sp.SympifyError as e:
#     print(f"error: {e}")
#
# newton(function, 2.5, 2, 0.0001)
