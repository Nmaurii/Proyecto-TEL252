from Sistema import *
from funciones import *
import sys
import termios
import tty


def main():
    
    sistema = Sistema("Nicolas", 8)
    sistema.set_contrasena()

    sistema.set_muestras()    
    sistema.login()


    termios.tcflush(sys.stdin, termios.TCIOFLUSH)

if __name__ == "__main__":
    main()

