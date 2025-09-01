"""
Kurios® Liquid Crystal Tunable Filter Controller (Thorlabs)
Manual: https://www.thorlabs.com/drawings/8095359c44da9912-173C283D-AAD0-DEC6-FD47CF7D75DF0BED/KURIOS2-Manual.pdf
"""

import time
import pyvisa

class KURIOS:

    def __init__(self, name):
        """
        Inicializa el controlador KURIOS.

        Abre la conexión con el fotocromador usando PyVISA, imprime la información del dispositivo
        y lo configura en modo manual (OM=1).
        """
        self._fotocromador = pyvisa.ResourceManager().open_resource(name)
        print(self._fotocromador.query('*IDN?')) 
        self._fotocromador.write('OM=1')

    def __del__(self):
        """
        Cierra la conexión VISA con el equipo.

        Esta función se llama automáticamente al eliminar el objeto.
        """
        self._fotocromador.close()	
    
    def set_longitud_de_onda(self,WL):
        """
        Establece la longitud de onda central del filtro.

        Parámetros:
        - WL (int o float): Longitud de onda en nanómetros dentro del rango permitido por el filtro.
        """

        self._fotocromador.write(f'WL={WL}')
    
    def set_ancho_de_banda(self,modo):
        """
        Establece el modo de ancho de banda para la secuencia.

        Parámetros:
        - modo (int): Código que representa el ancho de banda deseado.
            1 → BLACK (modo de bloqueo del haz)
            2 → WIDE (ancho de banda amplio)
            4 → MEDIUM (ancho de banda medio)
            8 → NARROW (ancho de banda estrecho)

        Nota: No todos los modelos de filtro KURIOS aceptan todos los modos.
        """
        self._fotocromador.write(f'BD={modo}')

    def get_temperature(self):
        """
        Consulta la temperatura actual del filtro óptico.

        Retorna:
        - (str): Temperatura actual en grados Celsius.
        """
        return self._fotocromador.query(f'TP?')