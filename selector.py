import os,sys
import time
import shutil
import argparse
from tkinter import filedialog as fd
 

def barra_progreso(iteracion, total, longitud=50):
    porcentaje = (iteracion / total) * 100
    completado = int(longitud * iteracion // total)
    barra = '=' * completado + '-' * (longitud - completado)
    sys.stdout.write(f'\r[{barra}] {porcentaje:.2f}% ({iteracion}/{total})')
    sys.stdout.flush()



def creando_backup(origen, destino,seleccion,contador = 0):
    
    total_archivos = sum(len(files) for _, _, files in os.walk(origen))
    if seleccion  == "*":
        shutil.copytree(origen,destino,dirs_exist_ok=True)
    else:
        list(seleccion)
        try:
            if not os.path.exists(destino):
                os.makedirs(destino)
                
            print(f"carpeta {destino} creada ")
            time.sleep(1)
            # Escanear el directorio actual
            with os.scandir(origen) as entradas:
                for entrada in entradas:
                    if entrada.is_file():   
                        
                        if entrada.name.split('.')[-1].lower() in seleccion:
                            contador +=1
                            ruta_archivo = os.path.join(origen, entrada.name)
                            #os.system("cls")
                            print(f'{entrada.name} -> {destino}')
                            
                            # copiando el archivo al destino
                            shutil.copy(ruta_archivo, os.path.join(destino,entrada.name))
                            #print(f"Archivo copiado: {ruta_archivo} -> {destino}")
                            time.sleep(0.2)
                            barra_progreso(contador,total_archivos)
                    elif entrada.is_dir():
                        # Recursividad papu
                        #print(f"Entrando en directorio: {entrada.path}")

                        nueva_ruta_destino = os.path.join(destino,entrada.name) # -> puta linea me hizo replantear 2 horas, al no crear otra ruta no se copiaban
                                                                                                    #los archivos de la raiz
                        creando_backup(entrada.path, nueva_ruta_destino, seleccion)
                    
                            
        except FileNotFoundError:
            print(f"La ruta {origen} no existe.")
        except PermissionError:
            print(f"No tienes permisos para acceder a {origen}.")
        




parametro = argparse.ArgumentParser()
parametro.add_argument("-i","--imagenes", help="Copiara Solo imagenes del origen", action="store_true")
parametro.add_argument("-v","--videos", help="Copiara Solo Videos del origen", action="store_true")
parametro.add_argument("-o","--ofimatica", help="Copiara Solo documentos de ofimatica del origen", action="store_true")
parametro.add_argument("-a","--todo", help="Copiara todo del origen", action="store_true")
argumentos = parametro.parse_args()

origen = fd.askdirectory()
destino = os.path.expanduser('~')+"\\Desktop\\"+f"{origen.split('/')[-1]}_Backup"


IMAGEN = "jpg jpeg png bpn gif tiff heif raw psd webp".split(' ')
VIDEOS ="mp4 mov wmv avi mkv flv webm avchd rm rmvb 3gp".split(' ')
OFIMATICA ="xls xlsx xlsm xlsb xltx doc docx ppt pptx rtf txt ".split(' ')
AUDIO = "mp3 m4a wav wma ogg aiff flac alac ape bwf dsd mqa mp3hd ply wav mp3 m4a ogg".split(' ')
TODO = "*"

if argumentos.imagenes:
    print('Formatos a escanear: %s'%IMAGEN)
    time.sleep(1)
    creando_backup(origen, destino,IMAGEN)
if argumentos.videos:
    creando_backup(origen, destino,VIDEOS)
if argumentos.ofimatica:
    creando_backup(origen, destino,OFIMATICA)
if argumentos.todo:
    creando_backup(origen, destino,TODO)

if not any(vars(argumentos).values()):
    parametro.print_help()
    sys.exit(1)


