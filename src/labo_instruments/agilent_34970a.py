"""
Multiplexor Agilent 34970A
Manual U (pdf): https://github.com/diegoshalom/labosdf/blob/master/manuales/Agilent34970a%20user%20manual.pdf
Manual P (pdf): https://github.com/diegoshalom/labosdf/blob/master/manuales/Agilent34970a%20command%20reference.pdf
Manual P (chm original): https://github.com/diegoshalom/labosdf/blob/master/manuales/Agilent34970a%20command%20reference.chm
"""

import pyvisa
import numpy as np
import datetime

class AGILENT34970A:
    """Clase para el manejo multiplexor Agilent34970A usando PyVISA de interfaz"""

    def __init__(self, name, 
                 scanInterval = 1, 
                 channelDelay = 0.2,
				 channelsList = (101,102,103,104,105,106,107,108)):
        """
        Inicializa la interfaz con el multiplexor Agilent 34970A y configura un barrido básico.

        Args:
            name (str): Dirección del recurso VISA del equipo (por ejemplo, "GPIB0::9::INSTR").
            scanInterval (float, optional): Tiempo entre cada barrido automático en segundos. Default: 1.
            channelDelay (float, optional): Retardo entre lecturas de canales. Default: 0.2.
            channelsList (tuple of int, optional): Canales a escanear. Default: (101, ..., 108).
                ⚠️ Si alguno de los canales está desconectado, dañado o no presente, el barrido fallará.
        """
        self.scanInterval = scanInterval
        self.channelDelay = channelDelay
        self.channelsList = channelsList
        self.nChannels = len(self.channelsList)
        self._mux = pyvisa.ResourceManager().open_resource(name)
        print(self._mux.query("*IDN?"))
        self.config(scanInterval =scanInterval, 
                 channelDelay = channelDelay,
				 channelsList =channelsList) 

    def __del__(self):
        """
        Cierra la conexión VISA con el equipo.

        Esta función se llama automáticamente al eliminar el objeto.
        """
        self._mux.close()	
	
    def config(  self, 
                 scanInterval = 1, 
                 channelDelay = 0.2,
				 channelsList = (101,102,103,104,105,106,107,108)):
        """
        Configura el barrido del multiplexor Agilent 34970A.

        Args:
            scanInterval (float, optional): Tiempo entre barridos, en segundos. Default: 1.
            channelDelay (float, optional): Retardo entre lecturas por canal. Default: 0.2.
            channelsList (tuple of int, optional): Canales a escanear. Default: (101–108).
                ⚠️ Si algún canal no responde correctamente, puede generar un error SCPI.
        
        Returns:
            None
        """

        #Setear atributos
        self.scanInterval = scanInterval
        self.channelDelay = channelDelay
        self.channelsList = channelsList
        self.nChannels = len(self.channelsList)

        #Limpiar configuración
        self._mux.write('*CLS')
        
        #Configurar barrido
        self._mux.write('ROUTE:SCAN (@' + str(self.channelsList)[1:-1] + ")")
        self._mux.write('ROUT:CHAN:DELAY ' + str(self.channelDelay))
        self._mux.write('FORMAT:READING:CHAN ON') #Return channel number with each reading
        self._mux.write('FORMAT:READING:TIME ON') # Return time stamp with each reading
		#self._mux.write('FORMat:READing:TIME:TYPE  RELative') #Return time stamp im seconds since scanstart
        self._mux.write('FORMat:READing:TIME:TYPE  ABSolute') #Return time stamp absolute
        self._mux.write('FORMat:READing:UNIT OFF')
        self._mux.write('TRIG:TIMER ' + str(self.scanInterval))		
        self._mux.write('TRIG:COUNT ' + str(1)) # one scan sweep per measure
    
    def get_time(self):	
        """
        Devuelve el tiempo actual del sistema interno del equipo en segundos desde la medianoche.

        Returns:
            float: Tiempo absoluto en segundos (formato timestamp).
        """
        self.initialTime = self._mux.query_ascii_values('SYSTEM:TIME?') #pido la hora de inicio			
        return float(self.initialTime[0])*3600 + float(self.initialTime[1])*60 + self.initialTime[2]	
	
    def query(self, myquery):
        """
        Envía una consulta SCPI al equipo y devuelve la respuesta.

        Args:
            myquery (str): Comando SCPI válido para lectura (por ejemplo: "*IDN?", "MEAS:TEMP?").

        Returns:
            str: Respuesta del equipo en texto plano.
        """
        return self._mux.query(myquery)

    def write(self, myquery):
        """
        Envía un comando SCPI al equipo sin esperar respuesta.

        Args:
            myquery (str): Comando SCPI válido de escritura (por ejemplo: "TRIG:IMM").

        Returns:
            None
        """
        self._mux.write(myquery)
    
    def one_scan(self):
        """
        Realiza un único barrido sobre los canales configurados.

        Returns:
            tuple:
                - data (list of float): Lecturas crudas del equipo.
                - temp (list of float): Valores de temperatura (u otra magnitud medida).
                - tim (list of float): Tiempos absolutos (timestamps) para cada medición.
                - chan (list of float): Números de canal asociados a cada lectura.
        """
        # time.sleep(.5+(self.channelDelay+0.1)*self.nChannels)
        
        data = self._mux.query_ascii_values('READ?')
        data2 = np.transpose(np.reshape(np.array(data), (self.nChannels, 8) ) )
        temp = data2[0]
        tim = np.array(data2[1:7], dtype=np.int32)
        tim = [datetime.datetime(x[0], x[1], x[2], x[3], x[4], x[5]).timestamp() for x in np.transpose(tim)]        
        chan = data2[7]
        
        return data,temp,tim,chan


