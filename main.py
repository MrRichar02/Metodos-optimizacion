from aleatoria.main import aleatorio
from biseccion.main import biseccion
from falsa_posicion.main import falsa_posicion
from interpolacion_cuadratica.main import interpolacion_cuadratica
from newton.main import newton
from razon_dorada.main import seccion_dorada
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

x_sym, y_sym = sp.symbols("x y")


# ══════════════════════════════════════════════════════════════════════════════
# Utilidades
# ══════════════════════════════════════════════════════════════════════════════

def parse_numpy_1d(func_str):
    """Convierte un string a función numpy de una variable (x)."""
    expr = sp.sympify(func_str)
    return sp.lambdify(x_sym, expr, "numpy")

def parse_numpy_2d(func_str):
    """Convierte un string a función numpy de dos variables (x, y)."""
    expr = sp.sympify(func_str)
    return sp.lambdify([x_sym, y_sym], expr, "numpy")

def parse_sympy(func_str):
    """Devuelve expresión sympy (para Newton)."""
    return sp.sympify(func_str)

def show_dataframe(parent, df, title="Resultados"):
    """Abre una ventana Toplevel con el DataFrame en una tabla."""
    win = tk.Toplevel(parent)
    win.title(title)

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=6, pady=6)

    cols = list(df.columns)
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=110, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", "end", values=[f"{v:.6g}" if isinstance(v, float) else v for v in row])

    vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(win, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew", in_=frame)
    vsb.grid(row=0, column=1, sticky="ns", in_=frame)
    hsb.grid(row=1, column=0, sticky="ew", in_=frame)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

def plot_1d(parent, func_str, x_range=(-10, 10), title="Función"):
    """Gráfica 2D de una función de una variable."""
    try:
        np_f = parse_numpy_1d(func_str)
        xs = np.linspace(x_range[0], x_range[1], 500)
        ys = np_f(xs)

        win = tk.Toplevel(parent)
        win.title(f"Gráfica – {title}")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(xs, ys, color="steelblue", linewidth=2)
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_title(f"f(x) = {func_str}")
        ax.set_xlabel("x"); ax.set_ylabel("f(x)")
        ax.grid(True, alpha=0.3)
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    except Exception as e:
        messagebox.showerror("Error gráfica", str(e), parent=parent)

def plot_error(parent, df, title="Error por iteración"):
    """Gráfica de la columna Error del DataFrame."""
    if df is None or "Error" not in df.columns:
        return
    win = tk.Toplevel(parent)
    win.title(f"Error – {title}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["Error"].values, marker="o", color="crimson", linewidth=1.5, markersize=4)
    ax.set_title("Error por iteración")
    ax.set_xlabel("Iteración"); ax.set_ylabel("Error")
    ax.grid(True, alpha=0.3)
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def plot_3d(parent, func_str, x_range=(-5, 5), y_range=(-5, 5), title="Función 3D"):
    """Gráfica 3D de una función de dos variables."""
    try:
        np_f = parse_numpy_2d(func_str)
        xs = np.linspace(x_range[0], x_range[1], 60)
        ys = np.linspace(y_range[0], y_range[1], 60)
        X, Y = np.meshgrid(xs, ys)
        Z = np_f(X, Y)

        win = tk.Toplevel(parent)
        win.title(f"Gráfica 3D – {title}")
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.85)
        ax.set_title(f"f(x,y) = {func_str}")
        ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("f(x,y)")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    except Exception as e:
        messagebox.showerror("Error gráfica 3D", str(e), parent=parent)


# ══════════════════════════════════════════════════════════════════════════════
# Frame genérico con campo de resultado x
# ══════════════════════════════════════════════════════════════════════════════

def make_field(parent, label, row, default=""):
    tk.Label(parent, text=label).grid(row=row, column=0, sticky="e", padx=4, pady=2)
    var = tk.StringVar(value=default)
    tk.Entry(parent, textvariable=var, width=28).grid(row=row, column=1, sticky="w", padx=4, pady=2)
    return var

def result_row(parent, row):
    tk.Label(parent, text="Resultado x:").grid(row=row, column=0, sticky="e", padx=4, pady=4)
    var = tk.StringVar(value="")
    tk.Entry(parent, textvariable=var, state="readonly", width=28,
             readonlybackground="#e8f4e8").grid(row=row, column=1, sticky="w", padx=4, pady=4)
    return var


# ══════════════════════════════════════════════════════════════════════════════
# Pestañas de cada método
# ══════════════════════════════════════════════════════════════════════════════

def tab_aleatorio(nb):
    frm = ttk.Frame(nb); nb.add(frm, text="Aleatorio")
    f_var   = make_field(frm, "f(x,y):",       0, "y - x - 2*x**2 - 2*x*y - y**2")
    xmin_v  = make_field(frm, "x_lower:",       1, "-2")
    xmax_v  = make_field(frm, "x_upper:",       2, "2")
    ymin_v  = make_field(frm, "y_lower:",       3, "1")
    ymax_v  = make_field(frm, "y_upper:",       4, "3")
    iter_v  = make_field(frm, "Iteraciones:",   5, "1000")
    res_var = result_row(frm, 6)

    def run():
        try:
            func_str = f_var.get()
            np_f = parse_numpy_2d(func_str)
            lim_x = (float(xmax_v.get()), float(xmin_v.get()))
            lim_y = (float(ymax_v.get()), float(ymin_v.get()))
            iters = int(iter_v.get())
            df = aleatorio(lim_x, lim_y, iters, np_f)
            best = df.iloc[-1]
            res_var.set(f"x={best['Max x']:.6g}, y={best['Max y']:.6g}")
            show_dataframe(frm.winfo_toplevel(), df, "Aleatorio – Tabla")
            # rango para gráfica 3d tomado de los límites
            x_range = (float(xmin_v.get()), float(xmax_v.get()))
            y_range = (float(ymin_v.get()), float(ymax_v.get()))
            plot_3d(frm.winfo_toplevel(), func_str, x_range, y_range, "Aleatorio")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frm, text="Calcular", command=run).grid(row=7, column=0, columnspan=2, pady=6)

