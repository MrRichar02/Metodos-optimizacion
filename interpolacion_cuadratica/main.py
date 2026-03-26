import pandas as pd

def interpolacion_cuadratica(x0, x1, x2, f, error, mode=1):
    iteraciones = []
    max_iter = 10000
    iter_count = 0

    while True:
        iter_count += 1
        if iter_count > max_iter:
            raise ValueError("No converge (máximo de iteraciones alcanzado)")
        fx0, fx1, fx2 = f(x0), f(x1), f(x2)

        # verificar que no se pase del rango
        if mode == 1:  
            if not (fx0 < fx1 > fx2):
                raise ValueError(f"El intervalo [{x0}, {x2}] no contiene un máximo. "
                               f"f({x0})={fx0}, f({x1})={fx1}, f({x2})={fx2}. "
                               "Se requiere f(x0) < f(x1) > f(x2)")
        else:  
            if not (fx0 > fx1 < fx2):
                raise ValueError(f"El intervalo [{x0}, {x2}] no contiene un mínimo. "
                               f"f({x0})={fx0}, f({x1})={fx1}, f({x2})={fx2}. "
                               "Se requiere f(x0) > f(x1) < f(x2)")

        numerador = (
            fx0 * (x1**2 - x2**2) + fx1 * (x2**2 - x0**2) + fx2 * (x0**2 - x1**2)
        )
        denominador = 2 * fx0 * (x1 - x2) + 2 * fx1 * (x2 - x0) + 2 * fx2 * (x0 - x1)

        if abs(denominador) < 1e-12:
            raise ValueError("Denominador cercano a cero")

        x3 = numerador / denominador


        if abs(x3 - x1) < 1e-12:
            raise ValueError("El método se estancó")

        fx3 = f(x3)
        error_actual = abs(x3 - x1)

        iteraciones.append([x0, x1, x2, x3, fx0, fx1, fx2, fx3, error_actual])

        match mode:
            case 1:
                if x3 >= x1 and fx3 > fx1:
                    x0 = x1
                    x1 = x3
                elif x3 >= x1 and fx3 < fx1:
                    x2 = x3
                elif x3 < x1 and fx3 < fx1:
                    x0 = x3
                elif x3 < x1 and fx3 > fx1:
                    x2 = x1
                    x1 = x3

            case 2:
                if x3 >= x1 and fx3 < fx1:
                    x0 = x1
                    x1 = x3
                elif x3 >= x1 and fx3 > fx1:
                    x2 = x3
                elif x3 < x1 and fx3 > fx1:
                    x0 = x3
                elif x3 < x1 and fx3 < fx1:
                    x2 = x1
                    x1 = x3

        if error_actual <= error:
            break

    return x3, pd.DataFrame(
        iteraciones,
        columns=["x0", "x1", "x2", "x3", "f(x0)", "f(x1)", "f(x2)", "f(x3)", "Error"],
    )

# func_str = input("Escriba la función: ")
# f = sp.sympify(func_str)
# x = sp.symbols("x")
# np_f = sp.lambdify(x, func_str, "numpy")
#
# data = interpolacion_cuadratica(-4, 0, 4, np_f, 0.0000001, 2)
# print(data)
