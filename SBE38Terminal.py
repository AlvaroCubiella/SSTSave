#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        SBE38 Terminal
# Purpose:
#
# Author:      Alvaro
#
# Created:     20-10-2014
# Copyright:   (c) Alvaro 2014
# Licence:     <your licence>
# Versiion:    V1.01
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-- Corroboro enlase internet
#-------------------------------------------------------------------------------
import sys, os, pdb, configparser

#-- Ruta de directorios

class SO():
    def __init__(self, sistema):
        self.SO = sistema
        self.sis(sistema)

    def sis(self, SO):
        if SO == 'win32':
            os.chdir("C:\SBE38 Terminal\Datos")
            self.directorio = os.getcwd();
            self.disp = 0
            self.tab = '\\'
            self.dir_py = sys.prefix
            self.cr = '\n'

        elif (SO == 'linux2') or (SO == 'linux'):
            os.chdir('/home/eoc/SBE38Terminal/Datos')
            self.directorio = os.getcwd()
            self.disp = '/dev/ttyUSB'
            self.tab = '/'
            self.dir_py = sys.prefix
            self.cr = '\r\n'


#-------------------------------------------------------------------------------
#-- Importo modulos, si no estan, los instala automaticamente...
#-------------------------------------------------------------------------------
def config_file(COM):
#    pdb.Pdb().set_trace()
    cfg = configparser.ConfigParser();
    if not cfg.read(['config.cfg']):
        sn = sensor.SerNum
        cfg.add_section('login')
        cfg.set('login', 'usuario', 'Alvaro Cubiella')
        cfg.set('login', 'Cuenta', 'datosbe38@gmail.com')
        cfg.set('login', 'Pass', 'gnmahc2015')
        cfg.add_section('Sistema')
        cfg.set('Sistema','SO', SO)
        cfg.set('Sistema','Directorio', os.getcwd())
        cfg.add_section('Conf_Sensor')
        cfg.set('Conf_Sensor', 'Modelo', 'SBE38')
        cfg.set('Conf_Sensor', 'S/N', sn)
        cfg.set('Conf_Sensor', 'puerto', sensor.COM)
        cfg.set('Conf_Sensor', 'BaudRate', '9600')
        cfg.add_section('Estacion')
        cfg.set('Estacion','Latitud','35.26543')
        cfg.set('Estacion','Longitud','45.23654')
        cfg.set('Estacion','Lugar','MdP')
        cfg.set('Estacion','Muestreo', '300')
        f = open('config.cfg','w')
        cfg.write(f)
        f.close()

import serial
import time, datetime, calendar
import imaplib, getpass
import email
import email.header
import subprocess
#import base64

#-------------------------------------------------------------------------------
#-- Defino variables globales
#-------------------------------------------------------------------------------
global Puerto, dato

#-------------------------------------------------------------------------------
#-- Escaneo los puertos disponibles
#-------------------------------------------------------------------------------
def scan_port(disp):
    comm_port=[];
    #-- Busco los primero 20 puertos
    for i in range(20):
        if type (disp) == str:
            com = disp + str(i)
        elif type(disp) == int:
            com = disp + i
        try:
            sensor = Sensor(com)
            #comm = serial.Serial(com, baudrate=9600);
            #comm.close();
            if sensor.SerNum != 'NaN':
                comm_port.append(com);
        except serial.SerialException:
            #-- Si el puerto no existe o no esta disponible da error
            pass;
    return comm_port;

def select_comm(numero_comm):
    if len(numero_comm)==0:
        print("No hay puertos disponibles\nPrograma finalizado!!");
        exit();
    else:
        print("Iniciando comunicacion en: COM%s" %(numero_comm[0]))
        COM = numero_comm[0];
    return COM;                     # Retorna el COM seleccionado

class Sensor():
    def __init__(self, COM):
        self.COM = COM;
        self.info_SBE38(COM)

    #-------------------------------------------------------------------------------
    #-- Extraigo informacion del SBE38
    #-------------------------------------------------------------------------------
    def info_SBE38(self, COM):
        try:
            comm = serial.Serial(COM,baudrate=9600);
            comm.portstr;
            comm.write("\r\n".encode());
            comm.write("d".encode());
            time.sleep(0.05);
            comm.write("c".encode());
            time.sleep(0.05);
            comm.write("\r\n".encode())
            time.sleep(0.25)
            info = comm.inWaiting()
            info = comm.read(info);
#            pdb.Pdb().set_trace()
#            info = info.decode()	
            info = info.rsplit("\r\n".encode());
            self.SerNum = "NaN"
