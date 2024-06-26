"""
José David Panaza Batres
Carné: 202111478
Programación Orientada a Objetos
Introducción a la programación 2

"""

import os
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import *
from xml.dom import minidom
from Celula import Celula
import time
#VARIABLES GLOBALES
buscarpaciente = True
ejecucion = True
matrix = []
celulas = []
rejillas = []
rejillaimprimir = []
datos = ['','','']
#FUNCION MENU
def menu():
    global buscarpaciente 
    buscarpaciente = True
    print("*********************************************************")
    print("            LAB. DE INVETIGACIÓN EPIDEMIOLÓGICA          ")
    print("                                                         ")
    print("Presione:")
    print("1. Para cargar y analizar un archivo.")
    print("2. Para Salir")
    resp = input("Escriba la opción que desea realizar: ")
    cargar_archivo(resp)

#FUNCION PARA CARGAR EL ARCHIVO XML
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
        else:
            try:
                global buscarpaciente
                while(buscarpaciente):
                    doc = minidom.parse(filename)
                    pacientes = doc.getElementsByTagName("paciente")
                    print("*********************************************************")
                    print("                  PACIENTES DISPONIBLES                  ")
                    print("                                                         ")
                    for paciente in pacientes:                    
                        nombre = paciente.getElementsByTagName("nombre")[0]
                        print("Nombre: " + str(nombre.firstChild.data))
                    print("                                                         ")
                    pacienteselected = input("Escriba el nombre del paciente que desea analizar y escriba 2 para salir: ")
                    analizar_paciente(pacienteselected, doc)
            except:
                messagebox.showwarning("Advertencia", "No fue posible examinar el archivo XML")
                
    elif(resp == "2"):
        global ejecucion
        ejecucion = False
        print("Se ha terminado la ejecución del programa")
        
#FUNCION PARA ANALIZAR EL PACIENTE
def analizar_paciente(pacienteselected, doc):
    if(pacienteselected == "2"):
        global buscarpaciente
        buscarpaciente = False
        return
    pacientes = doc.getElementsByTagName("paciente")
    pacienteencontrado = False
    #se busca el paciente
    for paciente in pacientes:
        nombre = paciente.getElementsByTagName("nombre")[0]
        if(str(pacienteselected).upper() == str(nombre.firstChild.data).upper()):
            pacienteencontrado = True
            m = paciente.getElementsByTagName("m")[0]
            t = paciente.getElementsByTagName("periodos")[0]
            if(int(m.firstChild.data) % 10 == 0 and int(m.firstChild.data) < 10000 and int(t.firstChild.data) < 10000):                
                n = int(m.firstChild.data)
                p = int(t.firstChild.data)
                global matrix
                global celulas
                celulas = [[0 for _ in range(n)] for _ in range(n)] #FILA,COLUMNA
                matrix = [[0 for _ in range(n)] for _ in range(n)] #FILA,COLUMNA
                celdasinfec = paciente.getElementsByTagName("celda")
                try:
                    for celda in celdasinfec:
                        f = int(celda.getAttribute("f"))
                        c = int(celda.getAttribute("c"))
                        matrix[f][c] = 1
                    crearnodos(matrix,n,p,pacienteselected)
                except:
                    messagebox.showwarning("Advertencia", "El número de celda se sale del límite indicado")
                
            else:
                messagebox.showwarning("Advertencia", "El paciente archivo no cuenta con un número válido de columnas y filas o excedió el numero de células o periodos")
                
    if(pacienteencontrado == False):
        messagebox.showwarning("Advertencia", "El paciente no ha sido encontrado")
