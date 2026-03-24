import numpy as np
import pandas as pd

def seccion_dorada(f, xu, xl, error, mode=1):
    PHI = (1+np.sqrt(5))/2
    interaciones = []
    PHI = (1+np.sqrt(5))/2
    CONSTANT = 1/PHI
    d = CONSTANT*(xu-xl)
    x1 = xl+d
    x2 = xu-d
    error_actual = abs(x1-x2)
    fx1 = f(x1)
    fx2 = f(x2)
    decision = fx2 > fx1
    interaciones.append([xl, xu, d, x1, x2, fx1, fx2, "f(x2)>f(x1)" if decision else "f(x2)<f(x1)", error_actual])
    while(error_actual > error):
        match mode:
            case 1:
                if decision:
                    xu = x1
                else:
                    xl = x2
            case 2:
                if not decision:
                    xu = x1
                else:
                    xl = x2
        d = CONSTANT*(xu-xl)
        x1 = xl+d
        x2 = xu-d
        error_actual = abs(x1-x2)
        fx1 = f(x1)
        fx2 = f(x2)
        decision = fx2 > fx1
        interaciones.append([xl, xu, d, x1, x2, fx1, fx2, "f(x2)>f(x1)" if decision else "f(x2)<f(x1)", error_actual])
    df = pd.DataFrame(interaciones, columns=["XL", "XU", "d", "X1", "X2", "F(X1)", "F(X2)", "Evaluacion", "Error"])
    return df

# func_str = input("Escriba la función: ")
# x = sp.symbols("x")
# f = sp.sympify(func_str)
# np_f = sp.lambdify(x, f, "numpy")
#
# data = seccion_dorada(np_f, 4, -4, 0.00001, 1)
# print(data)
