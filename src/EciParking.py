import sys #lib control de archivos
import sqlite3 #lib de base de datos SQLLITE
import os as Os #lib control de archivos
import os.path as path #lib leer archivos
import tkinter as tk #lib tkinter
from tkinter import messagebox #lib messagebox de tkinter
import time #Hora

nameDB = 'BiciParkDB'
Ubicacion_bd = Os.getcwd()+"\BiciParkDB.db" #variable de la ruta de base de datos
#variables de control de ventanas de tkinter para abrir y cerrarlas libremente
ventana=0
ventana_Park = 0
ventana_Ingr = 0
ventana_Sali = 0
contVentIngresar = False
contVentSalida = False
#diccionario con los datos actualizados de la base de datos
puestos = {}
carnets = []
libresA = 0
ocupadosA = 0
ocupadosB = 0
libresB = 0
#llevar control de los id
contPUESTO=0

#ventana de bienvenida
def ventana_Principal():
    global ventana, ventana_Park
    #crea ventana y se le hacen configuraciones
    ventana=tk.Tk()
    ventana.title("Bienvenido")
    ventana.configure(background="white")
    ventana.geometry("720x480")
    ventana.resizable(width=False, height=False)#no se podra grandar
    ventana.attributes("-topmost", True) #Siempre este la ventana encima de otras
    ventana.overrideredirect(1) #desactiva todo en la ventana
    fondo = tk.PhotoImage(file="fondo.png")#carga imagen
    lblFondo = tk.Label(ventana,image = fondo) #fondo
    bit = ventana.iconbitmap('icono.ico') #icono
    lblFondo.place(x=0, y=0, relwidth=1, relheight=1) #centrar fondo
    #texto de bienvenida
    TEXT1 = tk.Label(ventana,text="Bienvenido al programa\n de EciParking", bg="#A50606", fg="white",font='Helvetica 30 bold',relief="flat")
    TEXT1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    boton2 = tk.Button(ventana,text="Iniciar",command=ventana_Parking,font='Helvetica 16 bold', bg="#A50606", fg="white", bd= 5,activebackground="white",relief="solid") #boton iniciar
    boton2.pack(padx=5,pady=2,ipadx=20,ipady=5,side=tk.BOTTOM,before=TEXT1)
    boton3 = tk.Button(ventana,text="Cerrar",command=ventana.destroy, font='Helvetica 10 bold', bg="white", fg="black",relief="solid",bd= 5) #boton cerrar
    boton3.pack(padx=5,pady=2,ipadx=20,ipady=5,side=tk.BOTTOM,before=boton2)
    TEXT2 = tk.Label(ventana,text=" Por: Karen Piedra - Fernanda Cruz ", font='Helvetica 16 bold', bg="white", fg="#A50606", bd= 5,activebackground="white",relief="flat")
    TEXT2.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X,side=tk.BOTTOM,before=boton3)
    center(ventana)#centrar ventana
    crea_basededatos()#llamado a la funcion que crea el arcivo de base de datos
    sincronizarDatosDB()#extraigo datos BD
    
    ventana.mainloop()

