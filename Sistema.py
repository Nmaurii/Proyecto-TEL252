from pynput import keyboard
import time
import numpy as np

from funciones import *

class Sistema:

    def __init__(self, nombre, largo):
        self.__muestras = []
        self.__nombre = nombre
        self.__contrasena = None
        self.largo = largo

        #self.tiempo = None
        #self.intento = None 

    def login(self):
        """
        Captura un intento de login y retorna los tiempos y la contraseña ingresada
        """
        tiempos, contrasena = self.__capturar_patron_tecleo()
        print("\n")

        comparaciones = []
        
        for muestra in self.__muestras:
            resultado = comparar_patrones(tiempos,muestra)
            comparaciones.append(resultado) 

        print(comparaciones)
        graficar_comparacion(self.__muestras,tiempos)   
     
        
    
    def set_contrasena(self):
        while True:
            clave = input(f"Ingrese su contraseña de {self.largo} caracteres alfanumerico: ")
            if len(clave) >= self.largo:  
                self.__contrasena = clave
                break
            else:
                print(f"La contraseña debe tener al menos {self.largo} caracteres")

    
    def set_muestras(self,veces=2):
        contador = 0
        print(f"Ingrese la contraseña {veces} veces para registrar tiempos")

        while contador < veces:
            tiempos, contrasena = self.__capturar_patron_tecleo()
            
            if contrasena == self.__contrasena:
                self.__muestras.append(tiempos)
                contador += 1
                print(f"Muestra {contador}/{veces} registrada")
            else:
                print("Contraseña incorrecta, intente nuevamente")

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

    def __str__(self):
        return f"Usuario: {self.__nombre}\nContraseña: {'*' * len(self.__contrasena)}"
