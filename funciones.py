import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from scipy.integrate import simpson


def interpolar_muestra(tiempos, num_puntos=100):

    x_orig = np.arange(len(tiempos))    
    cs = CubicSpline(x_orig, tiempos)
    
    x_nuevo = np.linspace(0, len(tiempos)-1, num_puntos)
    y_nuevo = cs(x_nuevo)
    
    return x_nuevo, y_nuevo


def calcular_energia(senal):
    """
    Calcula la energía de una señal: Eg = ∫g²(t)dt
    """
    senal_cuadrada = np.power(senal, 2)
    energia = simpson(senal_cuadrada)
    return energia

def calcular_correlacion(senal1, senal2):
    """
    Calcula la correlación c = (1/√(Eg*Ex)) ∫g(t)x*(t)dt
    """
    E_g = calcular_energia(senal1)
    E_x = calcular_energia(senal2)
    
    producto = senal1 * senal2  
    integral = simpson(producto)
    
    correlacion = integral / np.sqrt(E_g * E_x)
    
    return correlacion

def comparar_patrones(patron1, patron2):
    """
    Compara dos patrones de tecleo y muestra sus estadísticas
    """
    correlacion = calcular_correlacion(np.array(patron1), np.array(patron2))
    '''
    print(f"\nEnergía patrón 1: {calcular_energia(np.array(patron1)):.4f}")
    print(f"Energía patrón 2: {calcular_energia(np.array(patron2)):.4f}")
    print(f"Correlación: {correlacion:.4f}")
    '''
    return correlacion

def graficar_muestras(muestras):
   plt.figure(figsize=(12, 6))

   for i, muestra in enumerate(muestras):
       x_nuevo, y_nuevo = interpolar_muestra(muestra)
       plt.plot(np.arange(len(muestra)), muestra, 'o', label=f'Puntos originales {i+1}')
       plt.plot(x_nuevo, y_nuevo, '-', label=f'Interpolación {i+1}')

   plt.title('Interpolación Cúbica de Patrones de Tecleo')
   plt.xlabel('Posición de la tecla')
   plt.ylabel('Tiempo entre teclas (s)')
   plt.grid(True)
   plt.legend()
   plt.show()

   for i, muestra in enumerate(muestras):
       print(f"\nMuestra {i+1}:")
       print(f"Media: {np.mean(muestra):.4f} segundos")
       print(f"Desviación estándar: {np.std(muestra):.4f} segundos")

def graficar_comparacion(muestras_ref, muestra_nueva):
   """
   Grafica las muestras de referencia como líneas continuas y 
   la nueva muestra como puntos
   """
   plt.figure(figsize=(12, 6))

   for i, muestra in enumerate(muestras_ref):
       x_nuevo, y_nuevo = interpolar_muestra(muestra)
       plt.plot(x_nuevo, y_nuevo, '-', label=f'Muestra de referencia {i+1}')

   x_nuevo, y_nuevo = interpolar_muestra(muestra_nueva)
   plt.plot(np.arange(len(muestra_nueva)), muestra_nueva, 'ro', 
           label='Muestra nueva', markersize=10)
   plt.plot(x_nuevo, y_nuevo, 'r--', label='Interpolación muestra nueva')

   plt.title('Comparación de Patrones de Tecleo')
   plt.xlabel('Posición de la tecla')
   plt.ylabel('Tiempo entre teclas (s)')
   plt.grid(True)
   plt.legend()
   plt.show()

   print("\nEstadísticas de muestras de referencia:")
   for i, muestra in enumerate(muestras_ref):
       print(f"\nMuestra {i+1}:")
       print(f"Media: {np.mean(muestra):.4f} segundos")
       print(f"Desviación estándar: {np.std(muestra):.4f} segundos")

   print("\nEstadísticas de muestra nueva:")
   print(f"Media: {np.mean(muestra_nueva):.4f} segundos")
   print(f"Desviación estándar: {np.std(muestra_nueva):.4f} segundos")
