#!/usr/bin/env python
#-*- coding: utf-8 -*-
import ftplib
import time
from ftplib import FTP
import os, sys, configparser
import datetime
import time

#Directorio del FTP.cmd y resto del programa
os.chdir('/home/eoc/SBE38Terminal')

class config():
    def __init__(self, archivo_cfg):
        self.config(archivo_cfg)

    def config(self, archivo):
        self.dir_datos = os.getcwd()
        cfg = configparser.ConfigParser()
        cfg.read(self.dir_datos + os.sep + 'config.cfg')
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

cfg = config('config.cfg')
#print('Iniciando programa...')
#time.sleep(1)
#print('Iniciando conexion con el servidor')
#-------------------------------------------------------------------------------
#-- Nombre del archivo a subir (día anterior)
#-------------------------------------------------------------------------------
hoy = datetime.datetime.now()                                                                         # Obtengo fecha actual de la PC
dia = datetime.timedelta(days=1)
ayer = hoy - dia
nom_archivo = cfg.lugar + 'SBE38' + str(ayer.year) + str(ayer.month).zfill(2) + str(ayer.day).zfill(2) + '.txt'    # Nombre del archivo a cargar
hoy_nom_archivo = cfg.lugar + 'SBE38' + str(hoy.year) + str(hoy.month).zfill(2) + str(hoy.day).zfill(2) + '.txt'    # Nombre del archivo a cargar
#-------------------------------------------------------------------------------
#-- Inicio la conexión al FTP
#-------------------------------------------------------------------------------
try:
    ftp = FTP('ftp.inidep.edu.ar')                                                              #Configuro direccion fttp
    ftp.login('oceanografia','oceanus','ftp.inidep.edu.ar')                                     #Realizo el login al servidor fttp
except Exception as e:
    print (e)                                                                                   #Imprimo el error que dió
else:                                                                                           #Si no da error entonces...
    filelist = ftp.nlst()                                                                       #Devuelve lista de las carpetas en el FTTP
    print(filelist)
    if not('TSM' in filelist):                                                                  #Verificio que existe la carpeta 'TSM'
        ftp.mkd('TSM')
    #Subo el arvhivo
    ftp.cwd('TSM')                                                                              #Sí existe entonces entro a ella
    filelist = ftp.nlst()
    print(filelist)
    if not(cfg.lugar in filelist):                                                              #Verificio que existe la carpeta 'SCT'
        ftp.mkd(cfg.lugar)
    ftp.cwd(cfg.lugar)                                                                          #Sí existe entonces entro a ella

    # Subo el archivo del dia de hoy
    try:
        file = open(os.getcwd() + os.sep + 'Datos' + os.sep +hoy_nom_archivo,'rb')              # file to send
        ftp.storbinary('STOR ' + hoy_nom_archivo, file)                                         # send the file
        file.close()
    except:
        print('Archivo no encontrado: %s' %(hoy_nom_archivo))

    # Subo el archivo del dia de ayer
    try:
        file = open(os.getcwd() + os.sep + 'Datos' + os.sep +nom_archivo,'rb')                  # file to send
        ftp.storbinary('STOR ' + nom_archivo, file)                                             # send the file
        file.close()                                                                            # close file and FTP
    except:
        print('Archivo no encontrado: %s' %(nom_archivo))

    print('Finalizada la carga de archivos')
    time.sleep(30)						                                                        #Tiempo de espera antes de cerrar el programa
    ftp.quit()