def tab_biseccion(nb):
    frm = ttk.Frame(nb); nb.add(frm, text="Bisección")
    f_var  = make_field(frm, "f(x):",     0, "3*x**2 - 120*x + 100")
    xu_v   = make_field(frm, "xu:",       1, "45")
    xl_v   = make_field(frm, "xl:",       2, "35")
    err_v  = make_field(frm, "Error:",    3, "0.000001")
    res_var = result_row(frm, 4)

    def run():
        try:
            func_str = f_var.get()
            np_f = parse_numpy_1d(func_str)
            xu, xl = float(xu_v.get()), float(xl_v.get())
            err = float(err_v.get())
            xr, df = biseccion(np_f, xu, xl, err)
            if xr is None:
                messagebox.showwarning("Sin raíz", "La función no cambia de signo.")
                res_var.set("")
                return
            res_var.set(f"{xr:.8g}")
            show_dataframe(frm.winfo_toplevel(), df, "Bisección – Tabla")
            plot_1d(frm.winfo_toplevel(), func_str, (min(xl, xu)-1, max(xl, xu)+1), "Bisección")
            plot_error(frm.winfo_toplevel(), df, "Bisección")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frm, text="Calcular", command=run).grid(row=5, column=0, columnspan=2, pady=6)

def tab_falsa_posicion(nb):
    frm = ttk.Frame(nb); nb.add(frm, text="Falsa Posición")
    f_var  = make_field(frm, "f(x):",  0, "x**3 - 6*x**2 + 11*x - 6")
    xu_v   = make_field(frm, "xu:",    1, "4")
    xl_v   = make_field(frm, "xl:",    2, "0")
    err_v  = make_field(frm, "Error:", 3, "0.01")
    res_var = result_row(frm, 4)

    def run():
        try:
            func_str = f_var.get()
            np_f = parse_numpy_1d(func_str)
            xu, xl = float(xu_v.get()), float(xl_v.get())
            err = float(err_v.get())
            xr, df = falsa_posicion(np_f, xu, xl, err)
            if xr is None:
                messagebox.showwarning("Sin raíz", "La función no cambia de signo.")
                res_var.set("")
                return
            res_var.set(f"{xr:.8g}")
            if df is not None and not df.empty:
                show_dataframe(frm.winfo_toplevel(), df, "Falsa Posición – Tabla")
                plot_error(frm.winfo_toplevel(), df, "Falsa Posición")
            plot_1d(frm.winfo_toplevel(), func_str, (min(xl, xu)-1, max(xl, xu)+1), "Falsa Posición")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frm, text="Calcular", command=run).grid(row=5, column=0, columnspan=2, pady=6)

