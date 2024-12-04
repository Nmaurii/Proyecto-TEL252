import tkinter as tk
from tkinter import ttk, messagebox
from Sistema import Sistema
from pynput import keyboard
import threading

from statistics import mean, median, mode, stdev


class Interfaz:
    def __init__(self, num_muestras=10):
        self.root = tk.Tk()
        self.root.title("Sistema Validador")
        self.root.geometry("400x300")
        
        self.sistema = None
        self.num_muestras = num_muestras
        self.capturando = False
        self.setup_main_screen()

    def setup_main_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Autenticación de datos", 
                font=('Arial', 16)).pack(pady=20)
        
        ttk.Button(self.root, text="Ingresar credenciales", 
                  command=self.mostrar_registro).pack(pady=10)
        ttk.Button(self.root, text="Validar", 
                  command=self.mostrar_login).pack(pady=10)

    def mostrar_registro(self):

        self.clear_screen()
        
        tk.Label(self.root, text="Registro de Usuario", 
                font=('Arial', 14)).pack(pady=10)
        
        tk.Label(self.root, text="Usuario:").pack()
        self.usuario_entry = ttk.Entry(self.root)
        self.usuario_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack()
        self.contrasena_entry = ttk.Entry(self.root, show="*")
        self.contrasena_entry.pack(pady=5)

        ttk.Button(self.root, text="Registrar", 
                  command=self.iniciar_registro).pack(pady=10)
        ttk.Button(self.root, text="Volver", 
                  command=self.setup_main_screen).pack()

    def iniciar_registro(self):
        nombre = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        
        if not nombre or not contrasena:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        self.sistema = Sistema(nombre, len(contrasena), self.num_muestras)
        self.sistema.set_contrasena(contrasena)
        self.iniciar_captura_patrones()

    def iniciar_captura_patrones(self):
        self.clear_screen()
        
        self.status_label = tk.Label(self.root, 
            text=f"Capture patrón de tecleo\nIntento 1/{self.num_muestras}", 
            font=('Arial', 12))
        self.status_label.pack(pady=10)
        
        self.instruccion_label = tk.Label(self.root, 
            text="Presione Enter para comenzar la captura...")
        self.instruccion_label.pack(pady=10)

        ttk.Button(self.root, text="Cancelar", 
                  command=self.setup_main_screen).pack(pady=10)

        self.root.bind('<Return>', self.comenzar_captura)

    def comenzar_captura(self, event=None):
        if not self.capturando:
            self.capturando = True
            self.instruccion_label.config(text="Escribiendo...")
            threading.Thread(target=self.capturar_patron).start()

    def capturar_patron(self):
        tiempos, contrasena = self.sistema._Sistema__capturar_patron_tecleo()
        self.root.after(0, self.procesar_captura, tiempos, contrasena)

    def procesar_captura(self, tiempos, contrasena):
        if contrasena == self.sistema._Sistema__contrasena:
            self.sistema._Sistema__muestras.append(tiempos)
            muestras_actuales = len(self.sistema._Sistema__muestras)
            
            if muestras_actuales < self.num_muestras:
                self.status_label.config(
                    text=f"Capture patrón de tecleo\nIntento {muestras_actuales + 1}/{self.num_muestras}")
                self.instruccion_label.config(text="Presione Enter para continuar...")
            else:
                messagebox.showinfo("Éxito", "Registro completado")
                self.setup_main_screen()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
            self.instruccion_label.config(text="Presione Enter para intentar nuevamente...")

        self.capturando = False

    def mostrar_login(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Iniciar Sesión", 
                font=('Arial', 14)).pack(pady=10)
        
        self.instruccion_label = tk.Label(self.root, 
            text="Presione Enter para comenzar la captura...")
        self.instruccion_label.pack(pady=10)

        ttk.Button(self.root, text="Cancelar", 
                  command=self.setup_main_screen).pack(pady=10)

        self.root.bind('<Return>', self.comenzar_login)

    def comenzar_login(self, event=None):
        if not self.capturando and self.sistema:
            self.capturando = True
            self.instruccion_label.config(text="Escribiendo...")
            threading.Thread(target=self.procesar_login).start()

    def procesar_login(self):
        resultado = self.sistema.login()
        if isinstance(resultado, tuple):  
            exito, promedio = resultado
            if exito:
                self.root.after(0, self.login_exitoso, promedio)
                return
        self.root.after(0, self.login_fallido)

    def login_exitoso(self, promedio):
        messagebox.showinfo("Éxito", f"Login exitoso con un coeficiente igual a {promedio:.4f}")
        self.mostrar_estadisticas()


   
    def login_fallido(self):
        messagebox.showerror("Error", "Login fallido")
        self.capturando = False
        self.mostrar_estadisticas()  
        
    def mostrar_estadisticas(self):
        self.clear_screen()

        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True, fill='both')

        tab_graficos = ttk.Frame(notebook)
        notebook.add(tab_graficos, text='Gráficos')

        frame_grafica = ttk.Frame(tab_graficos)
        frame_grafica.pack(expand=True, fill='both')

        self.sistema.mostrar_estadisticas(frame_grafica)

        tab_tabla = ttk.Frame(notebook)
        notebook.add(tab_tabla, text='Datos')
        self.crear_tabla_datos(tab_tabla)

        ttk.Button(self.root, text="Volver", 
                  command=self.setup_main_screen).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

    def mostrar_estadisticas(self):
        self.clear_screen()
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True, fill='both')
        
        tab_graficos = ttk.Frame(notebook)
        notebook.add(tab_graficos, text='Gráficos')
        
        frame_grafica = ttk.Frame(tab_graficos)
        frame_grafica.pack(expand=True, fill='both')
        
        self.sistema.mostrar_estadisticas(frame_grafica)  
        
        tab_tabla = ttk.Frame(notebook)
        notebook.add(tab_tabla, text='Datos')
        self.crear_tabla_datos(tab_tabla)
        
        ttk.Button(self.root, text="Volver", 
                  command=self.setup_main_screen).pack(pady=10)
        
    def crear_tabla_datos(self, parent):
        columns = ('Muestra', 'Tiempos', 'Coeficiente')
        tree = ttk.Treeview(parent, columns=columns, show='headings')

        tree.heading('Muestra', text='Muestra')
        tree.heading('Tiempos', text='Tiempos')
        tree.heading('Coeficiente', text='Coeficiente')

        tree.column('Muestra', width=100)
        tree.column('Tiempos', width=300)
        tree.column('Coeficiente', width=150)

        # Obtener datos
        muestras_iniciales = self.sistema.get_muestras_iniciales()
        muestras_actuales = self.sistema.get_muestras()
        muestra_login = self.sistema.get_muestra_login()
        coeficientes = self.sistema.coeficientes if hasattr(self.sistema, 'coeficientes') else None

        # Insertar cabecera para muestras iniciales
        tree.insert('', 'end', values=('MUESTRAS INICIALES', '', ''))

        # Insertar muestras iniciales
        for i, muestra in enumerate(muestras_iniciales):
            coef = coeficientes[i] if coeficientes else '-'
            tree.insert('', 'end', values=(
                f'Muestra {i+1}',
                f'[{", ".join([f"{t:.4f}" for t in muestra])}]',
                f'{coef:.4f}' if isinstance(coef, float) else '-'
            ))

        # Insertar separador
        tree.insert('', 'end', values=('', '', ''))
        tree.insert('', 'end', values=('MUESTRAS ACTUALES', '', ''))

        # Insertar muestras actualizadas
        for i, muestra in enumerate(muestras_actuales):
            tree.insert('', 'end', values=(
                f'Muestra {i+1}',
                f'[{", ".join([f"{t:.4f}" for t in muestra])}]',
                '-'
            ))

        # Insertar muestra de login
        if muestra_login is not None:
            tree.insert('', 'end', values=(
                'Login',
                f'[{", ".join([f"{t:.4f}" for t in muestra_login])}]',
                'Actual'
            ))

        # Insertar estadísticas
        if coeficientes:
            tree.insert('', 'end', values=('', '', ''))
            tree.insert('', 'end', values=(
                'ESTADÍSTICAS', '', ''
            ))
            tree.insert('', 'end', values=(
                'Promedio',
                '-',
                f'{mean(coeficientes):.4f}'
            ))
            tree.insert('', 'end', values=(
                'Desv. Est.',
                '-',
                f'{stdev(coeficientes):.4f}'
            ))

        # Configurar scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
