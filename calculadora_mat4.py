import streamlit as st
import sympy as sp

st.set_page_config(page_title="Calculadora MAT4 - UPES", layout="wide")
st.title("🧮 Calculadora de Sucesiones y Series")

# Definición de variables
n, x, k = sp.symbols('n x k')

menu = st.sidebar.selectbox("Seleccione Módulo", ["Sucesiones", "Series Infinitas", "Series de Potencias"])

# --- MÓDULO 1: SUCESIONES ---
if menu == "Sucesiones":
    st.header("Módulo 1: Sucesiones Infinitas")
    expr_input = st.text_input("Ingrese a_n:", "1/n")
    cant = st.number_input("Términos a mostrar:", 1, 100, 10)
    
    if st.button("Analizar Sucesión"):
        try:
            expr = sp.sympify(expr_input)
            lista = [float(expr.subs(n, i)) for i in range(1, cant + 1)]
            st.write("Términos:", lista)
            
            lim = sp.limit(expr, n, sp.oo)
            if lim.is_finite:
                st.success(f"Convergente. Límite: {lim}")
            else:
                st.error("Divergente")
        except Exception as e:
            st.error(f"Error: {e}")

# --- MÓDULO 2: SERIES ---
elif menu == "Series Infinitas":
    st.header("Módulo 2: Series Infinitas")
    expr_s = st.text_input("Ingrese a_k:", "(1/2)**k")
    
    if st.button("Analizar Serie"):
        try:
            s_expr = sp.sympify(expr_s)
            suma = sp.summation(s_expr, (k, 1, sp.oo))
            st.info(f"Suma exacta / Convergencia: {suma}")
            
            # Criterio de la razón simplificado
            razon = sp.limit(sp.Abs(s_expr.subs(k, k+1)/s_expr), k, sp.oo)
            st.write(f"Criterio de la razón (L): {razon}")
        except Exception as e:
            st.error(f"Error: {e}")

# --- MÓDULO 3: SERIES DE POTENCIAS ---
elif menu == "Series de Potencias":
    st.header("Módulo 3: Taylor y Error de Lagrange")
    f_in = st.text_input("Función f(x):", "exp(x)")
    c_val = st.number_input("Centro (c):", value=0.0)
    x_val = st.number_input("Punto x:", value=1.0)
    eps = st.number_input("Tolerancia (ε):", value=0.01, format="%.4f")

    if st.button("Calcular Grado Mínimo"):
        try:
            f_sym = sp.sympify(f_in)
            n_min = 0
            for i in range(1, 15): # Límite de seguridad
                der = sp.diff(f_sym, x, i + 1)
                max_der = max(abs(der.subs(x, c_val)), abs(der.subs(x, x_val)))
                err = (max_der / sp.factorial(i + 1)) * abs(x_val - c_val)**(i + 1)
                if err < eps:
                    n_min = i
                    break
            
            if n_min > 0:
                st.success(f"Grado necesario: n = {n_min}")
                poly = f_sym.series(x, c_val, n_min + 1).removeO()
                st.latex(sp.latex(poly))
            else:
                st.warning("Se requiere un grado mayor a 15.")
        except Exception as e:
            st.error(f"Error: {e}")