#            for i in info:
#                if i[0:6] == "SBE 38":
#                    self.SerNum = i.rsplit("S/N = ")[1];
#                    self.Model = i.rsplit("S/N = ")[0];
#            pdb.Pdb().set_trace()
            self.SerNum = str(info)[str(info).index('S/N')+6:str(info).index('S/N')+11]
            comm.close()
            #return self.SerNum;
        except serial.SerialException:
          #-- Error al abrir el puerto serie
            #print("CONF. Error al abrir el puerto (%s)\n" %("COM"+str(COM+1)));
            #print("Finalizado!!");
            #exit();
            self.SerNum = "NaN"
            pass

    #-------------------------------------------------------------------------------
    #-- Inizializo y configuro el SBE38
    #-------------------------------------------------------------------------------
    def conf_SBE38(self, COM):
        try:
            comm = serial.Serial(COM,baudrate=9600);
            comm.portstr;
            comm.write("\r\n".encode());
            time.sleep(0.25);
            comm.write("s".encode());
            time.sleep(0.01);
            comm.write("t".encode());
            time.sleep(0.01);
            comm.write("o".encode());
            time.sleep(0.01);
            comm.write("p".encode());
            time.sleep(0.01);
            comm.write("\r\n".encode());
            time.sleep(0.25);
            comm.write("D".encode());
            time.sleep(0.01);
            comm.write("i".encode());
            time.sleep(0.01);
            comm.write("g".encode());
            time.sleep(0.01);
            comm.write("i".encode());
            time.sleep(0.01);
            comm.write("t".encode());
            time.sleep(0.01);
            comm.write("s".encode());
            time.sleep(0.01);
            comm.write("=".encode());
            time.sleep(0.01);
            comm.write("3".encode());
            time.sleep(0.01);
            comm.write("\r\n".encode());
            time.sleep(0.25);
            comm.close()
        except serial.SerialException:
          #-- Error al abrir el puerto serie
            #print("CONF. Error al abrir el puerto (%s)\n" %("COM"+str(Puerto+1)));
            #print("Finalizado!!");
            pass

    #-------------------------------------------------------------------------------
    #-- Capturo dato del sensor
    #-------------------------------------------------------------------------------
    def Data(self, COM):
        dato = '';
        try:
            comm = serial.Serial(COM,9600);
            comm.timeout = 6;
            comm.portstr;
            comm.write("\r\n".encode());
            time.sleep(0.05);
            comm.write("t".encode());
            time.sleep(0.01);
            comm.write("s".encode());
            time.sleep(0.01);
            comm.write("\r\n".encode());
            time.sleep(0.01);
            comm.flushInput()               #Borro buffer del puerto serie
            dato = comm.readline()            
            dato = str(dato.decode());
            if len(dato)!=0:
                self.dato = dato.rstrip("\n")
            else:
                self.dato = "NaN"
            comm.flushInput();
            comm.close()
#            pdb.Pdb().set_trace()
        except serial.SerialException:
          #-- Error al abrir el puerto serie
            print(" DATA. Error al abrir el puerto (%s)\n" %("COM" + str(COM)))
            print("Finalizado!!");
            mensaje_log = ("Error al abrir el puerto (%s)" %("COM" + str(COM)))
            evento_log = "Data"
            #escribir_log(mensaje_log, evento_log, path_destino, nom_log)
            exit();

class config():
    def __init__(self, archivo_cfg):
#	pdb.Pdb().set_trace()
        self.config(archivo_cfg)

    def config(self, archivo):
        self.dir_datos = os.getcwd()
        cfg = configparser.ConfigParser()
        cfg.read(['config.cfg'])
        self.Lat = cfg.get('Estacion', 'latitud')
        self.Lon = cfg.get('Estacion','longitud')
        self.lugar = cfg.get('Estacion','lugar')
        self.Intervalo = cfg.get('Estacion','muestreo')
        self.usuario = cfg.get('login', 'Usuario')
        self.email = cfg.get('login','cuenta')
        self.psw = cfg.get('login','pass')
        self.Modelo = cfg.get('Conf_Sensor', 'modelo')
        self.S_N = cfg.get('Conf_Sensor','s/n')
        self.COM = cfg.get('Conf_Sensor', 'puerto')
        self.ruta = cfg.get('Sistema','directorio')