#SE CREAN LOS NODOS Y SE CONCECTAN A SUS VALORES
def crearnodos(matrix,n,p,paciente):
    #se crean y se conectan los nodos
    for i in range(0,n):
        for j in range(0,n):
            if(i == 0 and j == 0):
                celula = Celula(matrix[i][j],None, None, None, None, matrix[i][j+1], None, matrix[i+1][j], matrix[i+1][j+1])
            elif(i == 0 and j == (n-1)):
                celula = Celula(matrix[i][j],None, None,None,matrix[i][j-1],None,matrix[i+1][j-1],matrix[i+1][j],None)
            elif(i == (n-1) and j == 0):
                celula = Celula(matrix[i][j],None,matrix[i-1][j],matrix[i-1][j+1],None,matrix[i][j+1],None,None,None)
            elif(i == (n-1) and j == (n-1)):
                celula = Celula(matrix[i][j],matrix[i-1][j-1],matrix[i-1][j],None,matrix[i][j-1],None,None,None,None)                     
            elif(i == 0):
                celula = Celula(matrix[i][j],None,None,None,matrix[i][j-1],matrix[i][j+1],matrix[i+1][j-1],matrix[i+1][j],matrix[i+1][j+1])
            elif(i == (n-1)):
                celula = Celula(matrix[i][j],matrix[i-1][j-1],matrix[i-1][j],matrix[i-1][j+1],matrix[i][j-1],matrix[i][j+1],None,None,None)
            elif(j == 0):
                celula = Celula(matrix[i][j],None,matrix[i-1][j],matrix[i-1][j+1],None,matrix[i][j+1],None,matrix[i+1][j],matrix[i+1][j+1])
            elif(j == (n-1)):
                celula = Celula(matrix[i][j],matrix[i-1][j-1],matrix[i-1][j],None,matrix[i][j-1],None,matrix[i+1][j-1],matrix[i+1][j],None)
            else:
                celula = Celula(matrix[i][j],matrix[i-1][j-1],matrix[i-1][j],matrix[i-1][j+1],matrix[i][j-1],matrix[i][j+1],matrix[i+1][j-1],matrix[i+1][j],matrix[i+1][j+1])
            celulas[i][j] = celula
    rejillas.append(matrix)
    print("se crearon los nodos")     
    linea = ""   
    for i in range(0,n):
        for j in range(0,n):
            if(celulas[i][j].valor == 0):
                linea = linea + "□"
            else:
                linea = linea + "■"
        linea = linea + "\n"
    print(linea)
    tejidover = True
    while(tejidover):
        global datos
        resp = input("Desea ver como se desarrolla el tejido, responda S/N: ")
        if(resp.upper() == "S"):
            r = desarrollo(n,p)   
            resp2 = input("Para exportar los datos del paciente presione 1: ")
            if(resp2 == "1" or r == 1):
                reportes(paciente, datos[0],datos[1],datos[2])                
                rejillas.clear()
                celulas.clear()
                matrix.clear()  
                break
            rejillas.clear()
            celulas.clear()
            matrix.clear() 
            break
        elif(resp.upper() == "N"):
            tejidover = False