def tab_interpolacion(nb):
    frm = ttk.Frame(nb); nb.add(frm, text="Interpolación Cuadrática")
    f_var  = make_field(frm, "f(x):",   0, "-x**2 + 10*x")
    x0_v   = make_field(frm, "x0:",     1, "-4")
    x1_v   = make_field(frm, "x1:",     2, "0")
    x2_v   = make_field(frm, "x2:",     3, "4")
    err_v  = make_field(frm, "Error:",  4, "0.0000001")
    mode_v = make_field(frm, "Mode (1=max, 2=min):", 5, "1")
    res_var = result_row(frm, 6)

    def run():
        try:
            func_str = f_var.get()
            np_f = parse_numpy_1d(func_str)
            x0, x1, x2 = float(x0_v.get()), float(x1_v.get()), float(x2_v.get())
            err  = float(err_v.get())
            mode = int(mode_v.get())
            xr, df = interpolacion_cuadratica(x0, x1, x2, np_f, err, mode)
            res_var.set(f"{xr:.8g}")
            show_dataframe(frm.winfo_toplevel(), df, "Interpolación Cuadrática – Tabla")
            plot_1d(frm.winfo_toplevel(), func_str, (min(x0,x2)-1, max(x0,x2)+1), "Interpolación Cuadrática")
            plot_error(frm.winfo_toplevel(), df, "Interpolación Cuadrática")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frm, text="Calcular", command=run).grid(row=7, column=0, columnspan=2, pady=6)

def tab_newton(nb):
    frm = ttk.Frame(nb); nb.add(frm, text="Newton")
    f_var   = make_field(frm, "f(x):",           0, "x**3 - 2*x - 5")
    xi_v    = make_field(frm, "Valor inicial:",   1, "2.5")
    mode_v  = make_field(frm, "Mode (0=raíz, 1=optim):", 2, "0")
    err_v   = make_field(frm, "Error:",           3, "0.0001")
    res_var = result_row(frm, 4)

    def run():
        try:
            func_str = f_var.get()
            sym_f = parse_sympy(func_str)
            xi   = float(xi_v.get())
            mode = int(mode_v.get())
            err  = float(err_v.get())
            xr, df = newton(sym_f, xi, mode, err)
            res_var.set(f"{xr:.8g}")
            show_dataframe(frm.winfo_toplevel(), df, "Newton – Tabla")
            # rango centrado en xi
            plot_1d(frm.winfo_toplevel(), func_str, (xi-5, xi+5), "Newton")
            plot_error(frm.winfo_toplevel(), df, "Newton")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frm, text="Calcular", command=run).grid(row=5, column=0, columnspan=2, pady=6)

def tab_seccion_dorada(nb):
    frm = ttk.Frame(nb); nb.add(frm, text="Sección Dorada")
    f_var  = make_field(frm, "f(x):",  0, "-x**2 + 10*x")
    xu_v   = make_field(frm, "xu:",    1, "4")
    xl_v   = make_field(frm, "xl:",    2, "-4")
    err_v  = make_field(frm, "Error:", 3, "0.00001")
    mode_v = make_field(frm, "Mode (1=max, 2=min):", 4, "1")
    # Sección dorada no devuelve x directo, dejamos vacío
    tk.Label(frm, text="Resultado x:").grid(row=5, column=0, sticky="e", padx=4)
    tk.Entry(frm, state="readonly", width=28,
             readonlybackground="#e8f4e8").grid(row=5, column=1, sticky="w", padx=4)

    def run():
        try:
            func_str = f_var.get()
            np_f = parse_numpy_1d(func_str)
            xu, xl = float(xu_v.get()), float(xl_v.get())
            err  = float(err_v.get())
            mode = int(mode_v.get())
            df = seccion_dorada(np_f, xu, xl, err, mode)
            show_dataframe(frm.winfo_toplevel(), df, "Sección Dorada – Tabla")
            plot_1d(frm.winfo_toplevel(), func_str, (min(xl, xu)-1, max(xl, xu)+1), "Sección Dorada")
            plot_error(frm.winfo_toplevel(), df, "Sección Dorada")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frm, text="Calcular", command=run).grid(row=6, column=0, columnspan=2, pady=6)


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    root.title("Métodos de Optimización Numérica")
    root.resizable(False, False)

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=8, pady=8)

    tab_aleatorio(nb)
    tab_biseccion(nb)
    tab_falsa_posicion(nb)
    tab_interpolacion(nb)
    tab_newton(nb)
    tab_seccion_dorada(nb)

    root.mainloop()

if __name__ == "__main__":
    main()
