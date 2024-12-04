from pynput import keyboard
import time
import numpy as np

from funciones import *
from statistics import mean, median, mode, stdev
import copy

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class Sistema:

    def __init__(self,nombre,largo,veces):
        
        self.__muestras = []
        self.__muestras_iniciales = []
        self.__nombre = nombre
        self.__contrasena = None
        self.__tiempoLogin = None
        #self.__coeficiente = None
        self.coeficientes = None
        self.veces = veces

        self.largo = largo

        #self.tiempo = None
        #self.intento = None 
            

    def login(self):
        """
        Captura un intento de login y retorna los tiempos y la contraseña ingresada
        luego cambie la peor muestra si el login es exitoso
        """
        tiempos, contrasena = self.__capturar_patron_tecleo()
        print("\n")

        self.__tiempoLogin = tiempos

        self.__muestras_iniciales = copy.deepcopy(self.__muestras)


        comparaciones = []
        
        for muestra in self.__muestras:
            resultado = comparar_patrones(tiempos,muestra)
            comparaciones.append(resultado) 

        promedio,desv = mean(comparaciones),stdev(comparaciones)

        self.coeficientes = comparaciones
        indice_menor = np.argmin(comparaciones)

        if(self.__contrasena == contrasena and promedio >= 0.8-desv):
            self.__muestras[indice_menor] = tiempos
            #self.__coeficiente = promedio

            return True,promedio
        else:
            return False,0
        
    def mostrar_estadisticas(self, frame):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)

        muestras_ref = self.__muestras
        muestra_nueva = self.__tiempoLogin

        for i, muestra in enumerate(muestras_ref):
            if len(muestra) >= 2:
                x_nuevo, y_nuevo = interpolar_muestra(muestra)
                ax.plot(x_nuevo, y_nuevo, '-', label=f'Muestra de referencia {i+1}')

        if muestra_nueva is not None and len(muestra_nueva) >= 2:
            x_nuevo, y_nuevo = interpolar_muestra(muestra_nueva)
            ax.plot(np.arange(len(muestra_nueva)), muestra_nueva, 'ro', 
                    label='Muestra nueva', markersize=10)
            ax.plot(x_nuevo, y_nuevo, 'r--', label='Interpolación muestra nueva')

        ax.set_title('Comparación de Patrones de Tecleo')
        ax.set_xlabel('Posición de la tecla')
        ax.set_ylabel('Tiempo entre teclas (s)')
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')
   
    
    def set_contrasena(self,clave):
        while True:
            #clave = input(f"Ingrese su contraseña de {self.largo} caracteres alfanumerico: ")
            if len(clave) >= self.largo:  
                self.__contrasena = clave
                break
            else:
                print(f"La contraseña debe tener al menos {self.largo} caracteres")

    
    def set_muestras(self):
        contador = 0
        print(f"Ingrese la contraseña {self.veces} veces para registrar tiempos")

        while contador < self.veces:

            tiempos, contrasena = self.__capturar_patron_tecleo()
            if contrasena == self.__contrasena:
                self.__muestras.append(tiempos)
                contador += 1
                print(f"\nMuestra {contador}/{self.veces} registrada")
            else:
                print("\nContraseña incorrecta, intente nuevamente")

    def __capturar_patron_tecleo(self):

        tiempos = []
        tiempo_anterior = None
        contrasena = ""

        def al_presionar(tecla):
            nonlocal tiempo_anterior, contrasena
            tiempo_actual = time.time()

            try:
                if hasattr(tecla, 'char'):
                    caracter = tecla.char
                    if caracter is not None:
                        contrasena += caracter

                    if tiempo_anterior is not None:
                        tiempos.append(tiempo_actual - tiempo_anterior)

                    tiempo_anterior = tiempo_actual

                elif tecla == keyboard.Key.enter:
                    return False

                elif tecla == keyboard.Key.backspace and len(contrasena) > 0:
                    contrasena = contrasena[:-1]
                    if tiempos:
                        tiempos.pop()

            except AttributeError:
                pass

        print("Ingrese su contraseña y presione Enter: ", end="", flush=True)
        with keyboard.Listener(on_press=al_presionar) as escuchador:
            escuchador.join()

        return tiempos, contrasena

    def get_muestras(self):
        return self.__muestras
    
    def get_muestras_iniciales(self):
        return self.__muestras_iniciales
    
    def get_muestra_login(self):
        return self.__tiempoLogin


    def get_coeficientes(self):
        return self.coeficientes

    def __str__(self):
        return f"Usuario: {self.__nombre}\nContraseña: {'*' * len(self.__contrasena)}"