#FUNCION PARA VER EL DESARROLLO DE LAS CELULAS
def desarrollo(n,p):
    pasopaso = True
    np = 1
    tenfermedad = "Leve"
    Nperiodo0 = 0 #numero de periodo en donde se encuentra el patrón a repetir
    Nperiodo1 = 0 #cada cuanto se repite el periodo encontrado
    posiciones = []
    cont = 0    
    incurable = False
    for h in range(0,p):
        mtemp = celulas
        for i in range(0,n):
            for j in range(0,n):
                #SE VERIFICA SI HAY CELULAS VECINAS CONTAGIADAS
                if(mtemp[i][j].valor == 1):
                    if(mtemp[i][j].sigUL == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigU == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigUR == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigL == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigR == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigDL == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigD == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigDR == 1):
                        cont = cont + 1
                    # SE ACTUALIZAN LAS CELULAS A LA MATRIZ DE NODOS
                    if(cont == 2 or cont == 3):
                        celulas[i][j].valor = 1
                    else:
                        celulas[i][j].valor = 0
                    cont = 0
                elif(mtemp[i][j].valor == 0):
                    if(mtemp[i][j].sigUL == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigU == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigUR == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigL == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigR == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigDL == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigD == 1):
                        cont = cont + 1
                    if(mtemp[i][j].sigDR == 1):
                        cont = cont + 1
                    # SE ACTUALIZAN LAS CELULAS A LA MATRIZ DE NODOS
                    if(cont == 3):
                        celulas[i][j].valor = 1
                    else:
                        celulas[i][j].valor = 0
                    cont = 0
        #VER SI LA ENFERMEDAD ES INCURABLE QUE SE REPITE DESPUES DE SU PRIMER PERIODO  
        if(np == 1):
            repetidatotal = True                                
            for i in range(0,n):
                for j in range(0,n):
                    mtemporal = rejillas[0]
                    if(mtemporal[i][j] != celulas[i][j].valor):
                        repetidatotal = False
            if(repetidatotal):
                tenfermedad = " Incurable"
                incurable = True                                   
        if(incurable == False):
        #ver el tipo de enfermedad
            conti = 0
            for nmatrix in rejillas:                
                diferentes = False
                for i in range(0,n):
                    for j in range(0,n):
                        if(nmatrix[i][j] != celulas[i][j].valor):
                            diferentes = True
                if(diferentes == False): 
                    posiciones.append(conti)
                    if(Nperiodo0 == 0):
                        Nperiodo0 = np
                                                 
                    #Analizar el tipo de enfermedad
                conti = conti + 1
            if(len(posiciones) >= 2):
                Nperiodo1 = posiciones[len(posiciones)-1] - posiciones[len(posiciones)-2]
                if(Nperiodo1 == 1):
                    tenfermedad = " Incurable"
                else:
                    tenfermedad = " Grave"
        #CARGAR LA MATRIZ PARA GUARDAR EL REGISTRO    
        matriztemp =  [[0 for _ in range(n)] for _ in range(n)] 
        for i in range(0,n):
            for j in range(0,n):
                matriztemp[i][j] = celulas[i][j].valor
        
        rejillas.append(matriztemp)
        conectarnodos(n,matriztemp)            
        np = np + 1
        imprimircelulas(n,h,tenfermedad,Nperiodo0,Nperiodo1)
        global datos
        datos[0] = str(tenfermedad)
        datos[1] = str(Nperiodo0)       
        datos[2] = str(Nperiodo1)
        global rejillaimprimir
        rejillaimprimir = matriztemp
        if(pasopaso):
            flag = True
            while(flag):
                resp = input("introduzca 1 para el siguiente periodo, si desea ejecutar todos los periodos introduzca 2, si desea finalizar presione 3: ")
                if(resp == "2"):
                    pasopaso = False
                    flag = False
                elif(resp == "1"):
                    flag = False
                elif(resp == "3"):
                    return 1
                    
        else:                    
            time.sleep(0.5)
            