"""
    def crear_tabla_datos(self, parent):
        columns = ('Muestra', 'Tiempos', 'Coeficiente')
        tree = ttk.Treeview(parent, columns=columns, show='headings')

        tree.heading('Muestra', text='Muestra')
        tree.heading('Tiempos', text='Tiempos')
        tree.heading('Coeficiente', text='Coeficiente')

        tree.column('Muestra', width=100)
        tree.column('Tiempos', width=300)
        tree.column('Coeficiente', width=150)

        muestras = self.sistema.get_muestras_iniciales()
        muestra_login = self.sistema.get_muestra_login()
        coeficientes = self.sistema.coeficientes if hasattr(self.sistema, 'coeficientes') else None

        for i, muestra in enumerate(muestras):
            coef = coeficientes[i] if coeficientes else '-'
            tree.insert('', 'end', values=(
                f'Muestra {i+1}',
                f'[{", ".join([f"{t:.4f}" for t in muestra])}]',
                f'{coef:.4f}' if isinstance(coef, float) else '-'
            ))

        if muestra_login is not None:
            tree.insert('', 'end', values=(
                'Login',
                f'[{", ".join([f"{t:.4f}" for t in muestra_login])}]',
                'Actual'
            ))

        if coeficientes:
            tree.insert('', 'end', values=(
                'Promedio',
                '-',
                f'{mean(coeficientes):.4f}'
            ))
            tree.insert('', 'end', values=(
                'Desv. Est.',
                '-',
                f'{stdev(coeficientes):.4f}'
            ))

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
"""