def ventana_Parking():
    global ventana, ventana_Park, contVentIngresar, ventana_Ingr, libresA, ocupadosA, libresB, ocupadosB, ventana_Sali, contVentSalida
    #destruye la ventana de ingreso de datos sí ya se estaba antes en esa
    def cerrarApp():
        ventana.destroy()
    #destruir ventana ingresar si se sale de ahi y vuelve aca
    if(contVentIngresar):
        ventana_Ingr.destroy()
        contVentIngresar = False
    #destruir ventana Salida si se sale de ahi y vuelve aca
    if(contVentSalida):
        ventana_Sali.destroy()
        contVentSalida = False
    ventana.withdraw()
    ventana_Park = tk.Toplevel()
    ventana_Park.title("Zona de Parqueo")
    bit = ventana_Park.iconbitmap('icono.ico')
    ventana_Park.configure(background="#494545")
    ventana_Park.geometry("1024x625")
    ventana_Park.resizable(width=False, height=False)#no se podra grandar
    ventana_Park.overrideredirect(1) #desactiva todo en la ventana
    ventana_Park.attributes("-topmost", True)#Siempre este la ventana encima de otras
    fondo = tk.PhotoImage(file="zona-parking.png")
    lblFondo = tk.Label(ventana_Park,image = fondo).place(x=0,y=160)
    center(ventana_Park)#centro pantalla
    botones() #dibujo botones
    TEXT = tk.Label(ventana_Park,text="POR FAVOR SELECCIONE UNA CASILLA DE PARQUEO:", font='Helvetica 16 bold', bg="#A50606", fg="white", bd= 5,activebackground="white",relief="solid")
    TEXT.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    TEXT1 = tk.Label(ventana_Park,text="ZONA DE PARQUEO A \n libres: "+str(libresA)+"\n ocupados: "+str(ocupadosA), font='Helvetica 16 bold', bg="white", fg="#A50606", bd= 5,activebackground="white",relief="solid")
    TEXT1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    TEXT2 = tk.Label(ventana_Park,text="ZONA DE PARQUEO B \n libres: "+str(libresB)+"\n ocupados: "+str(ocupadosB), font='Helvetica 16 bold', bg="white", fg="#A50606", bd= 5,activebackground="white",relief="solid")
    TEXT2.place(x = 5, y = 470, relwidth = 1, width = -10, height = 100)
    botonCerrar = tk.Button(ventana_Park,text="Cerrar",command=cerrarApp, font='Helvetica 10 bold', bg="#A50606", fg="white",relief="solid",bd= 5) #boton cerrar
    botonCerrar.place(x = 512, y = 600, height = 40, anchor="center")
    
    ventana_Park.mainloop()
    
def ventana_Ingresar(puesto):
    global ventana, ventana_Park, ventana_Ingr, contVentIngresar, carnets
    contVentIngresar = True
    fechaHora = time.strftime("%c") #saco fecha y hora
    #funcion de verificacion de datos ingresados
    def agrega():
        if (not(is_number(carnet.get())) or (len(carnet.get()) != 7)):
            messagebox.showerror(message="Carnet incorrecto, por favor ingrese el numero correctamente de 7 digitos sin comas o otros caracteres, ejemplo(2101773)", title="Error Carnet")
        elif len(nombre.get())==0:
            messagebox.showerror(message="No tiene nada en nombre, por favor ingrese su nombre", title="Error nombre")
        elif (carnet.get() in carnets):
            messagebox.showerror(message="Este carnet ya cuenta con un Registro de entrada ingrese con otro carnet diferente", title="Carnet duplicado")
        else:
            messagebox.showinfo(message="Registro Completado", title="Exito!")
            ActualizarDatosBD(puesto,carnet.get(),nombre.get(),fechaHora,'true')
            ventana_Parking()
        
        
    ventana_Park.withdraw()
    ventana_Ingr = tk.Toplevel()
    ventana_Ingr.title("Registro Entrada para el puesto: "+puesto)
    bit = ventana_Ingr.iconbitmap('icono.ico')
    ventana_Ingr.configure(background="#D9D9D9")
    ventana_Ingr.geometry("450x350")
    ventana_Ingr.resizable(width=False, height=False)#no se podra grandar
    ventana_Ingr.attributes("-topmost", True)#Siempre este la ventana encima de otras
    ventana_Ingr.overrideredirect(1) #desactiva todo en la ventana
    fondo = tk.PhotoImage(file="registro.png")
    lblFondo = tk.Label(ventana_Ingr,image = fondo).place(x=0,y=50)
    center(ventana_Ingr)#centro pantalla
    TEXTIng1 = tk.Label(ventana_Ingr,text="Registre entrada al puesto: "+puesto, bg="#B40000", fg="white",font='Helvetica 16 bold')
    TEXTIng1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    #carnet
    carnet = tk.StringVar(ventana_Ingr)
    tk.Label(ventana_Ingr, text = "Carnet:", bg="#B40000",fg="white",font='Helvetica 11 bold',relief="solid", bd= 3).pack(padx=5,pady=5,ipadx=0,ipady=0)
    caja1 = tk.Entry(ventana_Ingr, textvariable=carnet,justify=tk.CENTER,relief="solid", bd= 1,font='Helvetica 11 bold')
    caja1.pack(padx=5,pady=5,ipadx=40,ipady=5)
    #nombre
    nombre = tk.StringVar(ventana_Ingr)
    tk.Label(ventana_Ingr, text = "Nombre:", bg="#B40000",fg="white",font='Helvetica 11 bold',relief="solid", bd= 3).pack(padx=5,pady=5,ipadx=0,ipady=0)
    caja2 = tk.Entry(ventana_Ingr, textvariable=nombre,justify=tk.CENTER,relief="solid", bd= 1,font='Helvetica 11 bold')
    caja2.pack(padx=5,pady=5,ipadx=50,ipady=5)
    #fecha
    TEXTIngFecha = tk.Label(ventana_Ingr,text="Fecha y hora del registro: "+fechaHora, bg="#B40000", fg="white",font='Helvetica 12 bold', relief="solid", bd= 3)
    TEXTIngFecha.pack(after=TEXTIng1)
    #boton registro
    botonIng1 = tk.Button(ventana_Ingr,text="Registrar Entrada",command=lambda : agrega(),font='Helvetica 16 bold', bg="#A50606", fg="white", bd= 5,activebackground="white",relief="solid") #boton cerrar
    botonIng1.pack(padx=5,pady=5,ipadx=5,ipady=5,side=tk.BOTTOM)
    #boton cancelar
    botonIng2 = tk.Button(ventana_Ingr,text="Cancelar",command=lambda : ventana_Parking(),font='Helvetica 10 bold', bg="#A50606", fg="white", bd= 5,activebackground="white",relief="solid") #boton cerrar
    botonIng2.pack(padx=5,pady=5,ipadx=5,ipady=5,side=tk.BOTTOM,before=botonIng1)
    ventana_Ingr.mainloop()

