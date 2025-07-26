"""
LOCKIN Stanford Research SR830
Manual: http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf
Manual: https://github.com/diegoshalom/labosdf/blob/master/manuales/SR830m.pdf
"""


import pyvisa
import time

class SR830:
    '''Clase para el manejo amplificador Lockin SR830 usando PyVISA de interfaz'''

    scale_values = (2e-9, 5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9, 500e-9, 1e-6,
                    2e-6, 5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1e-3,
                    2e-3, 5e-3, 10e-3, 20e-3, 50e-3, 100e-3, 200e-3, 500e-3, 1) # in V

    time_constant_values = (10e-6, 30e-6, 100e-6, 300e-6, 1e-3, 3e-3, 10e-3, 30e-3, 100e-3, 300e-3,
                    1e0, 3e0, 10e0, 30e0, 100e0, 300e0, 1e3, 3e3, 10e3, 30e3) # in s

    def __init__(self, resource):
        """
        Inicializa la conexión con el Lock-in Amplifier SR830 mediante PyVISA.

        Args:
            resource (str): Dirección del recurso VISA del instrumento (por ejemplo, "GPIB0::8::INSTR").

        Side Effects:
            - Bloquea el panel frontal del equipo para evitar interacción manual.
            - Obtiene la escala y constante de tiempo actuales del equipo.
        """

        self._lockin = pyvisa.ResourceManager().open_resource(resource)
        #print(self._lockin.query('*IDN?')) # habria que ver si es mejor no pedir IDN. Puede que trabe la comunicacion al ppio
        self._lockin.write("LOCL 2") #Bloquea el uso de teclas del Lockin
        time.sleep(1) # tal vez ayuda a evitar errores de comunicacion del pyvisa
        self.scale = self.get_scale()
        self.time_constant = self.get_time_constant()

    def __del__(self):
        """
        Finaliza la conexión con el Lock-in SR830 y desbloquea el panel frontal.

        Side Effects:
            - Envía el comando "LOCL 0" para habilitar el control manual del equipo.
            - Cierra la conexión VISA.
        """
        self._lockin.write("LOCL 0") #Desbloquea el Lockin
        self._lockin.close()

    def set_modo(self, modo):
        """
        Configura el modo de entrada del instrumento.

        Args:
            modo (int): Código SCPI del modo de medición:
                0 = A
                1 = A-B
                2 = I (50Ω)
                3 = I (10MΩ)

        Returns:
            None
        """
        self._lockin.write("ISRC {0}".format(modo))

    def set_filtro(self, sen, tbase, slope):
        """
        Configura el filtro paso bajo del Lock-in, incluyendo sensibilidad, constante de tiempo y pendiente.

        Args:
            sen (int): Índice de sensibilidad (ver tabla en manual SR830).
            tbase (int): Índice de constante de tiempo.
            slope (int): Número de polos (slope) del filtro.

        Returns:
            None
        """
        self._lockin.write("OFLS {0}".format(slope))
        self._lockin.write("OFLT {0}".format(tbase))
        self._lockin.write("SENS {0}".format(sen))
       
    def set_aux_out(self, auxOut = 1, auxV = 0):
        """
        Configura la salida auxiliar seleccionada con un valor de tensión determinado.

        Args:
            auxOut (int): Número de canal AUX (1 a 4).
            auxV (float): Tensión de salida en voltios (-10.5 a +10.5 V).

        Returns:
            None

        Raises:
            ValueError: Si auxV está fuera del rango permitido.
        """
        self._lockin.write('AUXV {0}, {1}'.format(auxOut, auxV))
           
    def set_referencia(self,isIntern, freq, voltaje = 1):
        """
        Configura la fuente de referencia como interna o externa.

        Args:
            isIntern (bool): True para usar referencia interna, False para usar externa.
            freq (float): Frecuencia de la referencia interna en Hz.
            voltaje (float): Nivel de voltaje de salida de la referencia interna (default: 1 V).

        Returns:
            None
        """
        if isIntern:
            #Referencia interna
            #Configura la referencia si es así
            self._lockin.write("FMOD 1")
            self._lockin.write("SLVL {0:f}".format(voltaje))
            self._lockin.write("FREQ {0:f}".format(freq))
        else:
            #Referencia externa
            self._lockin.write("FMOD 0")
           
    def set_scale(self, scale_number):
        """
        Configura la sensibilidad del Lock-in según un índice en la lista de escalas disponibles.

        Args:
            scale_number (int): Índice entre 0 y len(scale_values) - 1.

        Returns:
            int: Índice aplicado, limitado al rango válido.
        """
        self.scale = min(scale_number,len(self.scale_values))
        self._lockin.write(f'SENS {self.scale}')
        return self.scale
   
    def get_scale(self):
        """
        Obtiene el índice actual de sensibilidad (escala de voltaje) del instrumento.

        Returns:
            int: Índice correspondiente a la sensibilidad configurada.
        """
        self.scale = int(self._lockin.query_ascii_values('SENS ?')[0])
        return self.scale

    def set_time_constant(self, time_constant_number):
        """
        Configura la constante de tiempo del filtro paso bajo del Lock-in.

        Args:
            time_constant_number (int): Índice dentro de `time_constant_values`.

        Returns:
            int: Valor de índice aplicado como constante de tiempo.
        """
        self._lockin.write(f'OFLT {time_constant_number}')
        self.time_constant = time_constant_number
        return self.time_constant
   
    def get_time_constant(self):
        """
        Consulta el índice de la constante de tiempo actualmente configurada.

        Returns:
            int: Índice en la tabla `time_constant_values`.
        """
        return int(self._lockin.query_ascii_values('OFLT ?')[0])

    def set_display(self, isXY):
        """
        Configura qué valores se muestran en el display del instrumento.

        Args:
            isXY (bool): True para mostrar X/Y; False para mostrar R/θ (magnitud y fase).

        Returns:
            None
        """
        if isXY:
            self._lockin.write("DDEF 1, 0") #Canal 1, x
            self._lockin.write('DDEF 2, 0') #Canal 2, y
        else:
            self._lockin.write("DDEF 1,1") #Canal 1, R
            self._lockin.write('DDEF 2,1') #Canal 2, T
   
    def get_display(self):
        """
        Obtiene los valores mostrados actualmente en el display (canales 1 y 2).

        Returns:
            list[float]: Lista de dos valores flotantes representando las mediciones actuales.
        """
        orden = "SNAP? 10, 11"
        return self._lockin.query_ascii_values(orden, separator=",")
       
    def get_medicion(self,isXY = True):
        """
        Obtiene una medición instantánea en formato X/Y o R/θ, según se especifique.

        Args:
            isXY (bool, optional): True para obtener [X, Y], False para obtener [R, θ]. Default: True.

        Returns:
            list[float]: Lista con dos elementos representando la medición actual.
        """
        orden = "SNAP? "
        if isXY:
            self._lockin.write("DDEF 1,0") #Canal 1, XY
            orden += "1, 2" #SNAP? 1,2
        else:
            self._lockin.write("DDEF 1,1") #Canal 1, RTheta
            orden += "3, 4" #SNAP? 3, 4
        return self._lockin.query_ascii_values(orden, separator=",")

    def auto_scale(self):
        """
        Ajusta automáticamente la escala del Lock-in para optimizar la medición de la magnitud R.

        Espera un número determinado de constantes de tiempo antes de cada lectura para asegurar estabilidad.

        Returns:
            tuple:
                - r (float): Valor final de magnitud R medido.
                - tita (float): Valor de ángulo θ correspondiente.
        """
        debug = True
        sup_theshold = 1
        inf_threshold = 0.1        
        nespera = 5 # se recomienda esperar entre 3 y 5 veces el tiempo de medicion entre escalado y medicion        
        tespera = self.time_constant_values[self.time_constant] * nespera
        time.sleep(tespera)
        r,tita = self.get_medicion(isXY=False)

        while r < self.scale_values[self.scale] * inf_threshold and self.scale > 0:
            if debug:
                print('Valor por debajo de threshold, bajo escala (r=%g, oldscale=%g)'%(r,self.scale_values[self.scale]))
            self.scale -= 1
            self.set_scale(self.scale)
            time.sleep(tespera) # esperar N * el tiempo de integracion antes de medir
            r,tita = self.get_medicion(isXY=False)

        while r > self.scale_values[self.scale] * sup_theshold and self.scale < (len(self.scale_values)-1):
            if debug:
                print('Overloaded, subo escala (oldscale=%g)'%(self.scale_values[self.scale]))
            self.scale += 1
            self.set_scale(self.scale)
            time.sleep(tespera)
            r,tita = self.get_medicion(isXY=False)
       
        if debug:
            print('Listo (r=%g, scale=%g)'%(r, self.scale_values[self.scale]))

        return r, tita