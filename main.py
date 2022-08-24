"""
José David Panaza Batres
Carné: 202111478
Programación Orientada a Objetos
Introducción a la programación 2
"""
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import *
from xml.dom import minidom
matrix = []


def menu():
    print("*********************************************************")
    print("            LAB. DE INVETIGACIÓN EPIDEMIOLÓGICA          ")
    print("                                                         ")
    print("Presione:")
    print("1. Para cargar y analizar un archivo.")
    print("2. Para Salir")
    resp = input()
    cargar_archivo(resp)


def cargar_archivo(resp):
    if(resp == "1"):
        # dialog para seleccionar archivo
        filetypes = (('Archivos XML', '*.xml'), ('Todos los archivos', '*.*'))
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        if filename == "":
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo")
            menu()
        else:
            try:
                doc = minidom.parse(filename)
                pacientes = doc.getElementsByTagName("paciente")
                print("*********************************************************")
                print("                  PACIENTES DISPONIBLES                  ")
                print("                                                         ")
                for paciente in pacientes:                    
                    nombre = paciente.getElementsByTagName("nombre")[0]
                    print("Nombre: " + str(nombre.firstChild.data))
                print("                                                         ")
                pacienteselected = input("Escriba el nombre del paciente que desea analizar: ")
                analizar_paciente(pacienteselected, doc)
            except:
                messagebox.showwarning("Advertencia", "No fue posible examinar el archivo XML")
                menu()
    else:
        exit()


def analizar_paciente(pacienteselected, doc):
    pacientes = doc.getElementsByTagName("paciente")
    pacienteencontrado = False
    for paciente in pacientes:
        nombre = paciente.getElementsByTagName("nombre")[0]
        if(pacienteselected == nombre.firstChild.data):
            pacienteencontrado = True
            m = paciente.getElementsByTagName("m")[0]
            if(int(m.firstChild.data) % 10 == 0):
                global matrix
                n = int(m.firstChild.data)
                matrix = [[0 for _ in range(n)] for _ in range(n)]
                print("si se puede")
            else:
                messagebox.showwarning("Advertencia", "El paciente archivo no cuenta con un número válido de columnas y filas")
                menu()
    if(pacienteencontrado == False):
        messagebox.showwarning("Advertencia", "El paciente no ha sido encontrado")
        menu()


menu()