def ventana_Salida(puesto):
    global ventana, ventana_Park, ventana_Sali, contVentSalida, puestos
    contVentSalida = True
    ventana_Park.withdraw()#destruimos ventana parking
    fechaHora = time.strftime("%c") #saco fecha y hora
    #funcion de verificacion de datos ingresados
    def agrega():
        if ((not(is_number(carnet.get())) or (len(carnet.get()) != 7))):
            messagebox.showerror(message="Carnet incorrecto, por favor ingrese el numero correctamente de 7 digitos sin comas o otros caracteres, ejemplo(2101773)", title="Error Carnet")
            caja1.delete(0,tk.END) #limpia las cajas
        else:
            if not(str(carnet.get()) == puestos[puesto][0]):
                messagebox.showerror(message="Carnet no concuerda con el registrado \n por favor ingrese con el que afectuo el registro", title="Error Carnet no coincide")
            else:
                messagebox.showinfo(message="Salida Completada", title="Exito!")
                ActualizarDatosBD(puesto,carnet.get(),puestos[puesto][1],fechaHora,'false')
                ventana_Parking()
            
    ventana_Sali = tk.Toplevel()
    ventana_Sali.title("Registre Salida para el puesto: "+puesto)
    bit = ventana_Sali.iconbitmap('icono.ico')
    ventana_Sali.configure(background="#D9D9D9")
    ventana_Sali.geometry("450x350")
    ventana_Sali.resizable(width=False, height=False)#no se podra grandar
    ventana_Sali.attributes("-topmost", True)#Siempre este la ventana encima de otras
    ventana_Sali.overrideredirect(1) #desactiva todo en la ventana
    fondo = tk.PhotoImage(file="registro.png")
    lblFondo = tk.Label(ventana_Sali,image = fondo).place(x=0,y=50)
    center(ventana_Sali)#centro pantalla
    #titulo 1
    TEXTIng1 = tk.Label(ventana_Sali,text="Registre Salida al puesto: "+puesto, bg="#B40000", fg="white",font='Helvetica 16 bold')
    TEXTIng1.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    #fecha
    TEXTIngFecha = tk.Label(ventana_Sali,text="Fecha y hora de salida: "+fechaHora, bg="#B40000", fg="white",font='Helvetica 12 bold', relief="solid", bd= 3)
    TEXTIngFecha.pack(after=TEXTIng1)
    #carnet
    carnet = tk.StringVar(ventana_Sali)
    tk.Label(ventana_Sali, text = "Carnet:", bg="#B40000",fg="white",font='Helvetica 11 bold',relief="solid", bd= 3).pack(padx=5,pady=5,ipadx=0,ipady=0)
    caja1 = tk.Entry(ventana_Sali, textvariable=carnet,justify=tk.CENTER,relief="solid", bd= 1,font='Helvetica 11 bold')
    caja1.pack(padx=5,pady=5,ipadx=40,ipady=5)
    #boton registro
    botonIng1 = tk.Button(ventana_Sali,text="Registrar Salida",command=lambda : agrega(),font='Helvetica 16 bold', bg="#A50606", fg="white", bd= 5,activebackground="white",relief="solid") #boton cerrar
    botonIng1.pack(padx=5,pady=5,ipadx=5,ipady=5,side=tk.BOTTOM)
    #boton cancelar
    botonIng2 = tk.Button(ventana_Sali,text="Cancelar",command=lambda : ventana_Parking(),font='Helvetica 10 bold', bg="#A50606", fg="white", bd= 5,activebackground="white",relief="solid") #boton cerrar
    botonIng2.pack(padx=5,pady=5,ipadx=5,ipady=5,side=tk.BOTTOM,before=botonIng1)

    ventana_Sali.mainloop()
    
