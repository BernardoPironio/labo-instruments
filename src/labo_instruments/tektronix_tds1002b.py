"""
Osciloscopio Tektronix TDS1002B
Manual U (web): https://github.com/diegoshalom/labosdf/blob/master/manuales/TDS1000%20manual-usuario.pdf
Manual P (web): https://github.com/diegoshalom/labosdf/blob/master/manuales/TDS1000%20programming_manual.pdf
"""

from matplotlib import pyplot as plt
import numpy as np
import visa

class TDS1002B:
    """Clase para el manejo osciloscopio TDS2000 usando PyVISA de interfaz"""
    
    def __init__(self, name):
        """
        Inicializa el osciloscopio Tektronix TDS1002B mediante VISA y configura parámetros básicos de adquisición.

        Args:
            name (str): Dirección del recurso VISA del osciloscopio (ej. "USB0::0x0699::0x0363::C102223::INSTR").

        Raises:
            VISAIOError: Si no se puede establecer la conexión con el equipo.
        """
        self._osci = visa.ResourceManager().open_resource(name)
        print(self._osci.query("*IDN?"))

    	#Configuración de curva
        
        # Modo de transmision: Binario positivo.
        self._osci.write('DAT:ENC RPB') 
        # 1 byte de dato. Con RPB 127 es la mitad de la pantalla
        self._osci.write('DAT:WID 1')
        # La curva mandada inicia en el primer dato
        self._osci.write("DAT:STAR 1") 
        # La curva mandada finaliza en el último dato
        self._osci.write("DAT:STOP 2500") 

        #Adquisición por sampleo
        self._osci.write("ACQ:MOD SAMP")
				
        #Bloquea el control del osciloscopio
        self._osci.write("LOC")
    	
    def __del__(self):
        """
        Cierra la conexión con el osciloscopio al eliminar el objeto.

        Esta función se invoca automáticamente. Libera el recurso VISA.
        """
        self._osci.close()			

    def config(self):
        """
        Configura la escala vertical de los canales 1 y 2 y el tiempo horizontal por defecto.

        Esta función sirve como ejemplo de inicialización típica. Puede modificarse para otros casos.

        Returns:
            None
        """
        self.set_channel(channel=1, scale=20e-3)
        self.set_channel(channel=2, scale=20e-3)
        self.set_time(scale=1e-3, zero=0)

    def unlock(self):
        """
        Desbloquea el control manual del osciloscopio (libera el modo remoto).

        Returns:
            None
        """
        self._osci.write("UNLOC")

    def set_channel(self, channel, scale, zero=0):
        """
        Configura la escala vertical y el offset de un canal.

        Args:
            channel (int): Número de canal (1 o 2).
            scale (float): Escala vertical en voltios/div.
            zero (float, optional): Posición vertical en divisiones. Default: 0.

        Returns:
            None
        """
    	#if coup != "DC" or coup != "AC" or coup != "GND":
    	    #coup = "DC"
    	#self._osci.write("CH{0}:COUP ".format(canal) + coup) #Acoplamiento DC
    	#self._osci.write("CH{0}:PROB 
        self._osci.write("CH{0}:SCA {1}".format(channel, scale))
        self._osci.write("CH{0}:POS {1}".format(channel, zero))
	
    def get_channel(self, channel):
        """
        Devuelve la configuración actual del canal especificado.

        Args:
            channel (int): Número de canal (1 o 2).

        Returns:
            str: Cadena SCPI con la configuración del canal.
        """
        return self._osci.query("CH{0}?".format(channel))
		
    def set_time(self, scale, zero=0):
        """
        Configura la escala horizontal (tiempo por división) y el desplazamiento.

        Args:
            scale (float): Tiempo por división (en segundos).
            zero (float, optional): Offset horizontal en divisiones. Default: 0.

        Returns:
            None
        """
        self._osci.write("HOR:SCA {0}".format(scale))
        self._osci.write("HOR:POS {0}".format(zero))	
	
    def get_time(self):
        """
        Devuelve la configuración horizontal del osciloscopio.

        Returns:
            str: Parámetros actuales de escala y posición horizontal.
        """
        return self._osci.query("HOR?")
	
    def read_data(self, channel):
        """
        Adquiere una forma de onda del canal especificado y la devuelve como arrays de tiempo y voltaje.

        ⚠️ Asegurate de que el canal esté activado y configurado correctamente antes de llamar a este método.

        Args:
            channel (int): Número de canal (1 o 2).

        Returns:
            tuple:
                - tiempo (numpy.ndarray): Array de tiempos correspondientes a cada punto de la curva.
                - data (numpy.ndarray): Array de valores de voltaje medidos.

        Raises:
            VISAIOError: Si ocurre un problema de comunicación con el equipo.
        """
        # Hace aparecer el canal en pantalla. Por si no está habilitado
        self._osci.write("SEL:CH{0} ON".format(channel)) 
        # Selecciona el canal
        self._osci.write("DAT:SOU CH{0}".format(channel)) 
    	#xze primer punto de la waveform
    	#xin intervalo de sampleo
    	#ymu factor de escala vertical
    	#yoff offset vertical
        xze, xin, yze, ymu, yoff = self._osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', 
                                                                 separator=';') 
        data = (self._osci.query_binary_values('CURV?', datatype='B', 
                                               container=np.array) - yoff) * ymu + yze        
        tiempo = xze + np.arange(len(data)) * xin
        return tiempo, data
    
    def get_range(self, channel):
        """
        Devuelve el rango de voltaje de la señal visible del canal especificado.

        Args:
            channel (int): Canal a consultar (1 o 2).

        Returns:
            numpy.ndarray: Array con los valores mínimo y máximo de voltaje del canal.
        """
        xze, xin, yze, ymu, yoff = self._osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', 
                                                                 separator=';')         
        rango = (np.array((0, 255))-yoff)*ymu +yze
        return rango   