#-------------------------------------------------------------------------------
#-- Creo archivo logfile
#-------------------------------------------------------------------------------
def escribir_log(mensaje, evento, destino, nom_log):
    #-- Directorio donde se encuentra el archivo log
    ruta = destino + SO.tab + nom_log;
    archivo = open(ruta,"a")
    fecha = time.time();
    fecha_UTC = time.gmtime(fecha)
    fecha_local = time.localtime(fecha)
    fecha_UTC = datetime.datetime.fromtimestamp(time.mktime(fecha_UTC))
    fecha_local = datetime.datetime.fromtimestamp(time.mktime(fecha_local))
    fecha_evento = "%s,%s"%(fecha_UTC,fecha_local)
    texto = "%s,%s,%s\n"%(fecha_evento,evento,mensaje);
    #texto = encriptar(texto);
    archivo.write(texto)
    #-- Cierro el archivo
    archivo.close()

#-------------------------------------------------------------------------------
#--------------------------------Encriptar-dato---------------------------------
#-------------------------------------------------------------------------------
def encriptar(texto):
    print (texto)
    textocodificado = base64.encodestring(texto)
    print (textocodificado)
    base64.decodestring(textocodificado)
    return textocodificado

#-------------------------------------------------------------------------------
#-- Creo archivo txt
#-------------------------------------------------------------------------------
def Crear_txt(destino):
    fecha = time.gmtime()             #-- Fecha y hora UTC para crear archivo
    lugar = cfg.lugar;          #-- Lugar donde esta instalado el sensor
    Sensor = cfg.Modelo;                  #-- Marca/Modelo del sensor SBE38
    anno = time.strftime("%Y");
    mes = time.strftime("%m");
    dia = time.strftime("%d");
    #-- Nombre archivo de adquisicopn
    nom_archivo = lugar + Sensor + anno + mes + \
        dia + ".txt"
    ruta = destino + SO.tab + nom_archivo
    #-- Nombre archivo log
    nom_log = lugar + Sensor + anno + mes + ".log"
    ruta_log = destino + SO.tab + nom_log
    try:
        os.stat(ruta_log);
    except:
        #-- Como no existe lo creo
        archivo = open(ruta_log,"w");
        #-- Genero cabecera del archivo log
        linea = "***************************************\n\
\tINICIO DE ARCHIVO LOG\n\t%s/%s/%s\n*******************\
********************\n"%(dia,mes,anno);
        #linea = encriptar(linea);
        archivo.write(linea);
        linea = "Directorio: %s\nPuerto COM %s\nIntervalo: %s segundos\n\n"\
            %(cfg.dir_datos,sensor.COM,cfg.Intervalo);
        #linea = encriptar(linea);
        archivo.write(linea);
        linea = "Fecha UTC,Fecha Local, Evento, Mensaje" + SO.cr;
        #linea = encriptar(linea);
        archivo.write(linea)
        #-- por ultimo lo cierro
        archivo.close();
    try:
        os.stat(ruta);
    except:
        #-- Como no existe lo creo
        archivo = open(ruta,"w");
        #-- Genero cabecera del archivo
        Cabecera(destino, nom_archivo, nom_log)
        #-- por ultimo lo cierro
        archivo.close();
    #-- Retorno la ruta donde se encuentra el archivo creado
    return nom_archivo, nom_log;

#-------------------------------------------------------------------------------
#-- Creo cabecera del archivo
#-------------------------------------------------------------------------------
def Cabecera(destino, nom_archivo, nom_log):
    #-- Informacion del SBE38
    SerNum = sensor.SerNum;
    #-- Ruta del archivo
    ruta = destino + SO.tab + nom_archivo
    fecha = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    fecha_UTC = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime())
    try:
        archivo = open(ruta,"w");
        #-- Escribo cabecera del archivo
        archivo.write("* Sea-Bird SBE 38 Data File:" + SO.cr);
        archivo.writelines("* FileName = " + str(ruta) + SO.cr);
        archivo.write("* SBE38 SN = " + SerNum  + SO.cr);
        archivo.write("* System UpLoad Time = " + str(fecha) + SO.cr);
        archivo.write("* System UpLoad UTC Time = " + fecha_UTC + SO.cr);
        archivo.write("* Latitud = " + cfg.Lat + SO.cr);
        archivo.write("* Longitud = " + cfg.Lon + SO.cr);
        archivo.write("* Lugar = " + cfg.lugar + SO.cr);
        archivo.write("* Responsable = " + cfg.usuario + SO.cr);
        archivo.write("* Intervalo de muestreo = " + cfg.Intervalo + SO.cr);
        archivo.write("* AutoStart = 1" + SO.cr);
        archivo.write("* Generar archivo = 1" + SO.cr);
        archivo.write("*END*" + SO.cr + SO.cr);
        archivo.write("Scan,Fecha,Hora,Temp" + SO.cr);
        archivo.close();
        #-- Registro log archivo creado
        mensaje_log = "Archivo %s creado correctamente"%nom_archivo
        evento_log = "INICIO"
        escribir_log(mensaje_log, evento_log, destino, nom_log)
    except:
        #-- Registro log archivo no creado
        mensaje_log = "Error al intentar crear el archivo %s"%nom_archivo
        evento_log = "Cabecera"
        escribir_log(mensaje_log, evento_log, destino, nom_log)