#dibujo todos los botones de la pantalla parking, esto tambien actualiza estado de botones y dibuja segun este o no ocupado
def botones():
    global ventana_Park
    sincronizarDatosDB()
    formatoLetra='Helvetica 10 bold'
    colorFondo="#F9EC47"
    colorLetra="black"
    borde="solid"
    posX=5
    posY=170
    #zona A
    for i in range(0,50):
        puesto = "A"+str(i+1)
        if (i==25):
            posX=5
            posY=225
        if (puestos[puesto][3] == 'false'):
            colorFondo="#49C603" #´puestos verdes desocupados
            exec('botonn{} = tk.Button(ventana_Park,text="A{}",command= lambda: cogerOretirarPuesto("A{}"),width=3,height=2, font=formatoLetra, bg=colorFondo, fg=colorLetra,relief=borde,bd= 2)'.format(i+1,i+1,i+1))
            exec('botonn{}.place(x=posX, y=posY)'.format(i+1))
        else:
            colorFondo="#D85F38" #´puestos rojos ocupados
            exec('botonn{} = tk.Button(ventana_Park,text="A{}",command= lambda: cogerOretirarPuesto("A{}"),width=3,height=2, font=formatoLetra, bg=colorFondo, fg=colorLetra,relief=borde,bd= 2)'.format(i+1,i+1,i+1))
            exec('botonn{}.place(x=posX, y=posY)'.format(i+1))
        posX += 41
        
    posX=5
    posY=360
    for i in range(0,50):
        puesto = "B"+str(i+1)
        if(i==25):
            posX=5
            posY=410
        if (puestos[puesto][3] == 'false'):
            colorFondo="#49C603" #´puestos verdes desocupados
            exec('botonn{} = tk.Button(ventana_Park,text="B{}",command= lambda: cogerOretirarPuesto("B{}"),width=3,height=2, font=formatoLetra, bg=colorFondo, fg=colorLetra,relief=borde,bd= 2)'.format(i+1,i+1,i+1))
            exec('botonn{}.place(x=posX, y=posY)'.format(i+1))
        else:
            colorFondo="#D85F38" #´puestos rojos ocupados
            exec('botonn{} = tk.Button(ventana_Park,text="B{}",command= lambda: cogerOretirarPuesto("B{}"),width=3,height=2, font=formatoLetra, bg=colorFondo, fg=colorLetra,relief=borde,bd= 2)'.format(i+1,i+1,i+1))
            exec('botonn{}.place(x=posX, y=posY)'.format(i+1))
        posX += 41