#FUNCION PARA CONECTAR LOS NODOS
def conectarnodos(n,matrix):
    for i in range(0,n):
        for j in range(0,n):
            if(i == 0 and j == 0):
                celulas[i][j].sigUL = None
                celulas[i][j].sigU = None
                celulas[i][j].sigUR = None
                celulas[i][j].sigL = None
                celulas[i][j].sigR = matrix[i][j+1]
                celulas[i][j].sigDL = None
                celulas[i][j].sigD = matrix[i+1][j]
                celulas[i][j].sigDR = matrix[i+1][j+1]
            elif(i == 0 and j == (n-1)):
                celulas[i][j].sigUL = None
                celulas[i][j].sigU = None
                celulas[i][j].sigUR = None
                celulas[i][j].sigL = matrix[i][j-1]
                celulas[i][j].sigR = None
                celulas[i][j].sigDL = matrix[i+1][j-1]
                celulas[i][j].sigD = matrix[i+1][j]
                celulas[i][j].sigDR = None                
            elif(i == (n-1) and j == 0):
                celulas[i][j].sigUL = None
                celulas[i][j].sigU = matrix[i-1][j]
                celulas[i][j].sigUR = matrix[i-1][j+1]
                celulas[i][j].sigL = None
                celulas[i][j].sigR = matrix[i][j+1]
                celulas[i][j].sigDL = None
                celulas[i][j].sigD = None
                celulas[i][j].sigDR = None                 
            elif(i == (n-1) and j == (n-1)):
                celulas[i][j].sigUL = matrix[i-1][j-1]
                celulas[i][j].sigU = matrix[i-1][j]
                celulas[i][j].sigUR = None
                celulas[i][j].sigL = matrix[i][j-1]
                celulas[i][j].sigR = None
                celulas[i][j].sigDL = None
                celulas[i][j].sigD = None
                celulas[i][j].sigDR = None                
            elif(i == 0):
                celulas[i][j].sigUL = None
                celulas[i][j].sigU = None
                celulas[i][j].sigUR = None
                celulas[i][j].sigL = matrix[i][j-1]
                celulas[i][j].sigR = matrix[i][j+1]
                celulas[i][j].sigDL = matrix[i+1][j-1]
                celulas[i][j].sigD = matrix[i+1][j]
                celulas[i][j].sigDR = matrix[i+1][j+1] 
            elif(i == (n-1)):
                celulas[i][j].sigUL = matrix[i-1][j-1]
                celulas[i][j].sigU = matrix[i-1][j]
                celulas[i][j].sigUR = matrix[i-1][j+1]
                celulas[i][j].sigL = matrix[i][j-1]
                celulas[i][j].sigR = matrix[i][j+1]
                celulas[i][j].sigDL = None
                celulas[i][j].sigD = None
                celulas[i][j].sigDR = None
            elif(j == 0):
                celulas[i][j].sigUL = None
                celulas[i][j].sigU = matrix[i-1][j]
                celulas[i][j].sigUR = matrix[i-1][j+1]
                celulas[i][j].sigL = None
                celulas[i][j].sigR = matrix[i][j+1]
                celulas[i][j].sigDL = None
                celulas[i][j].sigD = matrix[i+1][j]
                celulas[i][j].sigDR = matrix[i+1][j+1] 
            elif(j == (n-1)):
                celulas[i][j].sigUL = matrix[i-1][j-1]
                celulas[i][j].sigU = matrix[i-1][j]
                celulas[i][j].sigUR = None
                celulas[i][j].sigL = matrix[i][j-1]
                celulas[i][j].sigR = None
                celulas[i][j].sigDL = matrix[i+1][j-1]
                celulas[i][j].sigD = matrix[i+1][j]
                celulas[i][j].sigDR = None
            else:
                celulas[i][j].sigUL = matrix[i-1][j-1]
                celulas[i][j].sigU = matrix[i-1][j]
                celulas[i][j].sigUR = matrix[i-1][j+1]
                celulas[i][j].sigL = matrix[i][j-1]
                celulas[i][j].sigR = matrix[i][j+1]
                celulas[i][j].sigDL = matrix[i+1][j-1]
                celulas[i][j].sigD = matrix[i+1][j]
                celulas[i][j].sigDR = matrix[i+1][j+1] 
#FUNCION PARA IMPRIMIR LAS REGILLAS
def imprimircelulas(n, h, tp,n0,n1):
    print("*********************************************************")
    print("                       PERIODO: " + str(h+1))
    print("Tipo de enfermedad:"+ tp)    
    print("Primera repetición en el periodo "+ str(n0))
    if(n1 > 0):
        print("Se repite cada "+ str(n1) + " periodos")
        print("")
    linea = ""   
    for i in range(0,n):
        for j in range(0,n):
            if(celulas[i][j].valor == 0):
                linea = linea + "□"
            else:
                linea = linea + "■"
        linea = linea + "\n"
    print(linea)
def reportes(paciente,tipo, primerp, cadap):
    global rejillaimprimir
    n = len(rejillaimprimir)
    label = ""
    label += "digraph G {\n\n edge [fontname=\"Helvetica,Arial,san-serif\"]\n"
    label += "label=<\n<TABLE > \n"
    for i in range(0,n):
        label += "<TR>"
        for j in range(0,n):
            label += "<TD>"
            if(rejillaimprimir[i][j] == 0):
                label += "□"
            else:
                label += "■"
            label += "</TD>\n"
        label += "</TR>\n\n"
    label += "</TABLE>>;"
    label +="\"paciente: "+ paciente +"\n Tipo: "+ tipo +"\n Primera repeticion en: "+ primerp +"\n Se repite cada: "+ cadap +"\"\n\n}"
    nfile = "reporte_" + paciente
    f = open(nfile+".txt", 'w', encoding='utf-8')
    f.write(str(label))
    f.close()
    print("Reporte hecho!")
    os.system("dot -Tpdf "+ nfile +".txt -o "+ nfile +".pdf")
#LO QUE SE EJECUTA AL INICIO
while(ejecucion):
    menu()
