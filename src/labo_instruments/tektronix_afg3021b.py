"""
Generador de funciones Tektronix AFG 3021B
Manual U (web): https://github.com/diegoshalom/labosdf/blob/master/manuales/AFG3021B%20user%20manual.pdf
Manual P (web): https://github.com/diegoshalom/labosdf/blob/master/manuales/AFG3021B%20Programmer%20Manual.pdf
"""


import time

import numpy as np
import pyvisa

class AFG3021B:
    
    def __init__(self, name='USB0::0x0699::0x0346::C034165::INSTR'):
        """
    Inicializa la conexión con el generador de funciones Tektronix AFG3021B y activa la salida.

    Args:
        name (str, optional): Dirección del recurso VISA del generador. Default: puerto USB con ID genérico.

    Side Effects:
        - Establece conexión VISA.
        - Activa la salida del canal 1.
        - Imprime la identificación del dispositivo.
    """
        self._generador = pyvisa.ResourceManager().open_resource(name)
        print(self._generador.query('*IDN?'))
        
        #Activa la salida
        self._generador.write('OUTPut1:STATe on')
        # self.setFrequency(1000)
        
    def __del__(self):
        """
    Cierra la conexión con el generador de funciones al destruir el objeto.

    Side Effects:
        - Libera el recurso VISA asociado.
    """
        self._generador.close()
        
    def setFrequency(self, freq):
        """
    Configura la frecuencia de salida del generador.

    Args:
        freq (float): Frecuencia deseada en Hz.

    Returns:
        None
    """
        self._generador.write(f'FREQ {freq}')
        
    def getFrequency(self):
        """
    Consulta la frecuencia actualmente configurada en el generador.

    Returns:
        list[float]: Lista con la frecuencia actual en Hz (formato IEEE 488.2 ASCII).
    """
        return self._generador.query_ascii_values('FREQ?')
        
    def setAmplitude(self, ampl):
        """
    Configura la amplitud de la señal de salida.

    Args:
        ampl (float): Valor de amplitud deseado en voltios pico a pico (Vpp).

    Returns:
        None
    """
        return self._generador.write(f'VOLT {ampl}')
        
    def getAmplitude(self):
        """
    Configura la amplitud de la señal de salida.

    Args:
        ampl (float): Valor de amplitud deseado en voltios pico a pico (Vpp).

    Returns:
        None
    """
        return self._generador.query_ascii_values('FREQ?')
    
    def setFunction(self,func):
        """
    Configura la forma de onda de salida del generador.

    Args:
        func (str): Tipo de función deseada. Valores válidos incluyen:
            - "SIN" → Senoidal
            - "SQU" → Cuadrada
            - "RAMP" → Diente de sierra
            - "PULS" → Pulso
            - "NOIS" → Ruido
            - "DC" → Nivel DC
            - "USER" → Arbitraria definida por el usuario

    Returns:
        None
    """
        return self._generador.write(f'FUNC {func}')