def cogerOretirarPuesto(puesto):
    #libre false
    if (puestos[puesto][3] == 'false'):
        ventana_Ingresar(puesto)

    #ocupado
    else:
        ventana_Salida(puesto)

#funcion que optimza y centra la ventana del programa a la ventana del computador
def center(toplevel): 
    toplevel.update_idletasks() 
    w = toplevel.winfo_screenwidth() 
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x')) 
    x = w/2 - size[0]/2 
    y = h/2 - size[1]/2 
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

#verifica si efectivamente una cadena puede ser un numero
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def sincronizarDatosDB():
    global puestos, libresA, libresB, ocupadosA, ocupadosB, carnets
    carnets = []
    libresA = 0
    libresB = 0
    ocupadosA = 0
    ocupadosB = 0
    con = sqlite3.connect(Ubicacion_bd)
    cursor = con.cursor()
    consulta=con.execute("SELECT * FROM PARKING_ZONE")#selecciono todos los datos
    resultados=consulta.fetchall()#guardo
    #meto en un diccionario los datos de la base de datos para trabajarlos mas comodamente despues
    for i in range(len(resultados)):
        puestos[resultados[i][0]] = [resultados[i][1],resultados[i][2],resultados[i][3],resultados[i][4]]
        #contador de puestos libres y ocupados en A y B
        #si es A
        if(('A' in resultados[i][0])):
            if (resultados[i][4]=='false'):
                libresA+=1
            else:
                carnets.append(resultados[i][1]) #lleno lista de carnets ocupados
                ocupadosA+=1
        #si es B
        else:
            if (resultados[i][4]=='false'):
                libresB+=1
            else:
                carnets.append(resultados[i][1]) #lleno lista carnets ocupados
                ocupadosB+=1
            
    
#agrega el PUESTO, CARNET, NOMBRE y FECHA a la tabla PARKING_ZONE dentro de la base de datos
def AgregarDatosBD(puesto,carnet,nombre,fecha,estado):
    con = sqlite3.connect(Ubicacion_bd)
    cursor = con.cursor()
    #se forma la cadena para insertar los datos correctamente
    cursor.execute(
        "INSERT INTO PARKING_ZONE VALUES (?, ?, ?, ?, ?)",
        (str(puesto), str(carnet), str(nombre), str(fecha), str(estado)))
    con.commit()
    con.close()

#elimina el dato dentro de la base de datos que sea igual al PUESTO
def ActualizarDatosBD(puesto,carnet,nombre,fecha,estado):
    con = sqlite3.connect(Ubicacion_bd)
    cursor = con.cursor()
    cursor.execute(
        "UPDATE PARKING_ZONE SET CARNET = ?, NOMBRE = ?, FECHA = ?, ESTADO = ? WHERE PUESTO = ?",
        (str(carnet), str(nombre), str(fecha), str(estado), str(puesto)))
    con.commit()
    con.close()
#elimina completamente base de datos y vuelve a crear una
def EliminarBaseDatos():
    Os.remove("BiciParkDB.db")
    crea_basededatos()
    
#crea la base de datos 
def crea_basededatos():
    #se verifica que el archivo BiciParkDB.db no este ya creado
    if not(path.exists("BiciParkDB.db")):
        con = sqlite3.connect(Ubicacion_bd)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE PARKING_ZONE
                        (PUESTO 	        TEXT PRIMARY KEY NOT NULL,
                        CARNET 		        TEXT NOT NULL,
                        NOMBRE 		        TEXT NOT NULL,
                        FECHA			TEXT NOT NULL,
                        ESTADO              TEXT NOT NULL)''')

        #se llenara la base de datos con los datos iniciales
        strPuestoA = "A"
        strPuestoB = "B"
        for i in range(50):
            #para los primeros 50 de la baia A
            strPuestoA += str(i+1)
            AgregarDatosBD(strPuestoA,0,0,0,'false')
            #para el resto de los 50 de la baia B
            strPuestoB += str(i+1)
            AgregarDatosBD(strPuestoB,0,0,0,'false')
            strPuestoA = "A"
            strPuestoB = "B"
        con.close()


ventana_Principal()