#-------------------------------------------------------------------------------
#-- Realizo lectura de temeratura y lo escribo en el archivo
#-------------------------------------------------------------------------------
def almacenar(destino, nom_archivo, hora_dato, scan):
    #-- Armo ruta donde esta localizado el archivo
    ruta = destino + SO.tab + nom_archivo;
    #-- Arbo el archivo
    archivo = open(ruta,"a");
    #-- Escribo el dato en el archivo
    archivo.write(str(scan)+","+hora_dato+","+str(sensor.dato)+"\n");
    #-- Cieroo el archivo
    archivo.close();

#-------------------------------------------------------------------------------
#------------------------------PROGRAMA-PRINCIPAL-------------------------------
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    SO = SO(sys.platform)
    cfg = config('config.cfg')
#    pdb.Pdb().set_trace()
#    puerto = scan_port(SO.disp)
    #-- Inicio puerto serie
    puerto = cfg.COM
#    puerto = select_comm(puerto);
    #-- Inicializo variables
    sensor = Sensor(puerto)
    #-- Cargo archivo configuracion
#    pdb.Pdb().set_trace()
    config_file(puerto)
    #-- Configuro SBE38
    sensor.conf_SBE38(puerto)
    cfg = config('config.cfg')
    cont = 1;
    intervalo = int(cfg.Intervalo);
    #-- Registro log inicio de adquisicion
    mensaje_log = "Inicio de adquisicion"
    evento_log = "INICIO"
    #-- Creo Archivo en el lugar de destino
    nom_archivo, nom_log = Crear_txt(cfg.dir_datos);
    escribir_log(mensaje_log, evento_log, cfg.dir_datos, nom_log)
    sensor.Data(sensor.COM)
    hora_dato = time.strftime("%d/%m/%Y %H:%M:%S");
    almacenar(cfg.dir_datos, nom_archivo, hora_dato, cont);
    print (cont, hora_dato, sensor.dato);
    hora_ant = hora_dato;
    while (True):
        #-- Hora actual del sistema
        horaA = hora_dato.rsplit(" ");horaA=horaA[1].rsplit(":");
        horaA = horaA = 3600*int(horaA[0])+60*int(horaA[1])+int(horaA[2])
        #-- Hora del ultimo dato registrado
        horaB = hora_ant.rsplit(" ");horaB=horaB[1].rsplit(":");
        horaB=3600*int(horaB[0])+60*int(horaB[1])+int(horaB[2])
        #-- Cambio de dia
        delta_seg = horaA - horaB;
        fechaA=hora_dato.rsplit(" ");fechaA=fechaA[0].rsplit("/");
        fechaB=hora_ant.rsplit(" ");fechaB=fechaB[0].rsplit("/");
        #-- Dias de diferencia
        delta_dia = int(fechaA[0])-int(fechaB[0]);
        if int(delta_dia) == 0: #-- Sigo en el mismo dia?
            if  int(delta_seg) >= int(intervalo):
                sensor.Data(sensor.COM);
                cont = cont + 1;
                almacenar(cfg.dir_datos, nom_archivo, hora_dato, cont);
                print (cont, hora_dato, sensor.dato);
                hora_ant = hora_dato;
            else:
                hora_dato = time.strftime("%d/%m/%Y %H:%M:%S");
        else:
            #-- Inicio nuevo archivo de adquisicion
            cont = 1;
            nom_archivo, nom_log = Crear_txt(cfg.dir_datos);
            sensor.Data(sensor.COM);
            hora_dato = time.strftime("%d/%m/%Y %H:%M:%S");
            almacenar(cfg.dir_datos, nom_archivo, hora_dato, cont);
            print ("\nInicio de nuevo archivo de adquisicion\n")
            print (cont, hora_dato, sensor.dato);
            hora_ant = hora_dato;
            mensaje_log = "Cambio de archivo de adquisicion"
            evento_log = "Cambio de dia"
            escribir_log(mensaje_log, evento_log, cfg.dir_datos, nom_log)
    print("Programa finalizado");
#-------------------------------------------------------------------------------
#-------------------------------FIN-DEL-PROGRAMA--------------------------------
#-------------------------------------------------------------------------------
