from .tektronix_tds1002b import TDS1002B
from .agilent_34970a import AGILENT34970A
from .sr830 import SR830
from .tektronix_afg3021b import AFG3021B
from .kurios import KURIOS

import inspect

clases = {
        "Osciloscopio Tektronix TDS1002B": TDS1002B,
        "Multiplexor Agilent 34970A": AGILENT34970A,
        "LOCKIN Stanford Research SR830": SR830,
        "Generador de funciones Tektronix AFG 3021B": AFG3021B, 
        "Kurios® Liquid Crystal Tunable Filter Controller": KURIOS,
        }

def listar_metodos_con_info(clase):
    metodos = []
    for nombre, miembro in inspect.getmembers(clase):
        if not nombre.startswith('_') and inspect.isfunction(miembro):
            sig = inspect.signature(miembro)
            doc = inspect.getdoc(miembro)
            primera_linea = doc.split("\n")[0] if doc else ""
            metodos.append((f"{nombre}{sig}", primera_linea))
    return metodos

def resumen():
    print("🧪 Paquete labo-instruments cargado.")
    print("Clases disponibles, métodos y descripción breve:\n")
    
    for nombre, clase in clases.items():
        print(f"📦 {nombre}")
        for firma, doc in listar_metodos_con_info(clase):
            print(f"   • {firma}")
            if doc:
                print(f"     ↪ {doc}")
        print()

    print("🛈 Para más información sobre una clase o método, podés usar help(NombreClase) o NombreClase.metodo? en IPython.")

resumen()
