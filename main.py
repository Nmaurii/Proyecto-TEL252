from Interfaz import *
from funciones import *
import sys
import termios
import tty


def main():

    cantidad_muestras = 5
    
    app = Interfaz(cantidad_muestras)
    app.run()


    #termios.tcflush(sys.stdin, termios.TCIOFLUSH)

if __name__ == "__main__":
    main()


